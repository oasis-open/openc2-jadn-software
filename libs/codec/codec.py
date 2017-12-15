"""
Abstract Object Encoder/Decoder

Object schema is specified in JSON Abstract Data Notation (JADN) format.

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

# JADN Type Definition columns
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

# Codec Table fields
C_DEC = 0       # Decode function
C_ENC = 1       # Encode function
C_ETYPE = 2     # Encoded type

# Symbol Table fields
S_TDEF = 0      # JADN type definition
S_CODEC = 1     # CODEC table entry for this type
S_STYPE = 2     # Encoded identifier type (string or tag)
S_TOPT = 3      # Type Options (dict format)
S_VSTR = 4      # Verbose_str
S_FLD = 5       # Field entries (definition and decoded options)
S_DMAP = 5      # Enum Encoded Val to Name
S_EMAP = 6      # Enum Name to Encoded Val

# Symbol Table Field Definition fields
S_FDEF = 0      # JADN field definition
S_FOPT = 1      # Field Options (dict format)
S_FNAMES = 2    # Possible field names returned from Choice type


class Codec:
    """
    Serialize (encode) and De-serialize (decode) values based on JADN syntax.

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

    def __init__(self, schema, verbose_rec=False, verbose_str=False):
        self.schema = schema
        self.set_mode(verbose_rec, verbose_str)

    def decode(self, datatype, mstr):
        try:
            symtype = self.symtab[datatype]
        except KeyError:
            raise ValueError("datatype '%s' is not defined: %s" % (datatype, mstr))
        return symtype[S_CODEC][C_DEC](symtype, mstr, self)

    def encode(self, datatype, message):
        try:
            symtype = self.symtab[datatype]
        except KeyError:
            raise ValueError("datatype '%s' is not defined: %s" % (datatype, message))
        return symtype[S_CODEC][C_ENC](symtype, message, self)

    def set_mode(self, verbose_rec=False, verbose_str=False):
        def symf(f):        # Field entries
            fs = [
                f,          # S_FDEF: JADN field definition
                opts_s2d(f[FOPTS]) if len(f) > FOPTS else None,  # S_FOPT: Field options (dict)
                []          # S_FNAMES: Possible field names returned from Choice type
            ]
            return fs

        def sym(t):         # Build symbol table based on encoding modes
            symval = [
                t,                          # 0: S_TDEF:  JADN type definition
                enctab[t[TTYPE]],           # 1: S_CODEC: Decoder, Encoder, Encoded type
                int,                        # 2: S_STYPE: Encoded string type (str or tag)
                opts_s2d(t[TOPTS]),         # 3: S_TOPT:  Type Options (dict)
                False,                      # 4: S_VSTR:  Verbose String Identifiers
                {},                         # 5: S_FLD/S_DMAP: Field list / Enum Val to Name
                {}                          # 6: S_EMAP:  Enum Name to Val
            ]
            fx = FTAG
            symval[S_VSTR] = verbose_str
            if t[TTYPE] == "Record":
                (symval[S_CODEC], fx) = ([_decode_maprec, _encode_maprec, dict], FNAME)\
                    if verbose_rec else ([_decode_maprec, _encode_maprec, list], FTAG)
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

        self.symtab = {t[TNAME]: sym(t) for t in self.schema["types"]}
        for n, t in self.symtab.items():
            if t[S_TDEF][TTYPE] in ["Map", "Record"]:
                for n, f in t[S_FLD].items():
                    if f[S_FDEF][FNAME] == '*':
                        t = self.symtab[f[S_FDEF][FTYPE]][S_TDEF]
                        assert(t[TTYPE] == 'Choice')
                        f[S_FNAMES] = [c[FNAME] for c in t[FIELDS]]

        self.symtab.update({t: [None, enctab[t], enctab[t][C_ETYPE]] for t in ("Binary", "Boolean", "Integer", "Number", "String")})


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


def _abort(ts, val, msg):
    raise Error(msg)


def _decode_array_of(ts, val, codec):              # TODO: refactor into array and array_of
    _check_type(ts, val, list)                  # TODO: check min/max array length
    vtype = ts[S_TOPT]["aetype"]
    return [codec.decode(vtype, v) for v in val]


def _encode_array_of(ts, val, codec):
    _check_type(ts, val, list)
    vtype = ts[S_TOPT]["aetype"]
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


