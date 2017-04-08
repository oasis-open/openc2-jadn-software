"""
Abstract Object Encoder/Decoder

Object schema is specified in JSON Abstract Encoding Notation (JAEN) format.

Codec currently supports three JSON concrete message formats (verbose,
concise, and minified) but can be extended to support XML or binary formats.

Copyright 2016 David Kemp
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0
"""

import base64
from .codec_utils import opts_s2d

__version__ = "0.2"

# TODO: add DEFAULT
# TODO: use CHOICE with both explicit (attribute) and implicit (wildcard field) type

# JAEN Type Definition columns
TNAME = 0       # Datatype name
TTYPE = 1       # Base type
TOPTS = 2       # Type options
TDESC = 3       # Type description
FIELDS = 4      # List of fields

# JAEN Field Definition columns
FTAG = 0        # Element ID
FNAME = 1       # Element name
EDESC = 2       # Description (for enumerated types)
FTYPE = 2       # Datatype of field
FOPTS = 3       # Field options
FDESC = 4       # Field Description

# Codec Table fields
C_DEC = 0       # Decode function
C_ENC = 1       # Encode function
C_ETYPE = 2     # Encoded type (for min encoding)

# Symbol Table fields
S_TDEF = 0      # JAEN type definition
S_CODEC = 1     # CODEC table entry for this type
S_ETYPE = 2     # Encoded type (current encoding mode)
S_STYPE = 3     # Encoded identifier type (string or tag)
S_TOPT = 4      # Type Options (dict format)
S_VSTR = 5      # Verbose_str
S_FLD = 6       # Field entries (definition and decoded options)
S_DMAP = 6      # Enum Encoded Val to Name
S_EMAP = 7      # Enum Name to Encoded Val

# Symbol Table Field Definition fields
S_FDEF = 0      # JAEN field definition
S_FOPT = 1      # Field Options (dict format)


class Codec:
    """
    Serialize (encode) and De-serialize (decode) values based on JAEN syntax.

    verbose_rec - True: Record types encoded as JSON objects
                 False: Record types encoded as JSON arrays
    verbose_str - True: Identifiers encoded as JSON strings
                 False: Identifiers encoded as JSON integers (tags)

    Encoding modes: rec,   str     Record Encoding
    --------------  -----  -----  -----------
        "Verbose" = True,  True    Dict, Name
        "Concise" = False, True    List, Name
       "Minified" = False, False   List, Tag
         not used = True,  False   Dict, Tag
    """

    def __init__(self, jaen, verbose_rec=False, verbose_str=False):
        self.jaen = jaen
        self.set_mode(verbose_rec, verbose_str)

    def decode(self, datatype, mstr):
        symtype = self.symtab[datatype]
        return symtype[S_CODEC][C_DEC](symtype, mstr, self)

    def encode(self, datatype, message):
        symtype = self.symtab[datatype]
        return symtype[S_CODEC][C_ENC](symtype, message, self)

    def set_mode(self, verbose_rec=False, verbose_str=False):
        def symf(f):        # Field entries
            fs = [
                f,          # S_FDEF:  JAEN field definition
                opts_s2d(f[FOPTS]) if len(f) > FOPTS else None  # S_FOPT: Field options (dict)
            ]
            return fs

        def sym(t):         # Build symbol table based on encoding modes
            symval = [
                t,                          # 0: S_TDEF:  JAEN type definition
                enctab[t[TTYPE]],           # 1: S_CODEC: Type decode function
                enctab[t[TTYPE]][C_ETYPE],  # 2: S_ETYPE: Encoded type
                int,                        # 3: S_STYPE: Encoded string type (str or tag)
                opts_s2d(t[TOPTS]),         # 4: S_TOPT:  Type Options (dict)
                False,                      # 5: S_VSTR:  Verbose String Identifiers
                {},                         # 6: S_FLD/S_DMAP: Field list / Enum Val to Name
                {}                          # 7: S_EMAP:  Enum Name to Val
            ]
            fx = FTAG
            symval[S_VSTR] = verbose_str
            if t[TTYPE] == "Record":
                (fx, symval[S_ETYPE]) = (FNAME, dict) if verbose_rec else (FTAG, list)
            if verbose_str and t[TTYPE] in ["Choice", "Enumerated", "Map"]:
                fx = FNAME
                symval[S_STYPE] = str
            if t[TTYPE] == "Enumerated":
                symval[S_DMAP] = {f[fx]: f[FNAME] for f in t[FIELDS]}
                symval[S_EMAP] = {f[FNAME]: f[fx] for f in t[FIELDS]}
            if t[TTYPE] in ["Choice", "Map", "Record"]:
                fx = FNAME if verbose_str else FTAG
                symval[S_FLD] = {str(f[fx]): symf(f) for f in t[FIELDS]}
                symval[S_EMAP] = {f[FNAME]: str(f[fx]) for f in t[FIELDS]}
            return symval
        self.symtab = {t[TNAME]: sym(t) for t in self.jaen["types"]}
        self.symtab.update({t: [None, enctab[t], enctab[t][C_ETYPE]] for t in ("Boolean", "Integer", "Number", "String")})


