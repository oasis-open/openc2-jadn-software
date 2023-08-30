import jadn
import json
import os
from jadn.definitions import TypeName, BaseType, Fields, FieldType
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
    if ':' in jsdef:
        return jsdef.split(':', maxsplit=1)[1].capitalize() + D[1]
    if d := jss['definitions'].get(jsdef, ''):
        if r := d.get('$ref', ''):
            return f'NoDef${jsdef}' + D[2]
    return jsdef + D[0]     # Exact type name


def typerefname(jsref: dict) -> str:
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
                return typerefname(td2) + D[7]
    return ''


def guess_type(tn: str, td: dict) -> str:
    if tdn := typedefname(tn):  # Return a reliable type name
        return tdn
    return td.get('title', 'Foo').replace(' ', '')  # Otherwise grasp at straws to return something
    # if tn := prop.capitalize():
    #     tn += '1' if jadn.definitions.is_builtin(tn) else ''
    #     return tn + D[8]
    # return jsref.get('title', '??').replace(' ', '').capitalize() + D[9]  # Guess type name from object def title


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
                if not (vtype := typerefname(v['items'])):
                    vtype = f'{typedefname(tn)}${k}'
                    nt.append(define_jadn_type(vtype, v['items']))
                    scandef(vtype, v['items'], nt)
                topts.append(f'*{vtype}')
                nt.append((k, ('ArrayOf', tuple(topts))))
            elif v.get('anyOf', ''):
                print('  choice:', tn, k, v['anyOf'])
                vtype = f'{typedefname(tn)}${k}'
                if td := define_jadn_type(vtype, v):
                nt.append(define_jadn_type(vtype, v))
                scandef(vtype, v['anyOf'], nt)
            elif typerefname(v):
                print('  nested property type:', f'{tn}${k}', v)
                # td = define_jadn_type(k, v)
                # nt.append(k, (td[BaseType], tuple()))
        if not tn:
            print(f'  nested type: "{tv.get("title", "")}"')


def define_jadn_type(tn: str, tv: dict) -> list:
    topts = []
    tdesc = tv.get('description', '')
    fields = []
    if (jstype := tv.get('type', '')) == 'object':
        basetype = 'Record'
        req = tv.get('required', [])
        for n, (k, v) in enumerate(tv.get('properties', {}).items(), start=1):
            fopts = ['[0'] if k not in req else []
            fdesc = v.get('description', '')
            if v.get('type', '') == 'array':
                if ft := newtypes.get(k, {}):
                    if len(set(ft)) == 1:
                        ftype = k.capitalize()
                    else:
                        ftype = 'Multiple'
                else:
                    ftype = guess_type(tn, v)
            elif v.get('type', '') == 'object':
                ftype = 'Object'
            elif t := jssx.get(v.get('$ref', ''), ''):
                ft = jss['definitions'][t]
                ftype = typerefname(ft)
                ftype = ftype if ftype in jss['definitions'] else typerefname(v)
                fdesc = ft.get('description', '')
            else:
                ftype = typerefname(v)
            fdef = [n, k, ftype, fopts, fdesc]
            fields.append(fdef)
    elif td := tv.get('anyOf', ''):
        basetype = 'Choice'
        topts = ['<']
        for n, v in enumerate(td, start=1):
            fd = define_jadn_type(f'{tn}${n}', v)
            ftype = fd[0] if fd else typerefname(v)
            fdef = [n, f'c{n}', ftype, [], '']
            fields.append(fdef)
    elif td := tv.get('enum', ''):
        basetype = 'Enumerated'
        for n, v in enumerate(td, start=1):
            fields.append(n, v, '')
    elif jstype == 'array':     # TODO: process individual items
        basetype = 'ArrayOf'
        topts = [f'[{tv["minItems"]}'] if 'minItems' in tv else []
        topts.append(f']{tv.get("maxItems", 0)}')
        topts.append(f'#{typerefname(tv["items"])}')
    elif jstype in ('string', 'number'):
        if p := tv.get('pattern', ''):
            topts.append(f'%{p}')
        basetype = jstype.capitalize()
    else:
        raise ValueError(f'{tn} not a type definition. Reference {typerefname(tv)}?')
        # return []

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
    info.update({'exports': ['$Root']})
    info.update({'config': {'$FieldName': '^[$a-z][-_$A-Za-z0-9]{0,63}$'}})

    nt = []
    newtypes = defaultdict(list)
    for tn, tv in jss['definitions'].items():
        scandef(tn, tv, nt)
    for t in nt:
        newtypes[t[0]].append(t[1] if len(t) == 2 else t)

    extra = []
    types = [define_jadn_type('$Root', jss)]
    for jtn, jtp in jss['definitions'].items():
        td = define_jadn_type(jtn, jtp)
        if not td[TypeName].startswith('NoDef$') and jadn.definitions.is_builtin(td[BaseType]):
            types.append(td)
        else:
            extra.append(td)

    dn = {}     # Correlate type definitions with references, for debugging
    rn = {}
    for td in types:
        dn.update({td[TypeName].lower(): td[TypeName]})
        for fd in td[Fields]:
            rn.update({fd[FieldType].lower(): fd[FieldType]})
    dd = [(dn.get(k, ''), rn.get(k, '')) for k in sorted(set(dn) | set(rn))]

    tx = {t[0]: t for t in types}
    ntx = {k.capitalize(): v[0][1][1][1:] for k, v in newtypes.items() if v[0][0] == 'ArrayOf'}  # Map ArrayOf vtype option to type name
    for k, v in newtypes.items():   # Merge nested types into top-level types
        if len(v[0]) == 2:
            nt = list(set(v))[0]
            tname = k.capitalize()
            tname += '1' if jadn.definitions.is_builtin(tname) else ''
            tdef = [tname, nt[0], list(nt[1]), "", []]
            if (rname := ntx.get(tname, '')) in tx:     # Sort array definitions to be with the array items
                types.insert(types.index(tx[rname]), tdef)
            else:
                types.append(tdef)
        else:
            types.append(v[0])

    jadn.dump(schema := {'info': info, 'types': types}, 'out.jadn')
    print('\n'.join([f'{k:>15}: {v}' for k, v in jadn.analyze(jadn.check(schema)).items()]))