def _encode_choice(ts, val, codec):         # TODO: bad schema - verify * field has only Choice type
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
    _check_type(ts, val, ts[S_CODEC][C_ETYPE])
    apival = dict()
    extra = set(val) - set(ts[S_FLD]) if type(val) == dict else len(val) > len(ts[S_FLD])
    if extra:
        _extra_value(ts, val, extra)
    for f in ts[S_TDEF][FIELDS]:
        fs = f[FNAME] if ts[S_VSTR] else str(f[FTAG])  # Verbose or Minified identifier strings
        fopts = ts[S_FLD][fs][S_FOPT]
        if type(val) == dict:
            fx = fs
            exists = fx in val and val[fx] is not None
        else:
            fx = f[FTAG] - 1
            exists = len(val) > fx and val[fx] is not None
        if exists:
            ftype = apival[fopts["atfield"]] if "atfield" in fopts else f[FTYPE]
            apival[f[FNAME]] = codec.decode(ftype, val[fx])
        else:
            if not fopts["optional"]:
                _bad_value(ts, val, f)
    return apival


def _encode_maprec(ts, val, codec):
    _check_type(ts, val, dict)
    encval = ts[S_CODEC][C_ETYPE]()
    fx = FNAME if ts[S_VSTR] else FTAG    # Verbose or minified identifier strings
    if type(encval) == list:
        fmax = max([ts[S_FLD][ts[S_EMAP][f]][S_FDEF][FTAG] for f in val])
    for f in ts[S_TDEF][FIELDS]:
        fopts = ts[S_FLD][str(f[fx])][S_FOPT]
        ftype = val[fopts["atfield"]] if "atfield" in fopts else f[FTYPE]
        if f[FNAME] == '*':
            fnames = ts[S_CNAMES]
        fv = codec.encode(ftype, val[f[FNAME]]) if f[FNAME] in val else None
        if fv is None and not fopts["optional"]:     # Missing required field
            _bad_value(ts, val, f)
        if type(encval) == list:            # Concise Record
            if f[FTAG] <= fmax:
                encval.append(fv)
        elif type(encval) == dict:          # Map or Verbose Record
            if fv is not None:
                encval[str(f[fx])] = fv
        else:
            _abort(ts, val, 'Internal error, bad type')
    fnames = [f[S_FDEF][FNAME] for k, f in ts[S_FLD].items()]
    if set(val) - set(fnames):
        _extra_value(ts, val, fnames)
    return encval


def _decode_array(ts, val, codec):          # Ordered list of types, no names in API
    _check_type(ts, val, list)
    apival = list()
    extra = len(val) > len(ts[S_FLD])
    if extra:
        _extra_value(ts, val, extra)
    for f in ts[S_TDEF][FIELDS]:
        fopts = ts[S_FLD][str(f[FTAG])][S_FOPT]
        fx = f[FTAG] - 1
        av = val[fx] if len(val) > fx else None
        if av is not None:
            ftype = apival[fopts["atfield"]] if "atfield" in fopts else f[FTYPE]
            apival.append(codec.decode(ftype, av))
        else:
            apival.append(None)
            if not fopts["optional"]:
                _bad_value(ts, val, f)
    return apival


def _encode_array(ts, val, codec):
    _check_type(ts, val, list)
    apival = list()
    extra = len(val) > len(ts[S_FLD])
    if extra:
        _extra_value(ts, val, extra)
    for f in ts[S_TDEF][FIELDS]:
        pass
    return apival


def _decode_string(ts, val, codec):
    _check_type(ts, val, str)
    return val


def _encode_string(ts, val, codec):
    _check_type(ts, val, str)
    return val


def is_primitive(vtype):
    if is_builtin(vtype):
        return vtype in ["ArrayOf", "Binary", "Boolean", "Integer", "Number", "String"]
    return False


def is_builtin(vtype):
    return vtype in enctab


enctab = {  # decode, encode, min encoded type
    "Binary": (_decode_binary, _encode_binary, str),
    "Boolean": (_decode_boolean, _encode_boolean, bool),
    "Integer": (_decode_integer, _encode_integer, int),
    "Number": (_decode_number, _encode_number, float),
    "String": (_decode_string, _encode_string, str),
    "ArrayOf": (_decode_array_of, _encode_array_of, list),
    "Array": (_decode_array, _encode_array, list),
    "Choice": (_decode_choice, _encode_choice, dict),
    "Enumerated": (_decode_enumerated, _encode_enumerated, int),
    "Map": (_decode_maprec, _encode_maprec, dict),
    "Record": (None, None, None),   # Dynamic values
}
