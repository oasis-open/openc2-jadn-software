import json
import re

from datetime import datetime

from ..utils import toStr, Utils


class Proto2JADN(object):
    def __init__(self, proto):
        """
        Schema Converter for ProtoBuf3 to JADN
        :param proto: str or dict of the JADN schema
        :type proto: str
        """
        self._proto = toStr(proto).replace('\r', '')  # replace windows line terminators with unix style
        self.indent = '  '

        self._fieldMap = {
            'enum': 'Enumerated',
            'message': 'Record',
            'oneof': 'Choice',
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
            'message': re.compile(r'(?P<type>.*?)\s+(?P<name>.*?)\s+=\s+(?P<id>\d+);(\s+//\s+(?P<comment>.*))?\n?'),
            'array': re.compile(r'\s+(?P<repeat>.*?)\s+(?P<type>.*?)\s+(?P<name>.*?)\s+=\s+(?P<id>\d+);(\s+//\s+(?P<comment>.*))?\n?')
        }
        self._fieldRegex['oneof'] = self._fieldRegex['message']
        self._fieldRegex['arrayof'] = self._fieldRegex['array']

    def jadn_dump(self):
        """
        Converts the Protobuf3 schema to JADN
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
        # meta = re.search(r'\s?\*\s*?meta(.*|\n)*?\*\/', toStr(self._proto))

        for line in re.findall(r'\s+\*\s+meta:\s+.*?\n', toStr(self._proto), flags=re.MULTILINE):
            line = re.sub(r'(\s+\*\s+meta:\s+|\n)', '', line).split(' - ')

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
        for type_def in re.findall(r'^((enum|message)(.|\n)*?^\}?$)', toStr(self._proto), flags=re.MULTILINE):
            tmp_type = []
            def_lines = [l for l in type_def[0].split('\n') if l != '']

            if re.match(r'.*{[\r\n]\s+(repeated).*\n}', type_def[0]):
                proto_type, field_name = def_lines[0].split(r'{')[0].split()
                parts = self._fieldRegex['arrayof'].match(def_lines[1]).groupdict()
                com, opts = self._loadOpts(parts['comment'])

                proto_type = list(map(lambda s: s.lower() == opts['type'].lower(), self._structs))
                proto_type = self._structs[proto_type.index(True)] if True in proto_type else 'Array'

                tmp.append([field_name, proto_type, Utils.opts_d2s(opts['options']), com])

            else:
                if re.match(r'^\s+(oneof)', def_lines[1]):
                    def_lines = def_lines[1:-1]

                proto_type, field_name = def_lines[0].split(r'{')[0].split()

                com = def_lines[0].split('//')
                com = (com[1][1:] if com[1].startswith(' ') else com[1]) if len(com) > 1 else ''

                com, opts = self._loadOpts(com)

                jadn_type = self._fieldMap.get(proto_type, 'Record')
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
                    parts = self._fieldRegex.get(proto_type, self._fieldRegex['message']).match(def_var)

                    if parts:
                        parts = parts.groupdict()
                        parts['comment'], opts = self._loadOpts(parts['comment'])

                        if proto_type == 'enum':
                            if parts['name'] == 'Unknown_{}'.format(field_name): continue

                            # id, name, comment
                            tmp_defs.append([
                                int(parts['id']) if parts['id'].isdigit() else parts['id'],
                                parts['name'],
                                parts['comment'] or ''
                            ])

                        elif proto_type in ['message', 'oneof']:
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
                        print('{} - {}'.format(proto_type, def_var))
                        print('Something Happened....')

                tmp_type.append(tmp_defs)
                tmp.append(tmp_type)

        return tmp

    def makeCustom(self):
        customFields = re.search(r'/\* JADN Custom Fields\n(?P<custom>[\w\W]+?)\n\*/', toStr(self._proto))
        fields = []

        if customFields:
            try:
                fields = Utils.defaultDecode(json.loads(customFields.group('custom').replace('\'', '\"')))
            except Exception as e:
                print('Custom Fields Load Error: {}'.format(e))

        return fields

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


def proto2jadn_dumps(proto):
    """
    Produce jadn schema from proto3 schema
    :arg proto: Proto3 Schema to convert
    :type proto: str
    :return: jadn schema
    :rtype str
    """
    return Proto2JADN(proto).jadn_dump()


def proto2jadn_dump(proto, fname, source=""):
    with open(fname, "w") as f:
        if source:
            f.write("-- Generated from " + source + ", " + datetime.ctime(datetime.now()) + "\n\n")
        f.write(proto2jadn_dumps(proto))
