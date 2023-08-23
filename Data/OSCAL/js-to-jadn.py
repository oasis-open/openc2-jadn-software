import jadn
import json
import os

SCHEMA_DIR = os.path.join('..', '..', 'Schemas', 'Metaschema')
JADN = os.path.join(SCHEMA_DIR, 'oscal-catalog.jadn')
JSCHEMA = os.path.join(SCHEMA_DIR, 'oscal_catalog_schema_1.1.0.json')
DEBUG = False
D = [(f'${n}' if DEBUG else '') for n in range(10)]


def typedefname(jsdef: str) -> str:
    """
    Infer type name from a JSON Schema definition
    """
    assert isinstance(jsdef, str), f'Not a type definition name: {jsdef}'
    if ':' in jsdef:
        return jsdef.split(':', maxsplit=1)[1].capitalize() + D[1]
    return jsdef + D[0]     # Exact type name


def typerefname(jsref: dict) -> str:
    """
    Infer a type name from a JSON Schema property reference
    """
    if ref := jsref.get('$ref', ''):
        if ref.startswith('#/definitions/'):  # Exact type name
            return ref.removeprefix('#/definitions/') + D[5]
        if td := jssx[ref]:
            if ':' in td:
                return td.split(':', maxsplit=1)[1].capitalize() + D[6]  # Extract type name from $id
            if td2 := jss['definitions'].get(td, {}):
                return typerefname(td2) + D[8]
    return jsref.get('title', '??').replace(' ', '') + D[7]  # Guess type name from object def title


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
            if v.get('type', '') == 'array':
                fopts.append(f']{v.get("maxItems", 0)}')
                ftype = typerefname(v['items'])
            else:
                ftype = typerefname(v)
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
    jssx = {v.get('$id', k): k for k, v in jss['definitions'].items()}     # Build index from $id to definitions name

    assert jss['type'] == 'object'
    info = {'package': jss['$id']}
    info.update({'comment': jss['$comment']} if '$comment' in jss else {})
    info.update({'exports': [typerefname(k) for k in jss['properties'].values()]})

    types = []
    for jtn, jtp in jss['definitions'].items():
        types.append(define_jadn_type(jtn, jtp))
    jadn.dump({'info': info, 'types': types}, 'out.jadn')