def _check_type(ts, val, vtype):
    td = ts[S_TDEF]
    if vtype is not None:
        if type(val) != vtype:
            if td:
                raise TypeError("%s(%s): %r is not %s" % (td[TNAME], td[TTYPE], val, vtype))
            else:
                raise TypeError("Primitive: %r is not %s" % (val, vtype))


def _bad_value(ts, val, fld=None):
    td = ts[S_TDEF]
    if fld is not None:
        raise ValueError("%s(%s): missing required field '%s': %s" % (td[TNAME], td[TTYPE], fld[FNAME], val))
    else:
        raise ValueError("%s(%s): bad value: %s" % (td[TNAME], td[TTYPE], val))


def _extra_value(ts, val, fld):
    td = ts[S_TDEF]
    raise ValueError("%s(%s): unexpected field: %s not in %s:" % (td[TNAME], td[TTYPE], val, fld))


def _decode_array(ts, val, codec):
    _check_type(ts, val, list)                  # TODO: check min/max array length
    vtype = ts[S_TDEF][FIELDS][0][FTYPE]
    return [codec.decode(vtype, v) for v in val]


def _encode_array(ts, val, codec):
    _check_type(ts, val, list)
    vtype = ts[S_TDEF][FIELDS][0][FTYPE]
    return [codec.encode(vtype, v) for v in val]


def _decode_binary(ts, val, codec):
    _check_type(ts, val, str)
    return base64.b64decode(val.encode(encoding="UTF-8"), validate=True)


def _encode_binary(ts, val, codec):
    _check_type(ts, val, bytes)
    return base64.b64encode(val).decode(encoding="UTF-8")


def _decode_boolean(ts, val, codec):
    _check_type(ts, val, bool)
    return val


def _encode_boolean(ts, val, codec):
    _check_type(ts, val, bool)
    return val


def _decode_choice(ts, val, codec):
    _check_type(ts, val, dict)
    k = next(iter(val))
    if len(val) != 1 or k not in ts[S_FLD]:
        _bad_value(ts, val)
    f = ts[S_FLD][k][S_FDEF]
    return {f[FNAME]: codec.decode(f[FTYPE], val[k])}


def _encode_choice(ts, val, codec):
    _check_type(ts, val, dict)
    k = next(iter(val))
    if len(val) != 1 or k not in ts[S_EMAP]:
        _bad_value(ts, val)
    f = ts[S_FLD][ts[S_EMAP][k]][S_FDEF]
    fx = f[FNAME] if ts[S_VSTR] else f[FTAG]            # Verbose or Minified identifier strings
    return {str(fx): codec.encode(f[FTYPE], val[k])}


def _decode_enumerated(ts, val, codec):
    _check_type(ts, val, ts[S_STYPE])
    if val in ts[S_DMAP]:
        return ts[S_DMAP][val]
    else:
        td = ts[S_TDEF]
        raise ValueError("%s: %r is not a valid %s" % (td[TTYPE], val, td[TNAME]))


