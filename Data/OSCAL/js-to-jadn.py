import jadn
import json
import os
from jadn.definitions import *

SCHEMA_DIR = os.path.join('..', '..', 'Schemas', 'Metaschema')
JADN = os.path.join(SCHEMA_DIR, 'oscal-catalog.jadn')
JSCHEMA = os.path.join(SCHEMA_DIR, 'oscal_catalog_schema_1.1.0.json')
DEBUG = True
D = [(f'${n}' if DEBUG else '') for n in range(10)]


def typedefname(jsdef: str) -> str:
    """
    Infer type name from a JSON Schema definition
    """
    assert isinstance(jsdef, str), f'Not a type definition name: {jsdef}'
    td = jss['definitions'][jsdef]
    if td.get('type', '') == 'string':
        return jsdef + D[0]     # Exact type name
    if (d := td.get('$ref', '')).startswith('#/definitions/'):  # Exact type name
        return d.removeprefix('#/definitions/') + D[1]
    return td.get('title', '??').replace(' ', '') + D[2]    # Guess type name from title


def typerefname(jsref: dict) -> str:
    """
    Infer a type name from a JSON Schema property reference
    """
    if ref := jsref.get('$ref', ''):
        if td := jssx[ref]:
            return td.split(':', maxsplit=1)[1].capitalize() + D[5]  # Extract type name from $id
    return jsref.get('title', '??').replace(' ', '') + D[6]  # Guess type name from object def title


def define_jadn_type(jsname: str, jstype: dict) -> list:
    fields = []
    jtype = 'String'
    tname = jsname.split(':', maxsplit=1)[-1]
    tref = jstype.get('$ref', '').replace('#/definitions/', '*')
    print(f'  {jsname:<60} {jstype.get("type", tref):>25}: {tname:<25} "{jstype.get("title", "")}"')
    req = jstype.get('required', [])
    if (ftype := jstype.get('type', None)) == 'object':
        jtype = 'Record'
        for n, (k, v) in enumerate(jstype.get('properties', {}).items(), start=1):
            fopts = ['[0'] if k not in req else []
            ft = ''
            if v.get('type', '') == 'array':
                fopts.append(f']{v.get("maxItems", 0)}')
                ft = typerefname(v['items'])
            ftype = v.get('$ref', ft).replace('#/definitions/', '')
            fdef = [n, k, ftype, fopts, v.get('description', '')]
            print(f'    {fdef}')
            fields.append(fdef)
    elif ftype == 'string':
        pass
    return [typedefname(jsname), jtype, [], jstype.get('description', ''), fields]

"""
Create a JADN type from each definition in a Metaschema-generated JSON Schema
"""
if __name__ == '__main__':
    with open(JSCHEMA, encoding='utf-8') as fp:
        jss = json.load(fp)
    jssx = {v.get('$id', ''): k for k, v in jss['definitions'].items()}     # Build index from $id to definitions name

    types = []
    for jtn, jtp in jss['definitions'].items():
        types.append(define_jadn_type(jtn, jtp))
    jadn.dump({'types': types}, 'out.jadn')