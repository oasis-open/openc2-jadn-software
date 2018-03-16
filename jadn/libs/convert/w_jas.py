"""
Translate JADN to JAS (JADN Abstract Syntax)
"""

from ..codec.jadn_defs import *
from ..codec.codec_utils import topts_s2d, fopts_s2d
from copy import deepcopy
from datetime import datetime
from textwrap import fill

stype_map = {                   # Map JADN built-in types to JAS type names
    "Binary": "BINARY",           # OCTET STRING
    "Boolean": "BOOLEAN",         # BOOLEAN
    "Integer": "INTEGER",         # INTEGER
    "Number": "REAL",             # REAL
    "Null": "NULL",               # NULL
    "String": "STRING",           # UTF8String
    "Array": "ARRAY",             # SEQUENCE
    "ArrayOf": "ARRAY_OF",        # SEQUENCE OF
    "Choice": "CHOICE",           # CHOICE
    "Enumerated": "ENUMERATED",   # ENUMERATED
    "Map": "MAP",                 # SET
    "Record": "RECORD"            # SEQUENCE
}

def stype(jtype):
    return stype_map[jtype] if jtype in stype_map else jtype

def jas_dumps(jadn):
    """
    Produce JAS module from JADN structure

    JAS represents features available in both JADN and ASN.1 using ASN.1 syntax, but adds
    extended datatypes (Record, Map) for JADN types not directly representable in ASN.1.
    With appropriate encoding rules (which do not yet exist), SEQUENCE could replace Record.
    Map could be implemented using ASN.1 table constraints, but for the purpose of representing
    JSON objects, the Map first-class type in JAS is easier to use.
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

    assert set(stype_map) == set(PRIMITIVE_TYPES + STRUCTURE_TYPES)         # Ensure type list is up to date
    for td in jadn["types"]:                    # 0:type name, 1:base type, 2:type opts, 3:type desc, 4:fields
        tname, ttype = td[TNAME:TTYPE+1]
        topts = topts_s2d(td[TOPTS])
        if "pattern" in topts:
            tostr = '(PATTERN "' + topts["pattern"] + '")'
        elif "aetype" in topts:
            tostr = '(' + stype(topts["aetype"]) + ')'
        else:
            tostr = ""
        tdesc = "    -- " + td[TDESC] if td[TDESC] else ""
        jas += "\n" + tname + " ::= " + stype(ttype) + tostr
        if len(td) > FIELDS:
            titems = deepcopy(td[FIELDS])
            for n, i in enumerate(titems):      # 0:tag, 1:enum item name, 2:enum item desc  (enumerated), or
                if len(i) > FOPTS:              # 0:tag, 1:field name, 2:field type, 3: field opts, 4:field desc
                    desc = i[FDESC]
                    i[FTYPE] = stype(i[FTYPE])
                else:
                    desc = i[EDESC]
                desc = "    -- " + desc if desc else ""
                i.append("," + desc if n < len(titems) - 1 else (" " + desc if desc else ""))   # TODO: fix hacked desc for join
            flen = min(32, max(12, max([len(i[FNAME]) for i in titems]) + 1 if titems else 0))
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
                    opts = fopts_s2d(i[FOPTS])
                    if len(opts) > 1:
                        pass        # debugging multiple opts
                    if "atfield" in opts:
                        ostr += ".&" + opts["atfield"]
                        del opts["atfield"]
                    if "min" in opts:
                        if opts["min"] == 0:         # TODO: handle array fields (max != 1)
                            ostr += " OPTIONAL"
                        del opts["min"]
                    items += [fmt.format(i[FTAG], i[FNAME], i[FTYPE], ostr, i[5]) + (" ***" + str(opts) if opts else "")]
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
