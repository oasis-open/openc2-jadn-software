import json
import re

from datetime import datetime

from bs4 import BeautifulSoup, Comment

from ..codec.codec_utils import opts_d2s
from ..utils import toStr


class Relax2Jadn(object):
    def __init__(self, relax):
        if type(relax) in [str, bytes]:
            relax = toStr(relax)
            relax = relax.replace('\n', '')
            relax = re.sub(r'>\s*?<', '><', relax)
            self.schema = BeautifulSoup(relax, 'lxml')

        else:
            raise TypeError('Relax-NG improperly formatted')

        self._fieldMap = {
            'base64Binary': 'Binary',
            'boolean': 'Boolean',
            'integer': 'Integer',
            'float': 'Number',
            '': 'Null',
            'string': 'String'
        }

    def jadn_dump(self):
        jadn = {
            'meta': self.makeMeta(),
            'types': self.makeTypes()
        }

        return self._jadnFormat(jadn, indent=2)

    def makeMeta(self):
        meta = {}

        for m in self.schema .find_all(string=lambda text: isinstance(text, Comment)):
            m = re.sub(r'(^\s|\s$)', '', m)
            if m.startswith('meta:'):
                m = re.sub('meta:\s?', '', m)
                k, v = m.split(' - ')

                try:
                    v = json.loads(v)
                except Exception as e:
                    v = re.sub(r'(^\s?|\s?$)', '', v)
                meta[k] = v

        return meta

    def makeTypes(self):
        types = []

        for t in self.schema.find_all('define'):
            tmp_type = [t['name']]
            children = list(t.children)
            if isinstance(children[0], Comment):
                com, opts = self._loadCommentDefs(children[0].string)

                if 'type' in opts:
                    tmp_type.append(opts['type'])

                if 'options' in opts:
                    tmp_type.append(self._opts_d2s(opts['options']))
                else:
                    tmp_type.append([])

                tmp_type.append(com)
                children = children[1:]

            if children[0].name == 'data':
                tmp_type.insert(1, self._fieldType(children[0]['type']))

            else:
                c = self._children(children)
                tmp_type.append(c)

            types.append(tmp_type)

        return types

    def formatStr(self, s):
        """
        Formats the string for use in schema
        :param s: string to format
        :type s: str
        :return: formatted string
        :rtype str
        """
        if s == '*':
            return 'unknown'
        else:
            return re.sub(r'[\- ]', '_', s)

    def _children(self, childList):
        tmp_defs = []
        tmp_count = 1
        for child in childList:
            # print(child)
            if child.name == 'interleave':
                # print('Interleave')
                c = self._children(list(child.children))
                tmp_defs.extend(c)

            elif child.name == 'optional':
                # print('Optional')
                c = self._children(list(child.children))
                tmp_defs.extend(c)

            elif child.name == 'choice':
                # print('Optional')
                c = self._children(list(child.children))
                tmp_defs.extend(c)

            elif child.name == 'element':
                tmp_def = [child['name']]
                comment = child.find_all(string=lambda text: isinstance(text, Comment))
                ref_data = child.findAll(['ref', 'data', 'text'])

                if len(comment) == 1 and len(ref_data) == 1:
                    com, opts = self._loadCommentDefs(comment[0].string)
                    ref_data = ref_data[0]

                    # print('Comment: {}'.format(com))
                    # print('Options: {}'.format(opts))
                    if 'field' in opts:
                        tmp_def.insert(0, opts['field'])

                    fieldType = ref_data['type'] if ref_data.name == 'data' else (ref_data['name'] if ref_data.name == 'ref' else 'string')

                    if 'type' in opts:
                        fieldTypeTmp = self.formatStr(opts['type'])
                        fieldType = fieldType if fieldTypeTmp == fieldType else fieldTypeTmp

                    tmp_def.append(self._fieldType(fieldType))

                    if 'options' in opts:
                        tmp_def.append(self._opts_d2s(opts['options'], field=True))
                    else:
                        tmp_def.append([])

                    tmp_def.append(com)

                else:
                    print(child.name)
                    print('Comment: {}'.format(comment))
                    print('Options: {}'.format(ref_data))
                    print('Issues with schema formatting')

                # print('Append Element')
                tmp_defs.append(tmp_def)

            elif child.name == 'value':
                def_name = child.parent.parent['name']
                tmp_def = []
                comment = child.find_all(string=lambda text: isinstance(text, Comment))
                if len(comment) == 1:
                    com, opts = self._loadCommentDefs(comment[0].string)

                    if 'field' in opts:
                        tmp_def.append(opts['field'])

                    else:
                        tmp_def.append(tmp_count)

                    val = child.text.strip()
                    if re.match(r'^Unknown_{}_'.format(def_name), val):
                        val = ''

                    tmp_def.append(val)
                    tmp_def.append(com)

                else:
                    tmp_def.append([tmp_count, child.text.strip(), ''])

                tmp_defs.append(tmp_def)

            else:
                print(child.name)
                pass
        tmp_count += 1
        # print('')

        return tmp_defs

    def _fieldType(self, f):
        """
        Determines the field type for the schema
        :param f: current type
        :return: type mapped to the schema
        :rtype str
        """
        rtn = self._fieldMap.get(f, f)

        return rtn

    def _loadCommentDefs(self, comStr):
        com = re.sub(r'(^\s?|\s?$)', '', comStr)
        com = re.sub(r'\s?#jadn_opts:\s*?\{.*?\}+', '', com)
        opts = re.sub(r'.*?#jadn_opts:\s*?(?P<opts>\{.*?\}+)', '\g<opts>', comStr)

        try:
            opts = json.loads(opts)
        except Exception as e:
            print('Err: {}'.format(opts))
            opts = {}

        return com, opts

    def _jadnFormat(self, jadn, indent=1):
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
                defs = "[\n{defs}\n{idn}{idn}]".format(idn=idn, defs=re.sub(re.compile(r'^', re.MULTILINE), '{idn}'.format(idn=idn*3), defs))

            type_defs.append("\n{idn}{idn}[{header}, {defs}]".format(
                idn=idn,
                header=', '.join(header),
                defs=defs
            ))

        types = "[{obj}\n{idn}]".format(idn=idn, obj=','.join(type_defs))

        return "{{\n{meta},\n{idn}\"types\": {types}\n}}".format(idn=idn, meta=meta, types=types)

    def _opts_d2s(self, opts, field=False):     # TODO: Refactor to use TYPE_OPTIONS / FIELD_OPTIONS as above
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
            elif k == "aetype":
                ostr.append("#{}".format(v))

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


def relax2jadn_dumps(relax):
    """
    Produce jadn schema from relax schema
    :arg relax: JADN Schema to convert
    :type relax: str
    :return: jadn schema
    :rtype str
    """
    return Relax2Jadn(relax).jadn_dump()


def relax2jadn_dump(relax, fname, source=""):
    with open(fname, "w") as f:
        if source:
            f.write("-- Generated from " + source + ", " + datetime.ctime(datetime.now()) + "\n\n")
        f.write(relax2jadn_dumps(relax))
