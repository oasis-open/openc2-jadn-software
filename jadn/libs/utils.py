import sys

# Version Compatability
encoding = sys.getdefaultencoding()
primitives = [bytes, str]

if sys.version_info.major >= 3:
    def toUnicode(s):
        return s.decode(encoding, 'backslashreplace') if hasattr(s, 'decode') else s

elif sys.version_info.major < 3:
    primitives.append(unicode)

    def toUnicode(s):
        return unicode(s)


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

        if hasattr(tmp, '__iter__'):
            for k in itm:
                def_k = Utils.defaultDecode(k)
                if type(tmp) == dict:
                    tmp[def_k] = Utils.defaultDecode(itm[k])

                elif type(tmp) == list:
                    tmp.append(def_k)

                else:
                    print('not prepared type')

        else:
            tmp = str(itm)

        return tmp
