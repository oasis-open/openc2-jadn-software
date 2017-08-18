"""
Translate JADN to and from JAS (JADN Abstract Syntax)
"""

import re
from .jas_parse import jasParser
from ..codec.codec import is_primitive
from ..codec.codec_utils import opts_s2d, opts_d2s
from copy import deepcopy
from datetime import datetime
from textwrap import fill

# JADN Type Definition columns (MUST remain in sync with codec).
TNAME = 0       # Datatype name
TTYPE = 1       # Base type
TOPTS = 2       # Type options
TDESC = 3       # Type description
FIELDS = 4      # List of fields

# JADN Field Definition columns
TAG = 0         # Element ID
NAME = 1        # Element name
EDESC = 2       # Description (for enumerated types)
FTYPE = 2       # Datatype of field
FOPTS = 3       # Field options
FDESC = 4       # Field Description

class Jastype:

    def __init__(self):
        types = [
            ("Binary", "BINARY"),           # OCTET STRING
            ("Boolean", "BOOLEAN"),         # BOOLEAN
            ("Integer", "INTEGER"),         # INTEGER
            ("Number", "REAL"),             # REAL
            ("String", "STRING"),           # UTF8String
            ("Array", "ARRAY_OF"),          # SEQUENCE OF
            ("Choice", "CHOICE"),           # CHOICE
            ("Enumerated", "ENUMERATED"),   # ENUMERATED
            ("Map", "MAP"),                 # SET
            ("Record", "RECORD")            # SEQUENCE
        ]
        self._ptype = {t[0]: t[1] for t in types}
        self._jtype = {t[1]: t[0] for t in types}

    def ptype(self, jt):            # Convert to source (JAS) type
        return self._ptype[jt] if jt in self._ptype else jt

    def jtype(self, pt):            # Convert to JADN type
        return self._jtype[pt] if pt in self._jtype else pt


def _parse_import(import_str):
    tag, ns, uid = re.match("(\d+),\s*(\w+),\s*(.+)$", import_str).groups()
    return [int(tag), ns, uid]


def _nstr(v):       # Return empty string if None
    return v if v else ""

def _topts(v):
    pt = Jastype()
    opts = {}
    for o in v if v else []:
        if isinstance(o, list) and o[0] == "PATTERN":
            opts.update({"pattern": "".join(o[1])})
        elif isinstance(o, str):              # TODO: do better checking that type=Array goes with topts=#aetype
            opts.update({"aetype": pt.jtype(o)})
        else:
            print("Unknown type option", o, v)
    return opts_d2s(opts)

def _fopts(v):      # TODO: process min/max/range option
    opts = {}
    for o in v if v else []:
        if isinstance(o, str) and o.lower() == "optional":
            opts.update({"optional": True})
        elif isinstance(o, list) and o[0] == ".&":
            opts.update({"atfield": o[1]})
        else:
            print("Unknown field option", o, v)
    return opts_d2s(opts)


def jas_loads(jas_str):
    """
    Load abstract syntax from JAS file
    """

    parser = jasParser(parseinfo=True, )

    ast = parser.parse(jas_str, 'jas', trace=False)
    meta = {}
    for m in ast["metas"]:
        k = m["key"]
        if k.lower() == "import":
            meta[k] = [[int(x), y.strip(), z.strip()] for x, y, z in (s.split(",") for s in m["val"])]
        else:
            meta[k] = " ".join(m["val"])

    pt = Jastype()
    types = []
    for t in ast["types"]:
        fields = []
        tdesc = t["td1"]
        topts = t["topts"]
        if t["f"]:
            tdesc = t["f"]["td2"] if t["f"]["td2"] else tdesc
            tf = t["f"]["fields"]
            for n in range(len(tf)-1):          # shift field descriptions up to corresponding fields
                tf[n]["fd2"] = tf[n+1]["fd1"]
            for n, f in enumerate(t["f"]["fields"]):
                fdesc = f["fd2"]
                tag = None
                if t["type"].lower() == "record":
                    tag = n + 1
                elif isinstance(f["tag"], str):
                    tag = int(f["tag"])
                else:
                    print("Error: missing tag", t["name"], f["name"])   # TODO: make all errors exceptions
                if tag is not None:
                    if t["type"].lower() == "enumerated":
                        fields.append([tag, f["name"], _nstr(fdesc)])
                    else:
                        fields.append([tag, f["name"], pt.jtype(f["type"]), _fopts(f["fopts"]), _nstr(fdesc)])
        tdef = [t["name"], pt.jtype(t["type"]), _topts(topts), _nstr(tdesc)]
        types.append(tdef if is_primitive(tdef[1]) else tdef + [fields] )
    jadn = {"meta": meta, "types": types}
    return jadn


