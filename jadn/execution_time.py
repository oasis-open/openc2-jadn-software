import json
import os
import re
import time

from arpeggio_proto_test import ProtoRules, ProtoVisitor
from arpeggio_thrift_test import ThriftRules, ThriftVisitor

from arpeggio import visit_parse_tree, ParserPython

from libs.utils import toStr, Utils


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


class Thrift2JADN(object):
    def __init__(self, thrift):
        """
        Schema Converter for Thrift to JADN
        :param thrift: str or dict of the JADN schema
        :type thrift: str
        """
        self._thrift = toStr(thrift).replace('\r', '')  # replace windows line terminators with unix style
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
                        if parts['name'] == 'unknown':
                            parts['name'] = '*'

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
                opts = {}
        else:
            opts = {}

        return com, opts


if __name__ == '__main__':
    schemaFiles = {
        'proto': '',
        'thrift': ''

    }

    for schema in schemaFiles:
        schemaFiles[schema] = toStr(open(os.path.join('.', 'schema_gen_test', 'openc2-wd06.{}'.format(schema)), 'rb').read())

    testResults = {
        'proto': {
            'arpeggio': [],
            'original': []
        },
        'thrift': {
            'arpeggio': [],
            'original': []
        }
    }

    iterations = 250
    for i in range(1, iterations + 1):
        if i % 10 == 0:
            print('Loop {}, {} remaining'.format(i, iterations - i))

        # Arpeggio - Proto
        start_time = time.time()
        parser = ParserPython(ProtoRules)
        parse_tree = parser.parse(schemaFiles['proto'])
        result = visit_parse_tree(parse_tree, ProtoVisitor())
        jadn = Utils.jadnFormat(result, indent=2)
        total_time = time.time() - start_time
        testResults['proto']['arpeggio'].append(total_time)

        # Original - Proto
        start_time = time.time()
        jadn = Proto2JADN(schemaFiles['proto']).jadn_dump()
        total_time = time.time() - start_time
        testResults['proto']['original'].append(total_time)

        # Arpeggio - Proto
        start_time = time.time()
        parser = ParserPython(ThriftRules)
        parse_tree = parser.parse(schemaFiles['thrift'])
        result = visit_parse_tree(parse_tree, ThriftVisitor())
        jadn = Utils.jadnFormat(result, indent=2)
        total_time = time.time() - start_time
        testResults['thrift']['arpeggio'].append(total_time)

        # Original - Proto
        start_time = time.time()
        jadn = Thrift2JADN(schemaFiles['thrift']).jadn_dump()
        total_time = time.time() - start_time
        testResults['thrift']['original'].append(total_time)

    print('')

    for form, tests in testResults.items():
        print(form)
        for test, results in tests.items():
            print('- {}'.format(test))
            print('-- Average: {:0.04f}'.format(sum(results) / len(results)))
            print('-- Shortest: {:0.04f}'.format(min(results)))
            print('-- Longest: {:0.04f}'.format(max(results)))

        print('')
