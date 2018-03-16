"""
Load, validate, prettyprint, and dump JSON Abstract Encoding Notation (JADN) schemas
"""

from __future__ import print_function

import json
import jsonschema
from datetime import datetime
from .codec import is_builtin, is_primitive
from .codec_utils import topts_s2d, fopts_s2d
from .jadn_defs import *

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


def jadn_check(schema):
    """
    Check JADN structure against JSON schema, then perform additional checks on type definitions
    """

    valid_topts = {
        'Binary': [],
        'Boolean': [],
        'Integer': ['min', 'max'],
        'Number': ['min', 'max'],
        'String': ['min', 'max', 'pattern', 'format'],
        'Array': ['min', 'max'],
        'ArrayOf': ['min', 'max', 'aetype'],
        'Choice': [],
        'Enumerated': ['etag'],
        'Map': [],
        'Record': [],
    }
    valid_fopts = {
        "Array": ['min', 'max', 'etype'],
        "Choice": [],
        "Enumerated": [],
        "Map": ['min', 'max', 'etype'],
        "Record": ['min', 'max', 'etype', 'atfield'],
    }

    jsonschema.Draft4Validator(jadn_schema).validate(schema)

    for t in schema["types"]:     # datatype definition: 0-name, 1-type, 2-options, 3-description, 4-item list
        if not is_builtin(t[TTYPE]):
            print("Type error: Unknown type", t[TTYPE], "(" + t[TNAME] + ")")       # TODO: handle if t[TNAME] doesn't exist
        vop = {k for k in topts_s2d(t[TOPTS])} - {k for k in valid_topts[t[TTYPE]]}
        if vop:
            print("Error:", t[TNAME], "type", t[TTYPE], "invalid option", str(vop))
        if is_primitive(t[TTYPE]) or t[TTYPE] == 'ArrayOf':
            if len(t) != 4:    # TODO: trace back to base type
                print("Type format error:", t[TNAME], "- type", t[TTYPE], "cannot have items")
        else:
            if len(t) != 5:
                print("Type format error:", t[TNAME], "- missing items from compound type", t[TTYPE])
            else:
                tags = set()
                n = 3 if t[1] == "Enumerated" else 5
                for k, i in enumerate(t[FIELDS]):       # item definition: 0-tag, 1-name, 2-type, 3-options, 4-description
                    tags.update(set([i[FTAG]]))         # or (enumerated): 0-tag, 1-name, 2-description
                    if t[TTYPE] == "Record" and i[FTAG] != k + 1:
                        print("Item tag error:", t[TTYPE], i[FNAME], i[FTAG], "should be", k + 1)
                    if len(i) != n:
                        print("Item format error:", t[TNAME], t[TTYPE], i[FNAME], "-", len(i), "!=", n)
                    if len(i) > 3:
                        fop = {k for k in fopts_s2d(i[FOPTS])} - {k for k in valid_fopts[t[TTYPE]]}
                        if fop:
                            print("Error:", t[TNAME], "field", i[FNAME], i[FTYPE], "invalid option", str(fop))
    # TODO: add check that wildcard name MUST be Choice type, and that only one wildcard is permitted per map/record.
                if len(t[FIELDS]) != len(tags):
                    print("Tag collision", t[TNAME], len(t[FIELDS]), "items,", len(tags), "unique tags")
    return schema

def topo_sort(items):
    """
    Topological sort with locality
    Sorts a list of (item: (dependencies)) pairs so that 1) all dependency items are listed before the parent item,
    and 2) dependencies are listed in the given order and as close to the parent as possible.
    Returns the sorted list of items and a list of root items.  A single root indicates a fully-connected hierarchy;
    multiple roots indicate disconnected items or hierarchies, and no roots indicate a dependency cycle.
    """
    def walk_tree(item):
        for i in deps[item]:
            if i not in out:
                walk_tree(i)
                out.append(i)

    out = []
    deps = {i[0]:i[1] for i in items}
    roots = {i[0] for i in items} - set().union(*[i[1] for i in items])
    for item in roots:
        walk_tree(item)
        out.append(item)
    out = out if out else [i[0] for i in items]     # if cycle detected, don't sort
    return out, roots


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
#    out, roots = topo_sort(items)
    types = {i[0] for i in items}
    refs = set().union(*[i[1] for i in items])
    version = ", " + schema['meta']['version'] if 'version' in schema['meta'] else ''
    print("  module:", schema["meta"]["module"] + version)
    print("  unreferenced:", [str(k) for k in types - refs])
    print("  undefined:", [str(k) for k in refs - types])
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
    elif isinstance(schema, (bool, int, type(""))):
        return json.dumps(schema)
    return "???"


def jadn_dump(schema, fname, source=""):
    with open(fname, "w") as f:
        if source:
            f.write("\"Generated from " + source + ", " + datetime.ctime(datetime.now()) + "\"\n\n")
        f.write(jadn_dumps(schema) + "\n")
