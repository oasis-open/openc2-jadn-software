import jadn
import json
import os
from jadn.definitions import TypeName, Fields, FieldType
from collections import defaultdict

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


def typerefname(prop: str, jsref: dict) -> str:
    """
    Infer a type name from a JSON Schema property reference
    """
    if (t := jsref.get('type', '')) in ('string', 'number'):
        return t.capitalize() + D[4]    # Built-in type
    if ref := jsref.get('$ref', ''):
        if ref.startswith('#/definitions/'):  # Exact type name
            return ref.removeprefix('#/definitions/') + D[5]
        if td := jssx[ref]:
            if ':' in td:
                return td.split(':', maxsplit=1)[1].capitalize() + D[6]  # Extract type name from $id
            if td2 := jss['definitions'].get(td, {}):
                return typerefname('', td2) + D[7]
    if tn := prop.capitalize():
        tn += '1' if jadn.definitions.is_builtin(tn) else ''
        return tn + D[8]
    return jsref.get('title', '??').replace(' ', '').capitalize() + D[9]  # Guess type name from object def title


def scandef(tn: str, tv: dict, nt: list):
    """
    Search type definition for nested definitions, add to new types list nt
    """
    if (ptype := tv.get('type', '')) == 'object':
        for k, v in tv.get('properties', {}).items():
            if v.get('type', '') == 'array':
                topts = [f'{{{v["minItems"]}'] if 'minItems' in v else []
                if maxv := v["maxItems"] if 'maxItems' in v else []:
                    topts.append(f'}}{maxv}')
                topts.append(f'*{typerefname(k, v["items"])}')
                nt.append((k, ('ArrayOf', tuple(topts))))
            elif v.get('anyOf', ''):
                print('  choice:', k, v['anyOf'])
            scandef(k, v, nt)


def define_jadn_type(tn: str, tv: dict) -> list:
    topts = []
    tdesc = tv.get('description', '')
    fields = []
    if (ftype := tv.get('type', None)) == 'object':
        basetype = 'Record'
        req = tv.get('required', [])
        for n, (k, v) in enumerate(tv.get('properties', {}).items(), start=1):
            fopts = ['[0'] if k not in req else []
            if v.get('type', '') in ('object', 'array'):
                if ft := newtypes.get(k, {}):
                    if len(set(ft)) == 1:
                        ftype = typerefname(k, {})
                    else:
                        ftype = 'Multiple'
                else:
                    ftype = 'Unknown'
            else:
                ftype = typerefname('', v)
            fdef = [n, k, ftype, fopts, v.get('description', '')]
            fields.append(fdef)
    elif ftype == 'array':
        basetype = 'ArrayOf'
        topts = [f'[{tv["minItems"]}'] if 'minItems' in tv else []
        topts.append(f']{tv.get("maxItems", 0)}')
        topts.append(f'#{typerefname("", tv["items"])}')
    elif ftype == 'string':
        basetype = 'String'
    else:
        basetype = 'Boolean'

    return [typedefname(tn), basetype, topts, tdesc, fields]

"""
Create a JADN type from each definition in a Metaschema-generated JSON Schema
"""
if __name__ == '__main__':
    with open(JSCHEMA, encoding='utf-8') as fp:
        jss = json.load(fp)
    types = {typedefname(k): v for k, v in jss['definitions'].items()}
    jssx = {v.get('$id', k): k for k, v in jss['definitions'].items()}     # Build index from $id to definitions name

    assert jss['type'] == 'object'
    info = {'package': jss['$id']}
    info.update({'comment': jss['$comment']} if '$comment' in jss else {})
    info.update({'exports': ['Root']})
    info.update({'config': {
        '$FieldName': '^[$a-z][-_A-Za-z0-9]{0,63}$',
        '$TypeName': '^[A-Z][-:$A-Za-z0-9]{0,63}$'}})

    nt = []
    newtypes = defaultdict(list)
    for tn, tv in jss['definitions'].items():
        scandef(tn, tv, nt)
    for t in nt:
        newtypes[t[0]].append(t[1])

    types = [define_jadn_type('Root', jss)]
    for jtn, jtp in jss['definitions'].items():
        td = define_jadn_type(jtn, jtp)
        if not td[TypeName].startswith('NoDef$'):
            types.append(td)

    dn = {}     # Correlate type definitions with references, for debugging
    rn = {}
    for td in types:
        dn.update({td[TypeName].lower(): td[TypeName]})
        for fd in td[Fields]:
            rn.update({fd[FieldType].lower(): fd[FieldType]})
    dd = [(dn.get(k, ''), rn.get(k, '')) for k in sorted(set(dn) | set(rn))]

    for k, v in newtypes.items():
        nt = list(set(v))[0]
        tname = k.capitalize()
        tname += '1' if jadn.definitions.is_builtin(tname) else ''
        types.append([tname, nt[0], list(nt[1]), "", []])

    jadn.dump(schema := {'info': info, 'types': types}, 'out.jadn')
    print('\n'.join([f'{k:>15}: {v}' for k, v in jadn.analyze(jadn.check(schema)).items()]))
