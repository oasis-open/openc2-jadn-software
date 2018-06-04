import json
import re


def jadnFormat(jadn, indent=1):
    idn = ' ' * (indent if type(indent) is int else 2)
    meta_opts = []

    for k, v in jadn['meta'].items():
        if type(v) is list:
            obj = []

            for itm in v:
                if type(itm) is list:
                    obj.append('{idn}[\"{v}\"]'.format(
                        idn=idn * 3,
                        v='\", \"'.join(itm)
                    ))
                else:
                    obj.append('{idn}\"{v}\"'.format(
                        idn=idn * 3,
                        v=itm
                    ))

            meta_opts.append('{idn}\"{k}\": [\n{v}\n{idn}]'.format(
                idn=idn * 2,
                k=k,
                v=',\n'.join(obj)
            ))
        else:
            meta_opts.append('{idn}\"{k}\": \"{v}\"'.format(
                idn=idn * 2,
                k=k,
                v=v
            ))

    meta = "{idn}\"meta\": {{\n{obj}\n{idn}}}".format(idn=idn, obj=',\n'.join(meta_opts))
    type_defs = []

    for itm in jadn['types']:
        # print(itm)
        header = []
        for h in itm[0: -1]:
            if type(h) is list:
                header.append("[{obj}]".format(obj=', '.join(['\"{}\"'.format(i) for i in h])))
            else:
                header.append('\"{}\"'.format(h))

        defs = []

        if type(itm[-1]) is list:
            for def_itm in itm[-1]:
                if type(def_itm) is list:
                    defs.append('{obj}'.format(obj=json.dumps(def_itm)))
                else:
                    defs.append("\"{itm}\"".format(itm=def_itm))

        else:
            defs.append("\"{itm}\"".format(itm=itm[-1]))

        defs = ',\n'.join(defs)  # .replace('\'', '\"')

        if re.match(r'^\s*?\[', defs):
            defs = "[\n{defs}\n{idn}{idn}]".format(idn=idn, defs=re.sub(re.compile(r'^', re.MULTILINE), '{idn}'.format(idn=idn * 3), defs))

        type_defs.append("\n{idn}{idn}[{header}, {defs}]".format(
            idn=idn,
            header=', '.join(header),
            defs=defs
        ))

    types = "[{obj}\n{idn}]".format(idn=idn, obj=','.join(type_defs))

    return "{{\n{meta},\n{idn}\"types\": {types}\n}}".format(idn=idn, meta=meta, types=types)


with open('schema_gen_test/openc2-wd06-format.jsdn', 'wb') as f:
    f.write(jadnFormat(json.load(open(b'schema/openc2-wd06.jadn'))).encode())