def jas_load(fname):
    with open(fname) as f:
        return jas_loads(f.read())


def jas_dumps(jadn):
    """
    Produce JAS module from JADN structure

    JAS represents features available in both jadn and ASN.1 using ASN.1 syntax, but creates
    extended datatypes (Record, Map, Attribute) for JADN types not directly representable in ASN.1.
    With appropriate encoding rules (which do not yet exist), SEQUENCE could replace Record.  Map and
    Attribute could be implemented using ASN.1 table constraints, but for the purpose of representing
    JSON objects, the Map and Attribute first-class types in JAS are easier to use.
    """

    jas = "/*\n"
    hdrs = jadn["meta"]
    hdr_list = ["module", "title", "version", "description", "namespace", "root", "import"]
    for h in hdr_list + list(set(hdrs) - set(hdr_list)):
        if h in hdrs:
            if h == "description":
                jas += fill(hdrs[h], width=80, initial_indent="{0:14} ".format(h+":"), subsequent_indent=15*" ") + "\n"
            elif h == "import":
                hh = "{:14} ".format(h+":")
                for imp in hdrs[h]:
                    jas += hh + "{0:d}, {1}, {2}\n".format(*imp)
                    hh = 15*" "
            else:
                jas += "{0:14} {1:}\n".format(h+":", hdrs[h])
    jas += "*/\n"

    pt = Jastype()
    for td in jadn["types"]:                    # 0:type name, 1:base type, 2:type opts, 3:type desc, 4:fields
        tname, ttype = td[TNAME:TTYPE+1]
        topts = opts_s2d(td[TOPTS])
        if "pattern" in topts:
            tostr = '(PATTERN "' + topts["pattern"] + '")'
        elif "aetype" in topts:
            tostr = '(' + pt.ptype(topts["aetype"]) + ')'
        else:
            tostr = ""
        tdesc = "    -- " + td[TDESC] if td[TDESC] else ""
        jas += "\n" + tname + " ::= " + pt.ptype(ttype) + tostr
        if len(td) > FIELDS:
            titems = deepcopy(td[FIELDS])
            for n, i in enumerate(titems):      # 0:tag, 1:enum item name, 2:enum item desc  (enumerated), or
                if len(i) > FOPTS:              # 0:tag, 1:field name, 2:field type, 3: field opts, 4:field desc
                    desc = i[FDESC]
                    i[FTYPE] = pt.ptype(i[FTYPE])
                else:
                    desc = i[EDESC]
                desc = "    -- " + desc if desc else ""
                i.append("," + desc if n < len(titems) - 1 else (" " + desc if desc else ""))   # TODO: fix hacked desc for join
            flen = min(32, max(12, max([len(i[NAME]) for i in titems]) + 1 if titems else 0))
            jas += " {" + tdesc + "\n"
            if ttype.lower() == "enumerated":
                fmt = "    {1:" + str(flen) + "} ({0:d}){3}"
                jas += "\n".join([fmt.format(*i) for i in titems])
            else:
                fmt = "    {1:" + str(flen) + "} [{0:d}] {2}{3}{4}"
                if ttype.lower() == 'record':
                    fmt = "    {1:" + str(flen) + "} {2}{3}{4}"
                items = []
                for n, i in enumerate(titems):
                    ostr = ""
                    opts = opts_s2d(i[FOPTS])
                    if len(opts) > 1:
                        pass        # debugging multiple opts
                    if "atfield" in opts:
                        ostr += ".&" + opts["atfield"]
                        del opts["atfield"]
                    if opts["optional"]:
                        ostr += " OPTIONAL"
                    del opts["optional"]
                    items += [fmt.format(i[TAG], i[NAME], i[FTYPE], ostr, i[5]) + (" ***" + str(opts) if opts else "")]
                jas += "\n".join(items)
            jas += "\n}\n" if titems else "}\n"
        else:
            jas += tdesc + "\n"
    return jas


def jas_dump(jadn, fname, source=""):
    with open(fname, "w") as f:
        if source:
            f.write("-- Generated from " + source + ", " + datetime.ctime(datetime.now()) + "\n\n")
        f.write(jas_dumps(jadn))
