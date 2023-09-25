"""
Translate JADN to XML Abstract Schema Definition (XASD) format
"""
import json

from lxml import etree
from datetime import datetime
from typing import NoReturn, TextIO, Tuple, Union
from ..core import check


def xasd_style() -> dict:
    # Return default column positions
    return {}


def xasd_dumps(schema: dict, style: dict = None) -> str:
    """
    Convert JADN schema to XASD
    """
    w = xasd_style()
    if style:
        w.update(style)   # Override any specified column widths

    xasd = etree.Element("xasd")
    if 'info' in schema:
        xasd.append(etree.Element('Info'))
    xasd.append(etree.Element('Types'))
    """
    info = schema['info'] if 'info' in schema else {}
    mlist = [k for k in INFO_ORDER if k in info]
    for k in mlist + list(set(info) - set(mlist)):              # Display info elements in fixed order
        text += f'{k:>{w["info"]}}: {json.dumps(info[k])}\n'    # TODO: wrap to page width, continuation-line parser

    wt = w['desc'] if w['desc'] else w['id'] + w['name'] + w['type']
    for td in schema['types']:
        tdef = f'{td[TypeName]} = {jadn2typestr(td[BaseType], td[TypeOptions])}'
        tdesc = ' // ' + td[TypeDesc] if td[TypeDesc] else ''
        text += f'\n{tdef:<{wt}}{tdesc}'[:w['page']].rstrip() + '\n'
        idt = td[BaseType] == 'Array' or get_optx(td[TypeOptions], 'id') is not None
        for fd in td[Fields] if len(td) > Fields else []:       # TODO: constant-length types
            fname, fdef, fmult, fdesc = jadn2fielddef(fd, td)
            if td[BaseType] == 'Enumerated':
                fdesc = ' // ' + fdesc if fdesc else ''
                fs = f'{fd[ItemID]:>{w["id"]}} {fname}'
                wf = w['id'] + w['name'] + 2
            else:
                fdef += '' if fmult == '1' else ' optional' if fmult == '0..1' else ' [' + fmult + ']'
                fdesc = ' // ' + fdesc if fdesc else ''
                wn = 0 if idt else w['name']
                fs = f'{fd[FieldID]:>{w["id"]}} {fname:<{wn}} {fdef}'
                wf = w['id'] + w['type'] if idt else wt
            wf = w['desc'] if w['desc'] else wf
            text += etrunc(f'{fs:{wf}}{fdesc}'.rstrip(), w['page']) + '\n'
    """
    return etree.tostring(xasd, pretty_print=True)


def xasd_dump(schema: dict, fname: Union[bytes, str, int], source='', style=None) -> NoReturn:
    with open(fname, 'w', encoding='utf8') as f:
        if source:
            f.write(f'<!-- Generated from {source}, {datetime.ctime(datetime.now())} -->\n\n')
        f.write(xasd_dumps(schema, style))


def xasd_loads(doc: str) -> dict:
    info = {}
    types = []
    """
    fields = None
    for line in doc.splitlines():
        if line:
            t, v = line2jadn(line, types[-1] if types else None)    # Parse a JIDL line
            if t == 'F':
                fields.append(v)
            elif fields:
                cleanup_tagid(fields)
                fields = None
            if t == 'I':
                info.update({v[0]: json.loads(v[1])})
            elif t == 'T':
                types.append(v)
                fields = types[-1][Fields]
    """
    return check({'info': info, 'types': types} if info else {'types': types})


def xasd_load(fp: TextIO) -> dict:
    return xasd_loads(fp.read())


__all__ = [
    'xasd_dump',
    'xasd_dumps',
    'xasd_load',
    'xasd_loads',
    'xasd_style'
]