def _encode_enumerated(ts, val, codec):
    _check_type(ts, val, str)
    if val in ts[S_EMAP]:
        return ts[S_EMAP][val]
    else:
        td = ts[S_TDEF]
        raise ValueError("%s: %r is not a valid %s" % (td[TTYPE], val, td[TNAME]))


def _decode_integer(ts, val, codec):
    _check_type(ts, val, int)
    return val


def _encode_integer(ts, val, codec):
    _check_type(ts, val, int)
    return val


def _decode_number(ts, val, codec):
    val = float(val) if type(val) == int else val
    _check_type(ts, val, float)
    return val


def _encode_number(ts, val, codec):
    val = float(val) if type(val) == int else val
    _check_type(ts, val, float)
    return val


def _decode_maprec(ts, val, codec):
    _check_type(ts, val, ts[S_ETYPE])
    apival = dict()                                 # API returns dict for Map and Record
    if ts[S_ETYPE] == list:
        extra = len(val) > len(ts[S_FLD])
    else:
        extra = set(val) - set(ts[S_FLD])
    if extra:
        _extra_value(ts, val, extra)
    for f in ts[S_TDEF][FIELDS]:
        if ts[S_ETYPE] == list:                     # Concise or Minified Record
            fx = f[FTAG] - 1
            exists = len(val) > fx and val[fx] is not None
        else:                                       # Map or Verbose Record
            fx = f[FNAME] if ts[S_VSTR] else str(f[FTAG])  # Verbose or Minified identifier strings
            exists = fx in val and val[fx] is not None
        if exists:
            apival[f[FNAME]] = codec.decode(f[FTYPE], val[fx])
        else:
            fs = f[FNAME] if ts[S_VSTR] else str(f[FTAG])  # Verbose or Minified identifier strings
            if not ts[S_FLD][fs][S_FOPT]["optional"]:
                _bad_value(ts, val, f)
    return apival


def _encode_maprec(ts, val, codec):
    _check_type(ts, val, dict)
    encval = ts[S_ETYPE]()
    fnames = [f[S_FDEF][FNAME] for k, f in ts[S_FLD].items()]
    extra = set(val) - set(fnames)
    if extra:
        _extra_value(ts, val, fnames)
    fx = FNAME if ts[S_VSTR] else FTAG    # Verbose or minified identifier strings
    if ts[S_ETYPE] == list:
        fmax = max([ts[S_FLD][ts[S_EMAP][f]][S_FDEF][FTAG] for f in val])
    for f in ts[S_TDEF][FIELDS]:
        fv = codec.encode(f[FTYPE], val[f[FNAME]]) if f[FNAME] in val else None
        if fv is None and not ts[S_FLD][str(f[fx])][S_FOPT]["optional"]:     # Missing required field
            _bad_value(ts, val, f)
        if ts[S_ETYPE] == list:         # Concise Record
            if f[FTAG] <= fmax:
                encval.append(fv)
        else:                           # Map or Verbose Record
            if fv is not None:
                encval[str(f[fx])] = fv
    return encval


def _decode_string(ts, val, codec):
    _check_type(ts, val, str)
    return val


def _encode_string(ts, val, codec):
    _check_type(ts, val, str)
    return val


def is_primitive(vtype):
    return vtype in "Binary", "Boolean", "Integer", "Number", "String"


def is_builtin(vtype):
    return vtype in enctab

enctab = {  # decode, encode, min encoded type
    "Binary": [_decode_binary, _encode_binary, str],
    "Boolean": [_decode_boolean, _encode_boolean, bool],
    "Integer": [_decode_integer, _encode_integer, int],
    "Number": [_decode_number, _encode_number, float],
    "String": [_decode_string, _encode_string, str],
    "Array": [_decode_array, _encode_array, list],
    "Choice": [_decode_choice, _encode_choice, dict],
    "Enumerated": [_decode_enumerated, _encode_enumerated, int],
    "Map": [_decode_maprec, _encode_maprec, dict],
    "Record": [_decode_maprec, _encode_maprec, dict],   # verbose:dict, concise:list, min:dict
}
