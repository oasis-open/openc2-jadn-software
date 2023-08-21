import jadn
import json
import os
from jadn.definitions import *

SCHEMA_DIR = os.path.join('..', '..', 'Schemas', 'Metaschema')
JADN = os.path.join(SCHEMA_DIR, 'oscal-catalog.jadn')
JSCHEMA = os.path.join(SCHEMA_DIR, 'oscal_catalog_schema.json')


def typename(jsdef):
    if isinstance(jsdef, str):
        td = jss['definitions'][jsdef]
        if (d := td.get('$ref', '')).startswith('#/definitions/'):     # Exact type name
            return d.removeprefix('#/definitions/')
        return td.get('title', '??').replace(' ', '')   # Guess type name from title
    elif ref := jsdef.get('$ref', ''):
        if td := jssx[ref]:
            return td.split(':', maxsplit=1)[1].capitalize()    # Extract type name from $id
    else:
        return jsdef.get('title', '??').replace(' ', '')   # Guess type name from object def title
    print('  ## unknown type', jsdef)


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
                ft = typename(v['items'])
            ftype = v.get('$ref', ft).replace('#/definitions/', '')
            fdef = [n, k, ftype, fopts, v.get('description', '')]
            print(f'    {fdef}')
            fields.append(fdef)
    elif ftype == 'string':
        pass
    return [typename(jsname), jtype, [], jstype.get('description', ''), fields]


with open(JADN, encoding='utf-8') as fp:
    jns = jadn.load(fp)
print(f'{JADN}:\n' + '\n'.join([f'{k:>15}: {v}' for k, v in jadn.analyze(jadn.check(jns)).items()]))
codec = jadn.codec.Codec(jns, verbose_rec=True, verbose_str=True)
jnsx = {k[TypeName]: {j[FieldName] for j in k[Fields]} for k in jns['types']}

with open(JSCHEMA, encoding='utf-8') as fp:
    jss = json.load(fp)
jssx = {v.get('$id', ''): k for k, v in jss['definitions'].items()}

types = []
for jtn, jtp in jss['definitions'].items():
    types.append(define_jadn_type(jtn, jtp))
jadn.dump({'types': types}, 'out.jadn')