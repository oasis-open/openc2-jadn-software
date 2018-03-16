"""
Abstract Object Encoder/Decoder

Object schema is specified in JSON Abstract Data Notation (JADN) format.

Codec currently supports three JSON concrete message formats (verbose,
concise, and minified) but can be extended to support XML or binary formats.

Copyright 2016 David Kemp
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0
"""

from __future__ import unicode_literals
import base64
from .jadn_defs import *
from .codec_utils import topts_s2d, fopts_s2d

__version__ = "0.2"

# TODO: add DEFAULT
# TODO: use CHOICE with both explicit (attribute) and implicit (wildcard field) type

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
        self.symtab = {}
        self.set_mode(verbose_rec, verbose_str)
        assert set(enctab) == set(PRIMITIVE_TYPES + STRUCTURE_TYPES)
        self.max_array = 100,       # Set conservative upper bounds that can be overridden when necessary
        self.max_string = 255,
        self.max_binary = 32767

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

    def _check_type(self, ts, val, vtype):
        if vtype is not None:
            if type(val) != vtype:
                td = ts[S_TDEF]
                tn = "%s(%s)" % (td[TNAME], td[TTYPE]) if td else "Primitive"
                raise TypeError("%s: %r is not %s" % (tn, val, vtype))

    def _check_field_len(self, ts, val):
        op = ts[S_TOPT]
        if vtype in (list, type('')):
            if len(val) < op['emin']:
                raise ValueError("%s: length %s < minimum %s" % td[TNAME], len(val), omin)
            if len(val) > op['emax']:
                raise ValueError("%s: length %s > maximum %s" % td[TNAME], len(val), omax)

    def set_mode(self, verbose_rec=False, verbose_str=False):
        def symf(fld):              # Field entries
            fs = [
                fld,                # S_FDEF: JADN field definition
                fopts_s2d(fld[FOPTS]) if len(fld) > FOPTS else None,  # S_FOPT: Field options (dict)
                []                  # S_FNAMES: Possible field names returned from Choice type
            ]
            fo = fs[S_FOPT]
            emax = None
            if fld[FTYPE] == list:
                emax = self.max_array
            elif fld[FTYPE] == type(''):
                emax = self.max_string
            emax = fo['max'] if 'max' in fo and fo['max'] > 0 else emax
            emin = fo['min'] if 'min' in fo else 1
            fo.update({'emin': emin, 'emax': emax})
            return fs

        def sym(t):                 # Build symbol table based on encoding modes
            symval = [
                t,                          # 0: S_TDEF:  JADN type definition
                enctab[t[TTYPE]],           # 1: S_CODEC: Decoder, Encoder, Encoded type
                int,                        # 2: S_STYPE: Encoded string type (str or tag)
                topts_s2d(t[TOPTS]),        # 3: S_TOPT:  Type Options (dict)
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
                symval[S_STYPE] = type('')
            if t[TTYPE] == "Enumerated":
                fa = FTAG if "etag" in symval[S_TOPT] else FNAME
                symval[S_DMAP] = {f[fx]: f[fa] for f in t[FIELDS]}
                symval[S_EMAP] = {f[fa]: f[fx] for f in t[FIELDS]}
            if t[TTYPE] in ["Choice", "Map", "Record"]:
                fx = FNAME if verbose_str else FTAG
                symval[S_FLD] = {str(f[fx]): symf(f) for f in t[FIELDS]}
                symval[S_EMAP] = {f[FNAME]: str(f[fx]) for f in t[FIELDS]}
            return symval

        self.symtab = {t[TNAME]: sym(t) for t in self.schema["types"]}
        for t in self.symtab.values():        # TODO: Check for wildcard name collisions
            if t[S_TDEF][TTYPE] in ["Map", "Record"]:
                for f in t[S_FLD].values():
                    if f[S_FDEF][FNAME] == '*':
                        t = self.symtab[f[S_FDEF][FTYPE]][S_TDEF]
                        assert(t[TTYPE] == 'Choice')
                        f[S_FNAMES] = [c[FNAME] for c in t[FIELDS]]

        self.symtab.update({t: [None, enctab[t], enctab[t][C_ETYPE]] for t in
                            ("Binary", "Boolean", "Integer", "Number", "String")})


def _bad_value(ts, val, fld=None):
    td = ts[S_TDEF]
    if fld is not None:
        raise ValueError("%s(%s): missing required field '%s': %s" % (td[TNAME], td[TTYPE], fld[FNAME], val))
    else:
        v = next(iter(val)) if type(val) == dict else val
        raise ValueError("%s(%s): bad value: %s" % (td[TNAME], td[TTYPE], v))


def _extra_value(ts, val, fld):
    td = ts[S_TDEF]
    raise ValueError("%s(%s): unexpected field: %s not in %s:" % (td[TNAME], td[TTYPE], val, fld))


def _decode_array_of(ts, val, codec):
    codec._check_type(ts, val, list)                      # TODO: check min/max array length
    return [codec.decode(ts[S_TOPT]["aetype"], v) for v in val]


def _encode_array_of(ts, val, codec):
    codec._check_type(ts, val, list)
    return [codec.encode(ts[S_TOPT]["aetype"], v) for v in val]


def _decode_binary(ts, val, codec):
    codec._check_type(ts, val, type(''))
    return base64.standard_b64decode(val.encode(encoding="UTF-8"))


def _encode_binary(ts, val, codec):
    codec._check_type(ts, val, bytes)
    return base64.standard_b64encode(val).decode(encoding="UTF-8")


def _decode_boolean(ts, val, codec):
    codec._check_type(ts, val, bool)
    return val


def _encode_boolean(ts, val, codec):
    codec._check_type(ts, val, bool)
    return val


def _decode_choice(ts, val, codec):
    codec._check_type(ts, val, dict)
    k = next(iter(val))
    if len(val) != 1 or k not in ts[S_FLD]:
        _bad_value(ts, val)
    f = ts[S_FLD][k][S_FDEF]
    return {f[FNAME]: codec.decode(f[FTYPE], val[k])}


def _encode_choice(ts, val, codec):         # TODO: bad schema - verify * field has only Choice type
    codec._check_type(ts, val, dict)
    k = next(iter(val))
    if len(val) != 1 or k not in ts[S_EMAP]:
        _bad_value(ts, val)
    f = ts[S_FLD][ts[S_EMAP][k]][S_FDEF]
    fx = f[FNAME] if ts[S_VSTR] else f[FTAG]            # Verbose or Minified identifier strings
    return {str(fx): codec.encode(f[FTYPE], val[k])}


def _decode_enumerated(ts, val, codec):
    codec._check_type(ts, val, ts[S_STYPE])
    if val in ts[S_DMAP]:
        return ts[S_DMAP][val]
    else:
        td = ts[S_TDEF]
        raise ValueError("%s: %r is not a valid %s" % (td[TTYPE], val, td[TNAME]))


def _encode_enumerated(ts, val, codec):
    etype = int if 'etag' in ts[S_TOPT] else type('')
    codec._check_type(ts, val, etype)
    if val in ts[S_EMAP]:
        return ts[S_EMAP][val]
    else:
        td = ts[S_TDEF]
        raise ValueError("%s: %r is not a valid %s" % (td[TTYPE], val, td[TNAME]))


def _decode_integer(ts, val, codec):
    codec._check_type(ts, val, int)
    return val


def _encode_integer(ts, val, codec):
    codec._check_type(ts, val, int)
    return val


def _decode_number(ts, val, codec):
    val = float(val) if type(val) == int else val
    codec._check_type(ts, val, float)
    return val


def _encode_number(ts, val, codec):
    val = float(val) if type(val) == int else val
    codec._check_type(ts, val, float)
    return val


def _decode_maprec(ts, val, codec):
    codec._check_type(ts, val, ts[S_CODEC][C_ETYPE])
    apival = dict()
    fx = FNAME if ts[S_VSTR] else FTAG    # Verbose or minified identifier strings
    fnames = [k for k in ts[S_FLD]]
    for f in ts[S_TDEF][FIELDS]:
        ft = str(f[fx])
        fs = ts[S_FLD][ft]
        fopts = fs[S_FOPT]
        if type(val) == dict:
            fn = next(iter(set(val) & set(fs[S_FNAMES])), None) if f[FNAME] == '*' else ft
            fv = val[fn] if fn in val else None
        else:
            fn = f[FTAG] - 1
            fv = val[fn] if len(val) > fn else None
        if fv:
            ftype = apival[fopts["atfield"]] if "atfield" in fopts else f[FTYPE]
            if f[FNAME] == '*':
                if type(val) == dict:
                    apival.update(codec.decode(ftype, {fn: fv}))
                    fnames.append(fn)
                else:
                    apival.update(codec.decode(ftype, fv))
            else:
                apival[f[FNAME]] = codec.decode(ftype, fv)
        else:
            if "min" not in fopts or fopts["min"] > 0:
                _bad_value(ts, val, f)
    extra = set(val) - set(fnames) if type(val) == dict else len(val) > len(ts[S_FLD])
    if extra:
        _extra_value(ts, val, extra)
    return apival


def _encode_maprec(ts, val, codec):
    codec._check_type(ts, val, dict)
    encval = ts[S_CODEC][C_ETYPE]()
    assert type(encval) in (list, dict)
    fx = FNAME if ts[S_VSTR] else FTAG    # Verbose or minified identifier strings
    fnames = [f[S_FDEF][FNAME] for f in ts[S_FLD].values()]
    for f in ts[S_TDEF][FIELDS]:
        fs = ts[S_FLD][str(f[fx])]
        fopts = fs[S_FOPT]
        ftype = val[fopts["atfield"]] if "atfield" in fopts else f[FTYPE]
        if f[FNAME] == '*':                 # Implicit selector - pull Choice value up to this level
            vn = next(iter(set(val) & set(fs[S_FNAMES])), None)
            fnames.append(vn)
            fv = codec.encode(ftype, {vn: val[vn]}) if vn in val else None
        else:
            vn = f[FNAME]
            fv = codec.encode(ftype, val[vn]) if vn in val else None
        if fv is None and ("min" not in fopts or fopts["min"] > 0):     # Missing required field
            _bad_value(ts, val, f)
        if type(encval) == list:            # Concise Record
            encval.append(fv)
        else:                               # Map or Verbose Record
            if fv is not None:
                if f[FNAME] == '*':
                    encval.update(fv)
                else:
                    encval[str(f[fx])] = fv

    if set(val) - set(fnames):
        _extra_value(ts, val, fnames)
    if type(encval) == list:
        while encval and encval[-1] is None:    # Strip non-populated trailing optional values
            encval.pop()
    return encval


def _decode_array(ts, val, codec):          # Ordered list of types, no names in API
    codec._check_type(ts, val, list)
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
            if fopts["min"] > 0:
                _bad_value(ts, val, f)
    return apival


def _encode_array(ts, val, codec):
    codec._check_type(ts, val, list)
    apival = list()
    extra = len(val) > len(ts[S_FLD])
    if extra:
        _extra_value(ts, val, extra)
    for f in ts[S_TDEF][FIELDS]:
        pass
    return apival


def _decode_null(ts, val, codec):
    codec._check_type(ts, val, type(''))
    if val:
        _bad_value(ts, val)
    return val


def _encode_null(ts, val, codec):
    codec._check_type(ts, val, type(''))
    if val:
        _bad_value(ts, val)
    return val


def _decode_string(ts, val, codec):
    codec._check_type(ts, val, type(''))
    return val


def _encode_string(ts, val, codec):
    codec._check_type(ts, val, type(''))
    return val


def is_primitive(vtype):
    return vtype in PRIMITIVE_TYPES


def is_builtin(vtype):
    return vtype in PRIMITIVE_TYPES + STRUCTURE_TYPES


enctab = {  # decode, encode, min encoded type
    "Binary": (_decode_binary, _encode_binary, str),
    "Boolean": (_decode_boolean, _encode_boolean, bool),
    "Integer": (_decode_integer, _encode_integer, int),
    "Number": (_decode_number, _encode_number, float),
    "Null": (_decode_null, _encode_null, str),
    "String": (_decode_string, _encode_string, str),
    "ArrayOf": (_decode_array_of, _encode_array_of, list),
    "Array": (_decode_array, _encode_array, list),
    "Choice": (_decode_choice, _encode_choice, dict),
    "Enumerated": (_decode_enumerated, _encode_enumerated, int),
    "Map": (_decode_maprec, _encode_maprec, dict),
    "Record": (None, None, None),   # Dynamic values
}
