import json
import re
import sys

# Version Compatability
encoding = sys.getdefaultencoding()
primitives = [
    bytes,
    str
]
defaultDecode_itr = [
    str,
    int,
    float
]

if sys.version_info.major >= 3:
    def toUnicode(s):
        return s.decode(encoding, 'backslashreplace') if hasattr(s, 'decode') else s

    def toStr(s):
        return toUnicode(s)

elif sys.version_info.major < 3:
    primitives.append(unicode)
    defaultDecode_itr.append(basestring)

    def toUnicode(s):
        return unicode(s)

    def toStr(s):
        return str(s)


class Utils(object):
    @staticmethod
    def defaultEncode(itm):
        tmp = type(itm)()
        for k in itm:
            ks = toUnicode(k)
            if type(itm[k]) in [dict, list]:
                tmp[ks] = Utils.defaultEncode(itm[k])

            elif type(itm[k]) in primitives:
                tmp[ks] = toUnicode(itm[k])

            else:
                print('Not prepared type: {}'.format(type(itm[k])))
                tmp[ks] = itm[k]

        return tmp

    @staticmethod
    def defaultDecode(itm):
        tmp = type(itm)()

        if hasattr(tmp, '__iter__') and type(tmp) not in defaultDecode_itr:
            for k in itm:
                if type(tmp) == dict:
                    tmp[Utils.defaultDecode(k)] = Utils.defaultDecode(itm[k])

                elif type(tmp) == list:
                    tmp.append(Utils.defaultDecode(k))

                else:
                    print('not prepared type: {}-{}'.format(type(tmp), tmp))

        else:
            tmp = toStr(itm)

        return tmp

    @staticmethod
    def jadnFormat(jadn, indent=1):
        if type(jadn) is not dict:
            try:
                jadn = json.load(jadn)
            except Exception as e:
                print(e)
                raise TypeError("JADN improperly formatted")

        idn = ' ' * (indent if type(indent) is int else 2)
        meta_opts = []

        if 'meta' in jadn:
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

        if 'types' in jadn:
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
                    defs = "[\n{defs}\n{idn}{idn}]".format(idn=idn, defs=re.sub(re.compile(r'^', re.MULTILINE), '{idn}'.format(idn=idn*3), defs))

                type_defs.append("\n{idn}{idn}[{header}{defs}]".format(
                    idn=idn,
                    header=', '.join(header),
                    defs='' if defs == '' else ', {}'.format(defs)
                ))

        types = "[{obj}\n{idn}]".format(idn=idn, obj=','.join(type_defs))

        return "{{\n{meta},\n{idn}\"types\": {types}\n}}".format(idn=idn, meta=meta, types=types)

    @staticmethod
    def opts_d2s(opts, field=False):     # TODO: Refactor to use TYPE_OPTIONS / FIELD_OPTIONS as above
        """
        Convert options dictionary to list of option strings
        """
        if type(opts) is list:
            return opts

        field = field if type(field) is bool else False
        ostr = []
        for k, v in opts.items():
            # print(k, v)
            if k == "optional" and v:
                ostr.append("?")
            elif k == "atfield":
                ostr.append("{{}".format(v))
            elif k == "range":
                ostr.append("[{}:{}".format(v[0], v[1]))
            elif k == "pattern":
                ostr.append(">{}".format(v))
            elif k == "format":
                ostr.append("@{}".format(v))
            elif k == "rtype":
                ostr.append("*{}".format(v))

            # Additional options from original function
            elif k == "min":
                ostr.append("[{}".format(v if type(v) is int else 0))
            elif k == "max":
                ostr.append("]{}".format(v if type(v) is int else 1))

            # Type Options
            elif k == "compact" and not field:
                ostr.append("=")

            # Field Options
            elif k == "atfield" and v and field:
                ostr.append("&{}".format(v))
            elif k == "etype" and v and field:
                ostr.append("/{}".format(v))
            elif k == "default" and field:
                ostr.append("!")

            else:
                print("Unknown option '{}'".format(k))
        return ostr
