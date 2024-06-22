"""
Translate JADN to XML Abstract Schema Definition (XASD) format
"""

import jadn
from lxml import etree
from datetime import datetime
from typing import NoReturn, TextIO, Tuple, Union
from jadn.definitions import TypeName, BaseType, TypeOptions, TypeDesc, Fields
from jadn.definitions import ItemID, ItemValue, ItemDesc
from jadn.definitions import FieldID, FieldName, FieldType, FieldOptions, FieldDesc


def xasd_style() -> dict:
    # Return default column positions
    return {}


def xasd_dumps(schema: dict, style: dict = None) -> str:
    """
    Convert JADN schema to XASD
    """
    def set_attr(e: etree.Element, at: dict):
        [e.set(k, str(v)) for k, v in at.items() if not isinstance(v, str) or len(v)]

    w = xasd_style()
    if style:
        w.update(style)

    exports = schema.get('info', {}).get('exports', [])
    root = exports[0] if len(exports) == 1 else 'Root'

    xasd = etree.Element(root)
    if 'info' in schema:
        xasd.append(info := etree.Element('Info'))
        # for info in schema['info']:
        #
    xasd.append(types := etree.Element('Types'))

    for td in schema['types']:
        te = etree.Element(td[BaseType], attrib={'name': td[TypeName]})
        set_attr(te, jadn.topts_s2d(td[TypeOptions]))
        set_attr(te, {'description': td[TypeDesc]})
        if td[BaseType] == 'Enumerated':
            for item in td[Fields]:
                fe = etree.Element('item', attrib={
                    'id': str(item[ItemID]),
                    'value': item[ItemValue]})
                set_attr(fe, {'description': item[ItemDesc]})
                te.append(fe)
        elif jadn.definitions.has_fields(td[BaseType]):
            for field in td[Fields]:
                fe = etree.Element('field', attrib={
                    'id': str(field[FieldID]),
                    'name': field[FieldName],
                    'type': field[FieldType]})
                fto, fo = jadn.ftopts_s2d(field[FieldOptions])
                set_attr(fe, fto)
                set_attr(fe, fo)
                set_attr(fe, {'description': field[FieldDesc]})
                te.append(fe)
        types.append(te)

    return etree.tostring(xasd, pretty_print=True).decode()


def xasd_dump(schema: dict, fname: Union[bytes, str, int], source='', style=None) -> NoReturn:
    with open(fname, 'w', encoding='utf8') as f:
        if source:
            f.write(f'<!-- Generated from {source}, {datetime.ctime(datetime.now())} -->\n\n')
        f.write(xasd_dumps(schema, style))


def xasd_loads(doc: str) -> dict:
    info = {}
    types = []
    xasd = etree.fromstring(doc)

    return jadn.core.check({'info': info, 'types': types} if info else {'types': types})


def xasd_load(fp: TextIO) -> dict:
    return xasd_loads(fp.read())


__all__ = [
    'xasd_dump',
    'xasd_dumps',
    'xasd_load',
    'xasd_loads',
    'xasd_style'
]
