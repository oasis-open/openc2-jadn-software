import json
import re

from ..utils import Utils


class Proto3toJADN(object):
    def __init__(self, proto):
        """
        Schema Converter for ProtoBuf3 to JADN
        :param proto: str or dict of the JADN schema
        :type proto: str
        """
        self._proto = proto
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
            'message': re.compile(r'(?P<type>.*?)\s+(?P<name>.*?)\s+=\s+(?P<id>\d+);(\s+//\s+(?P<comment>.*))?\n?')
        }
        self._fieldRegex['oneof'] = self._fieldRegex['message']

    def jadn_dump(self):
        """
        Converts the Protobuf3 schema to JADN
        :return: JADN schema
        :rtype str
        """
        meta = "{idn}\"meta\": {{\n{meta}\n{idn}}}".format(
            idn=self.indent,
            meta=',\n'.join(["{idn}{idn}\"{mk}\": \"{mv}\"".format(idn=self.indent, mk=k, mv=v) for k, v in self.makeHeader().items()])
        )

        types = "[\n{obj},\n{custom}\n{idn}]".format(
            idn=self.indent,
            obj=',\n'.join([
                self._formatType(t) for t in self.makeTypes()
            ]),
            custom=',\n'.join([
                '{idn}{idn}{field}'.format(idn=self.indent, field=f.__str__().replace('\'', '\"')) for f in self.makeCustom()
            ])
        )

        return "{{\n{meta},\n{idn}\"types\": {types}\n}}".format(
            idn=self.indent,
            meta=meta,
            types=types
        )

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

    def makeHeader(self):
        """
        Create the header for the schema
        :return: header for schema
        :rtype dict
        """
        tmp = {}
        meta = re.search(r'/\* meta[\n\w\d\-*. ]+\*/', self._proto)
        if meta:
            for meta_line in meta.group().split('\n')[1:-1]:
                line = re.sub(r'^\s+\*\s+', '', meta_line).split(' - ')
                tmp[line[0]] = ' - '.join(line[1:])

        return tmp

    def makeTypes(self):
        """
        Create the type definitions for the schema
        :return: type definitions for the schema
        :rtype list
        """
        tmp = []
        for type_def in re.findall(r'^((enum|message)(.|\n)*?^\}$)', self._proto, flags=re.MULTILINE):
            tmp_type = []
            def_lines = type_def[0].split('\n')
            if re.match(r'^\s+(oneof)', def_lines[1]):
                def_lines = def_lines[1:-1]

            proto_type, field_name = def_lines[0].split(r'{')[0].split()

            c = def_lines[0].split('//')
            c = (c[1][1:] if c[1].startswith(' ') else c[1]) if len(c) > 1 else ''
            opts, c = self._loadOpts(c)

            jadn_type = self._fieldMap.get(proto_type, 'Record')
            jadn_type = jadn_type if jadn_type == opts.get('type', jadn_type) else opts['type']

            tmp_type.extend([
                field_name,
                jadn_type,
                opts.get('options', []),  # options ??
                c
            ])

            tmp_defs = []
            for def_var in def_lines[1:-1]:
                def_var = re.sub(r'^\s+', '', def_var)
                parts = self._fieldRegex.get(proto_type, self._fieldRegex['message']).match(def_var)

                if parts:
                    parts = parts.groupdict()
                    opts, parts['comment'] = self._loadOpts(parts['comment'])

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
                            opts.get('options', []),
                            parts['comment'] or ''
                        ])

                    else:
                        # tmp_defs.append([])
                        pass
                else:
                    print('{} - {}'.format(proto_type, def_var))
                    print('Something Happened....')

            tmp_type.append(tmp_defs)
            tmp.append(tmp_type)
        return tmp

    def makeCustom(self):
        customFields = re.search(r'/\* JADN Custom Fields\n(?P<custom>[\w\W]+?)\n\*/', self._proto)

        if customFields:
            try:
                fields = Utils.defaultDecode(json.loads(customFields.group('custom').replace('\'', '\"')))
            except Exception as e:
                fields = []
                print('oops....')

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
        comment = re.sub(r'\s?#jadn_opts:(?P<opts>{.*?})\n?', '', c)
        if c == comment:
            return {}, comment

        opts = re.match(r'\s*?#jadn_opts:(?P<opts>{.*?})\n?', c.replace(comment, ''))
        if opts:
            try:
                opts = json.loads(opts.group('opts'))
                opts['type'] = str(opts['type'])
                if 'options' in opts: opts['options'] = [str(o) for o in opts['options']]
            except Exception:
                print('oops...')
                opts = {}
        else:
            opts = {}

        return opts, comment
