"""
Load, validate, prettyprint, and dump JSON Abstract Encoding Notation (JADN) schemas
"""

import json
import jsonschema
from datetime import datetime
from .codec import is_builtin, is_primitive
from .codec_utils import opts_s2d

# TODO: Establish CTI/JSON namespace conventions, merge "module" (name) and "namespace" (module unique id) properties
# TODO: convert prints to ValidationError exception

jadn_schema = {
    "type": "object",
    "required": ["meta", "types"],
    "additionalProperties": False,
    "properties": {
        "meta": {
            "type": "object",
            "required": ["module"],
            "additionalProperties": False,
            "properties": {
                "description": {"type": "string"},
                "import": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "minItems": 3,
                        "maxItems": 3,
                        "items": [
                            {"type": "integer"},
                            {"type": "string"},
                            {"type": "string"}
                        ]
                    }
                },
                "module": {"type": "string"},
                "root": {"type": "string"},
                "namespace": {"type": "string"},
                "title": {"type": "string"},
                "version": {"type": "string"}
            }
        },
        "types": {
            "type": "array",
            "items": {
                "type": "array",
                "minItems": 4,
                "maxItems": 5,
                "items": [
                    {"type": "string"},
                    {"type": "string"},
                    {"type": "array",
                        "items": {"type": "string"}
                    },
                    {"type": "string"},
                    {"type": "array",
                        "items": {
                            "type": "array",
                            "minItems": 3,
                            "maxItems": 5,
                            "items": [
                                {"type": "integer"},
                                {"type": "string"},
                                {"type": "string"},
                                {"type": "array",
                                 "items": {"type": "string"}
                                },
                                {"type": "string"}
                            ]
                        }
                    }
                ]
            }
        }
    }
}

# JADN Type Definition columns      # MUST remain in sync with codec
TNAME = 0       # Datatype name
TTYPE = 1       # Base type
TOPTS = 2       # Type options
TDESC = 3       # Type description
FIELDS = 4      # List of fields

# JADN Field Definition columns
FTAG = 0        # Element ID
FNAME = 1       # Element name
EDESC = 2       # Description (for enumerated types)
FTYPE = 2       # Datatype of field
FOPTS = 3       # Field options
FDESC = 4       # Field Description


def jadn_check(schema):
    """
    Check JADN structure against JSON schema, then perform additional checks on type definitions
    """

    jsonschema.Draft4Validator(jadn_schema).validate(schema)

    for t in schema["types"]:     # datatype definition: 0-name, 1-type, 2-options, 3-description, 4-item list
        if not is_builtin(t[TTYPE]):
            print("Type error: Unknown type", t[TTYPE], "(" + t[TNAME] + ")")       # TODO: handle if t[TNAME] doesn't exist
        if is_primitive(t[TTYPE]):
            if len(t) != 4:    # TODO: trace back to base type
                print("Type format error:", t[TNAME], "- type", t[TTYPE], "cannot have items")
        else:
            if len(t) != 5:
                print("Type format error:", t[TNAME], "- missing items from compound type", t[TTYPE])
        for o, v in opts_s2d(t[2]).items():
            if o not in ["pattern"] and o == "optional" and v:      # "optional" not present when value = False
                print("Invalid typedef option:", t[0], o)
        tags = set()
        if len(t) > 4:
            n = 3 if t[1] == "Enumerated" else 5
            for k, i in enumerate(t[FIELDS]):       # item definition: 0-tag, 1-name, 2-type, 3-options, 4-description
                tags.update(set([i[FTAG]]))         # or (enumerated): 0-tag, 1-name, 2-description
                if t[TTYPE] == "Record" and i[FTAG] != k + 1:
                    print("Item tag error:", t[TTYPE], i[FNAME], i[FTAG], "should be", k + 1)
                if len(i) != n:
                    print("Item format error:", t[TNAME], t[TTYPE], i[FNAME], "-", len(i), "!=", n)
                for o in opts_s2d(i[3]) if n > 3 else []:
                    if o not in ["atfield", "optional", "range"]:
                        print("Invalid field option:", t[TNAME], i[FNAME], o)
# TODO: add check that wildcard name MUST be Choice type, and that only one wildcard is permitted per map/record.
            if len(t[FIELDS]) != len(tags):
                print("Tag collision", t[TNAME], len(t[FIELDS]), "items,", len(tags), "unique tags")
    return schema


def build_jadn_deps(schema):
    items = []
    for tdef in schema["types"]:
        deps = []
        if tdef[TTYPE] == "Array":
            aetype = opts_s2d(tdef[TOPTS])["aetype"]
            if not is_builtin(aetype):
                deps.append(aetype)
        if len(tdef) > FIELDS and tdef[TTYPE] != "Enumerated":
            for f in tdef[FIELDS]:
                if not is_builtin(f[FTYPE]):
                    deps.append(f[FTYPE])
        items.append((tdef[TNAME], deps))
    return items


def jadn_analyze(schema):
    items = build_jadn_deps(schema)
    types = {i[0] for i in items}
    refs = set().union(*[i[1] for i in items])
    print("  module:", schema["meta"]["module"])
    print("  unreferenced:", types - refs)
    print("  undefined:", refs - types)
    print("  cycles:", [])


def jadn_loads(jadn_str):
    schema = json.loads(jadn_str)
    jadn_check(schema)
    return schema


def jadn_load(fname):
    with open(fname) as f:
        schema = json.load(f)
    jadn_check(schema)
    return schema


def jadn_dumps(schema, level=0, indent=1):
    sp = level * indent * " "
    sp2 = (level + 1) * indent * " "
    if isinstance(schema, dict):
        sep = ",\n" if level > 0 else ",\n\n"
        lines = []
        for k in sorted(schema):
            lines.append(sp2 + "\"" + k + "\": " + jadn_dumps(schema[k], level + 1, indent))
        return "{\n" + sep.join(lines) + "\n" + sp + "}"
    elif isinstance(schema, list):
        sep = ",\n" if level > 1 else ",\n\n"
        vals = []
        nest = schema and isinstance(schema[0], list)
        sp4 = ""
        for v in schema:
            sp3 = sp2 if nest else ""
            sp4 = sp if v and isinstance(v, list) else ""
            vals.append(sp3 + jadn_dumps(v, level + 1, indent))
        if nest:
            return "[\n" + sep.join(vals) + "]\n"
        return "[" + ", ".join(vals) + sp4 + "]"
    elif isinstance(schema, (bool, int, str)):
        return json.dumps(schema)
    return "???"


def jadn_dump(schema, fname, source=""):
    with open(fname, "w") as f:
        if source:
            f.write("\"Generated from " + source + ", " + datetime.ctime(datetime.now()) + "\"\n\n")
        f.write(jadn_dumps(schema) + "\n")
