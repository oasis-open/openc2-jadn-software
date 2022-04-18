"""
Translate JADN to/from Markdown tables
"""
import json
import re

from datetime import datetime
from typing import NoReturn, Tuple, Union
from jadn.definitions import TypeName, BaseType, TypeOptions, TypeDesc, Fields, ItemID, FieldID, INFO_ORDER
from jadn.utils import cleanup_tagid, get_optx, fielddef2jadn, jadn2fielddef, jadn2typestr, raise_error, typestr2jadn

# MARKDOWN -> JADN Type regexes
p_tname = r'\s*([-$\w]+)'               # Type Name
p_assign = r'\s*='                      # Type assignment operator
p_tstr = r'\s*(.*?)\s*\{?'              # Type definition
p_tdesc = r'(?:\s*\/\/\s*(.*?)\s*)?'    # Optional Type description

# MARKDOWN -> JADN Field regexes
p_id = r'\s*(\d+)'  # Field ID
p_fname = r'\s+([-:$\w]+\/?)?'  # Field Name with dir/ option (colon is deprecated, allow for now)
p_fstr = r'\s*(.*?)'  # Field definition or Enum value
p_range = r'\s*(?:\[([.*\w]+)\]|(optional))?'  # Multiplicity
p_desc = r'\s*(?:\/\/\s*(.*?)\s*)?'  # Field description, including field name if .id option


def markdown_style() -> dict:
    return {
        'pad': True,    # Use one space horizontal padding
        'links': True   # Retain Markdown links: [text](link)
    }


def markdown_dumps(schema: dict, style: dict = None) -> str:
    """
    Convert JADN schema to Markdown Tables

    :param dict schema: JADN schema
    :param dict style: Override default options if specified
    :return: Markdown tables
    :rtype: str
    """
    w = markdown_style()
    if style:
        w.update(style)   # Override any specified style options

    text = ''
    info = schema['info'] if 'info' in schema else {}
    mlist = [k for k in INFO_ORDER if k in info]
    for k in mlist + list(set(info) - set(mlist)):      # Display info elements in fixed order
        text += f'{k:>14}: {json.dumps(info[k])}\n'     # TODO: wrap to width, continuation-line parser

    for td in schema['types']:
        if len(td) > Fields and td[Fields]:
            tdef = f'{td[TypeName]} ({jadn2typestr(td[BaseType], td[TypeOptions])})'
            tdesc = f'\n{td[TypeDesc]}\n' if td[TypeDesc] else ''
            text += f'{tdesc}\n**Type: ' + tdef.replace("*", "\*") + '**\n'
            idt = td[BaseType] == 'Array' or get_optx(td[TypeOptions], 'id') is not None
            table_type = (0 if td[BaseType] == 'Enumerated' else 2) + (0 if idt else 1)
            table = [
                [['ID', 'Description']],
                [['ID', 'Item', 'Description']],
                [['ID', 'Type', '\#', 'Description']],
                [['ID', 'Name', 'Type', '\#', 'Description']]
            ][table_type]
            for fd in td[Fields]:
                fname, fdef, fmult, fdesc = jadn2fielddef(fd, td)
                fdef = fdef.replace('*', '\*')
                fmult = fmult.replace('*', '\*')
                dsc = fdesc.split('::', maxsplit=2)
                fdesc = f'**{dsc[0]}** - {dsc[1].strip()}' if len(dsc) == 2 else fdesc
                if table_type == 0:
                    table.append([str(fd[ItemID]), fdesc])
                elif table_type == 1:
                    table.append([str(fd[ItemID]), f'**{fname}**', fdesc])
                elif table_type == 2:
                    table.append([str(fd[FieldID]), fdef, fmult, fdesc])
                elif table_type == 3:
                    table.append([str(fd[FieldID]), f'**{fname}**', fdef, fmult, fdesc])
        else:
            table = [['Type Name', 'Type Definition', 'Description'],
                     [f'**{td[TypeName]}**', jadn2typestr(td[BaseType], td[TypeOptions]), td[TypeDesc]]]
        text += f'\n{format_table(table)}\n\n**********\n'
    return text


def format_table(rows: list) -> str:
    cwidth = [len(data.strip()) for data in rows[0]]
    for row in rows[1:]:
        for c in range(len(row)):
            cwidth[c] = max(cwidth[c], len(row[c].strip()))
    hbar = f'|{"|".join(["-" * (c + 2) for c in cwidth])}|'
    cf = f'| {" | ".join(["{:" + str(c) + "}" for c in cwidth])} |'
    return '\n'.join([cf.format(*rows[0])] + [hbar] + [cf.format(*r) for r in rows[1:]])


def markdown_dump(schema: dict, fname: Union[bytes, str, int], source='', style=None) -> NoReturn:
    with open(fname, 'w', encoding='utf8') as f:
        if source:
            f.write(f'<!--- Generated from {source}, {datetime.ctime(datetime.now())} --->\n\n')
        f.write(markdown_dumps(schema, style))


# Convert MARKDOWN to JADN
def line2jadn(line: str, tdef: list) -> Tuple[str, list]:
    if line.split('//', maxsplit=1)[0].strip():
        p_info = r'^\s*([-\w]+):\s*(.+?)\s*$'
        if m := re.match(p_info, line):
            return 'M', [m.group(1), m.group(2)]

        p_type = fr'^{p_tname}{p_assign}{p_tstr}{p_tdesc}$'
        if m := re.match(p_type, line):
            btype, topts, fo = typestr2jadn(m.group(2))
            assert fo == []                     # field options MUST not be included in typedefs
            newtype = [m.group(1), btype, topts, m.group(3) if m.group(3) else '', []]
            return 'T', newtype

        if tdef:        # looking for fields
            pn = '()' if (get_optx(tdef[TypeOptions], 'id') is not None or tdef[BaseType] == 'Array') else p_fname
            if tdef[BaseType] == 'Enumerated':      # Parse Enumerated Item
                pattern = fr'^{p_id}{p_fstr}{p_desc}$'
                if m := re.match(pattern, line):
                    return 'F', fielddef2jadn(int(m.group(1)), m.group(2), '', '', m.group(3) if m.group(3) else '')
            else:                                   # Parse Field
                pattern = f'^{p_id}{pn}{p_fstr}{p_range}{p_desc}$'
                if m := re.match(pattern, line):
                    m_range = '0..1' if m.group(5) else m.group(4)        # Convert 'optional' to range
                    fdesc = m.group(6) if m.group(6) else ''
                    return 'F', fielddef2jadn(int(m.group(1)), m.group(2), m.group(3), m_range if m_range else '', fdesc)
        else:
            raise_error(f'MARKDOWN Load - field with no type: {repr(line)}')

    return '', []


def markdown_loads(doc: str) -> dict:
    info = {}
    types = []
    fields = None
    for line in doc.splitlines():
        if line:
            t, v = line2jadn(line, types[-1] if types else None)    # Parse a MARKDOWN line
            if t == 'F':
                fields.append(v)
            elif fields:
                cleanup_tagid(fields)
                fields = None
            if t == 'M':
                info.update({v[0]: json.loads(v[1])})
            elif t == 'T':
                types.append(v)
                fields = types[-1][Fields]
    return {'info': info, 'types': types} if info else {'types': types}


def markdown_load(fname: Union[bytes, str, int]) -> dict:
    with open(fname, 'r') as f:
        return markdown_loads(f.read())


__all__ = [
    'markdown_dump',
    'markdown_dumps',
    'markdown_load',
    'markdown_loads',
    'markdown_style'
]
