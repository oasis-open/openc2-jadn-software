import sys

# Version Compatability
encoding = sys.getdefaultencoding()
primitives = [
    bytes,
    str
]
defaultDecode_ign = [
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
    defaultDecode_ign.append(basestring)

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

        if hasattr(tmp, '__iter__') and type(tmp) not in defaultDecode_ign:
            for k in itm:
                if type(tmp) == dict:
                    tmp[Utils.defaultDecode(k)] = Utils.defaultDecode(itm[k])

                elif type(tmp) == list:
                    tmp.append(Utils.defaultDecode(k))

                else:
                    print('not prepared type: {}'.format(type(tmp)))

        else:
            tmp = str(itm)

        return tmp
