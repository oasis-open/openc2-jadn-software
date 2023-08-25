import jadn
import json
import os
from jadn.definitions import TypeName, Fields, FieldType

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
    if d := jss['definitions'].get(jsdef, ''):
        if r := d.get('$ref', ''):
            return f'NoDef${jsdef}' + D[2]
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
    return jsref.get('title', '??').replace(' ', '').capitalize() + D[7]  # Guess type name from object def title


def define_jadn_type(jsname: str, jstype: dict, types: list):
    topts = []
    tdesc = jstype.get('description', '')
    fields = []
    if (ftype := jstype.get('type', None)) == 'object':
        basetype = 'Record'
        req = jstype.get('required', [])
        for n, (k, v) in enumerate(jstype.get('properties', {}).items(), start=1):
            fopts = ['[0'] if k not in req else []
            # if v.get('type', '') == 'array':
            #    fopts.append(f']{v.get("maxItems", 0)}')
            #    ftype = typerefname(v['items'])
            if 'type' in v:
                define_jadn_type('Foo', v, types)
            else:
                ftype = typerefname(v)
            fdef = [n, k, ftype, fopts, v.get('description', '')]
            print(f'    {fdef}')
            fields.append(fdef)
    elif ftype == 'array':
        basetype = 'ArrayOf'
        if 'minItems' in jstype:
            topts.append(f'[{jstype["minItems"]}')
    elif ftype == 'string':
        basetype = 'String'
    else:
        basetype = None

    types.append([typedefname(jsname), basetype, topts, tdesc, fields])

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
    info.update({'exports': ['$Root']})
    info.update({'config': {'$FieldName': '^[a-z][-_A-Za-z0-9]{0,63}$'}})

    types = []
    define_jadn_type('$Root', jss, types)
    for jtn, jtp in jss['definitions'].items():
        define_jadn_type(jtn, jtp, types)
        # types.append(define_jadn_type(jtn, jtp))

    dn = {}     # Correlate type definitions with references, for debugging
    rn = {}
    for td in types:
        dn.update({td[TypeName].lower(): td[TypeName]})
        for fd in td[Fields]:
            rn.update({fd[FieldType].lower(): fd[FieldType]})
    dd = [(dn.get(k, ''), rn.get(k, '')) for k in sorted(set(dn) | set(rn))]

    jadn.dump({'info': info, 'types': types}, 'out.jadn')