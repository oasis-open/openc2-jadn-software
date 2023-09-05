import jadn
import json
import os
from jadn.definitions import TypeName, BaseType, TypeOptions, Fields, FieldType

SCHEMA_DIR = os.path.join('..', '..', 'Schemas', 'Metaschema')
JSCHEMA = os.path.join(SCHEMA_DIR, 'oscal_catalog_schema_1.1.0.json')
DEBUG = False
D = [(f'${n}' if DEBUG else '') for n in range(10)]


def typedefname(jsdef: str) -> str:
    """
    Infer type name from a JSON Schema definition
    """
    assert isinstance(jsdef, str), f'Not a type definition name: {jsdef}'
    if d := jss['definitions'].get(jsdef, ''):
        if ':' in jsdef:  # qualified definition name
            return maketypename('', jsdef.split(':', maxsplit=1)[1]) + D[1]
        if ref := d.get('$ref', ''):
            return ref.removeprefix('#/definitions/')+ D[2]
    return jsdef.removeprefix('#/definitions/') + D[0]     # Exact type name or none


def typerefname(jsref: dict) -> str:
    """
    Infer a type name from a JSON Schema property reference
    """
    if (t := jsref.get('type', '')) in ('string', 'integer', 'number', 'boolean'):
        return t.capitalize() + D[4]    # Built-in type
    if ref := jsref.get('$ref', ''):
        td = jssx.get(ref, ref)
        if td.startswith('#/definitions/'):  # Exact type name
            return td.removeprefix('#/definitions/') + D[5]
        if ':' in td:
            return maketypename('', td.split(':', maxsplit=1)[1]) + D[6]  # Extract type name from $id
        if td2 := jss['definitions'].get(td, {}):
            return typerefname(td2) + D[7]
    return ''


def singular(name: str) -> str:
    """
    Guess a singular type name for the anonymous items in a plural ArrayOf type
    """
    if name.endswith('ies'):
        return name[:-3] + 'y'
    elif name.endswith('es'):
        n = -2 if name[-4:-3] == 's' else -1
        return name[:n]
    elif name.endswith('s'):
        return name[:-1]
    return name + '-item'


def maketypename(tn: str, name: str) -> str:
    """
    Convert a type and property name to type name
    """
    tn = typedefname(tn)
    name = f'{tn}${name}' if tn else name.capitalize()
    return name + '1' if jadn.definitions.is_builtin(name) else name


def scandef(tn: str, tv: dict, nt: list):
    """
    Process nested type definitions, add to list nt
    """

    if not (td := define_jadn_type(tn, tv)):
        return
    nt.append(td)
    if tv.get('type', '') == 'object':
        for k, v in tv.get('properties', {}).items():
            if v.get('$ref', '') or v.get('type', '') in ('string', 'number', 'integer', 'boolean'):     # Not nested
                pass
            elif v.get('type', '') == 'array':
                scandef(maketypename('', k), v, nt)
                scandef(singular(maketypename('', k)), v['items'], nt)  # TODO: primitive with options or none
            elif v.get('anyOf', '') or v.get('allOf', ''):
                scandef(maketypename(tn, k), v, nt)
            elif typerefname(v):
                print('  nested property type:', f'{td[TypeName]}${k}', v)

        if not tn:
            print(f'  nested type: "{tv.get("title", "")}"')
    elif (tc := tv.get('anyOf', '')) or (tc := tv.get('allOf', '')):
        for n, v in enumerate(tc, start=1):
            scandef(maketypename(tn, n), v, nt)
    pass


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
                ftype = maketypename('', k)
                idesc = jss['definitions'].get(jssx.get(v['items'].get('$ref', ''), ''), {}).get('description', '')
                fdesc = fdesc if fdesc else v['items'].get('description', idesc)
            elif v.get('type', '') == 'object':
                ftype = tn
            elif t := jssx.get(v.get('$ref', ''), ''):
                rt = jss['definitions'][t].get('$ref', '')
                ftype = typedefname(rt if rt else t)
                ft = jss['definitions'][t]
                fdesc = ft.get('description', '')
            elif v.get('anyOf', '') or v.get('allOf', ''):
                ftype = maketypename(tn, k)
            else:
                ftype = typerefname(v)
            fdef = [n, k, ftype, fopts, fdesc]
            if not ftype:
                raise ValueError(f'  empty field type {tn}${k}')
            fields.append(fdef)
    elif (td := tv.get('anyOf', '')) or (td := tv.get('allOf', '')):
        basetype = 'Choice'
        # topts = ['<', '∪'] if 'allOf' in tv else ['<']    # TODO: update Choice in JADN library
        # topts = ['∪'] if 'allOf' in tv else []
        for n, v in enumerate(td, start=1):
            fd = typerefname(v)
            ftype = fd if fd else maketypename(tn, n)
            fdef = [n, f'c{n}', ftype, [], '']
            fields.append(fdef)
    elif td := tv.get('enum', ''):
        basetype = 'Enumerated'
        for n, v in enumerate(td, start=1):
            fields.append([n, v, ''])
    elif jstype == 'array':     # TODO: process individual items
        basetype = 'ArrayOf'
        topts = [f'{{{tv["minItems"]}'] if 'minItems' in tv else []
        topts.append(f'}}{tv["maxItems"]}') if 'maxItems' in tv else []
        ref = jss['definitions'].get(jssx.get(tv['items'].get('$ref', ''), ''), {})
        tr = typerefname(ref)
        tr = tr if tr else typerefname(tv['items'])
        tr = tr if tr else singular(tn)
        topts.append(f'*{tr}')
    elif jstype in ('string', 'integer', 'number', 'boolean'):
        if p := tv.get('pattern', ''):
            topts.append(f'%{p}')
        basetype = jstype.capitalize()
    else:
        return []

    return [typedefname(tn), basetype, topts, tdesc, fields]


if __name__ == '__main__':
    """
    Create a JADN type from each definition in a Metaschema-generated JSON Schema
    """
    with open(JSCHEMA, encoding='utf-8') as fp:
        jss = json.load(fp)
    assert jss['type'] == 'object', f'Unsupported JSON Schema format'
    jssx = {v.get('$id', k): k for k, v in jss['definitions'].items()}      # Index from $id to definition
    types = {typedefname(k): v for k, v in jss['definitions'].items()}      # Index from type name to definition
    assert len(types) == len(set(types)), f'Type name collision'

    info = {'package': jss['$id']}
    info.update({'comment': jss['$comment']} if '$comment' in jss else {})
    info.update({'exports': ['$Root']})
    info.update({'config': {'$MaxString': 1000, '$FieldName': '^[$a-z][-_$A-Za-z0-9]{0,63}$'}})

    nt = []     # Walk nested type definition tree to build type list
    scandef('$Root', jss, nt)
    for tn, tv in jss['definitions'].items():
        scandef(tn, tv, nt)

    ntypes = []     # Prune identical type definitions
    for t in nt:
        if t not in ntypes:     # O(n^2) runtime because type definitions aren't hashable
            ntypes.append(t)    # Convert to immutable types if it becomes an issue

    jadn.dump(schema := {'info': info, 'types': ntypes}, 'out.jadn')
    print('\n'.join([f'{k:>15}: {v}' for k, v in jadn.analyze(jadn.check(schema)).items()]))
