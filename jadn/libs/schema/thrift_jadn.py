import json
import re

from datetime import datetime
from ..utils import toStr, Utils


class Thrift2JADN(object):
    def __init__(self, thrift):
        """
        Schema Converter for Thrift to JADN
        :param thrift: str or dict of the JADN schema
        :type thrift: str
        """
        self._thrift = thrift.replace('\r', '')  # replace windows line terminators with unix style
        self.indent = '  '

        self._fieldMap = {
            'enum': 'Enumerated',
            'struct': 'Record',
            # primitives
            'string': 'String'
        }
        self._structs = [
            'Record',
            'Choice',
            'Map',
            'Enumerated',
            'Array',
            'ArrayOf'
        ]

        self._fieldRegex = {
            'enum': re.compile(r'(?P<name>.*?)\s+=\s+(?P<id>\d+);(\s+//\s+(?P<comment>.*))?\n?'),
            'struct': re.compile(r'(?P<id>\d+):\s+(?P<option>.*?)\s+(?P<type>.*?)\s+(?P<name>.*?);(\s+//\s+(?P<comment>.*))?\n?'),
            'array': re.compile(r'(?P<id>\d+):\s+(?P<option>.*?)\s+list\<(?P<type>.*?)\>\s+(?P<name>.*?);(\s+//\s+(?P<comment>.*))?\n?')
        }
        self._fieldRegex['arrayof'] = self._fieldRegex['array']

    def jadn_dump(self):
        """
        Converts the Thrift schema to JADN
        :return: JADN schema
        :rtype str
        """
        jadn = {
            'meta': self.makeMeta(),
            'types': self.makeTypes() + self.makeCustom()
        }

        return Utils.jadnFormat(jadn, indent=2)

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

    def makeMeta(self):
        """
        Create the header for the schema
        :return: header for schema
        :rtype dict
        """
        tmp = {}
        meta = re.search(r'\/\*\s*?meta(.*|\n)*?\*\/', toStr(self._thrift))

        if meta:
            for meta_line in meta.group().split('\n')[1:-1]:
                line = re.sub(r'^\s+\*\s+', '', meta_line).split(' - ')

                try:
                    tmp[line[0]] = json.loads(' - '.join(line[1:]))
                except Exception as e:
                    tmp[line[0]] = ' - '.join(line[1:])

        return tmp

    def makeTypes(self):
        """
        Create the type definitions for the schema
        :return: type definitions for the schema
        :rtype list
        """
        tmp = []
        for type_def in re.findall(r'^((enum|struct)(.|\n)*?^\}?$)', toStr(self._thrift), flags=re.MULTILINE):
            tmp_type = []
            def_lines = [l for l in type_def[0].split('\n') if l != '']

            if re.match(r'(.|\r?\n)*list<[\w\d]+>', type_def[0]):
                thrift_type, field_name = def_lines[0].split(r'{')[0].split()
                parts = self._fieldRegex['arrayof'].match(re.sub(r'^\s+', '', def_lines[1])).groupdict()
                com, opts = self._loadOpts(parts['comment'])

                thrift_type = list(map(lambda s: s.lower() == opts['type'].lower(), self._structs))
                thrift_type = self._structs[thrift_type.index(True)] if True in thrift_type else 'Array'

                tmp.append([field_name, thrift_type, Utils.opts_d2s(opts['options']), com])

            else:

                thrift_type, field_name = def_lines[0].split(r'{')[0].split()

                com = def_lines[0].split('//')
                com = (com[1][1:] if com[1].startswith(' ') else com[1]) if len(com) > 1 else ''

                com, opts = self._loadOpts(com)

                jadn_type = self._fieldMap.get(thrift_type, 'Record')
                jadn_type = jadn_type if jadn_type == opts.get('type', jadn_type) else opts['type']

                tmp_type.extend([
                    field_name,
                    jadn_type,
                    Utils.opts_d2s(opts.get('options', {})),  # options ??
                    com
                ])

                tmp_defs = []
                for def_var in def_lines[1:-1]:
                    def_var = re.sub(r'^\s+', '', def_var)
                    parts = self._fieldRegex.get(thrift_type, self._fieldRegex['struct']).match(def_var)
                    if parts:
                        parts = parts.groupdict()
                        parts['comment'], opts = self._loadOpts(parts['comment'])

                        if thrift_type == 'enum':
                            if parts['name'] == 'Unknown_{}'.format(field_name): continue

                            # id, name, comment
                            tmp_defs.append([
                                int(parts['id']) if parts['id'].isdigit() else parts['id'],
                                parts['name'],
                                parts['comment'] or ''
                            ])

                        elif thrift_type == 'struct':
                            field_type = self._fieldType(parts['type'])
                            field_type = field_type if field_type == opts.get('type', field_type) else opts['type']

                            # id, name, type, opts, comment
                            tmp_defs.append([
                                int(parts['id']) if parts['id'].isdigit() else parts['id'],
                                parts['name'],
                                field_type,
                                Utils.opts_d2s(opts.get('options', {}), field=True),
                                parts['comment'] or ''
                            ])

                        else:
                            print('Something...')
                            # tmp_defs.append([])
                            pass
                    else:
                        print('{} - {}'.format(thrift_type, def_var))
                        print('Something Happened....')


                tmp_type.append(tmp_defs)
                tmp.append(tmp_type)

        return tmp

    def makeCustom(self):
        customFields = re.search(r'/\* JADN Custom Fields\n(?P<custom>[\w\W]+?)\n\*/', toStr(self._thrift))
        fields = []

        if customFields:
            try:
                fields = Utils.defaultDecode(json.loads(customFields.group('custom').replace('\'', '\"')))
            except Exception as e:
                print('Custom Fields Load Error: {}'.format(e))

        return fields

    def _formatType(self, t):
        tmp = ','.join(['\n{idn}{idn}{idn}{defn}'.format(idn=self.indent, defn=td.__str__()) for td in t[-1]])

        if tmp != '':
            tmp += '\n{idn}{idn}'.format(idn=self.indent)

        return '{idn}{idn}{head}, [{defs}]]'.format(
            idn=self.indent,
            head=t[:-1].__str__()[:-1],
            defs=tmp
        ).replace('\'', '\"')

    def _fieldType(self, f):
        if re.match(r'^google', f):
            ft = 'String'
        else:
            ft = self._fieldMap.get(f, f)

        return ft

    def _loadOpts(self, com):
        c = com or ''
        com = com or ''

        com = re.sub(r'\s*?#jadn_opts:\s?{.*?}+\n?', '', com)
        if c == com:
            return com, {}

        opts = re.match(r'\s*?#jadn_opts:\s?(?P<opts>{.*?}+)\n?', c.replace(com, ''))
        if opts:
            try:
                opts = json.loads(opts.group('opts'))

            except Exception as e:
                # print('Err: {}'.format(opts))
                opts = {}
        else:
            opts = {}

        return com, opts


def thrift2jadn_dumps(thrift):
    """
    Produce jadn schema from thrift schema
    :arg thrift: Thrift Schema to convert
    :type thrift: str
    :return: jadn schema
    :rtype str
    """
    return Thrift2JADN(thrift).jadn_dump()


def thrift2jadn_dump(thrift, fname, source=""):
    with open(fname, "w") as f:
        if source:
            f.write("-- Generated from " + source + ", " + datetime.ctime(datetime.now()) + "\n\n")
        f.write(thrift2jadn_dumps(thrift))