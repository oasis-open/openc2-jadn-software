import json
import re


class JADNtoProto3(object):
    def __init__(self, jadn):
        """
        Schema Converter for JADN to ProtoBuf3
        :param jadn: str or dict of the JADN schema
        :type jadn: str
        """
        if type(jadn) is str:
            try:
                jadn = json.loads(jadn)
            except Exception as e:
                raise e

            self._meta = jadn['meta'] or None
            self._types = jadn['types'] or None

        elif type(jadn) is dict:
            self._meta = jadn['meta'] or None
            self._types = jadn['types'] or None

        else:
            raise TypeError('JADN improperly formatted')

        self._imports = []
        self.indent = '    '

        self._fields = {t[0]: t[1] for t in self._types if len(t) == 4}
        self._fieldTypes = [t[0] for t in self._types if len(t) == 5]
        self._fieldMap = {
            'Binary': 'string',
            'Boolean': 'bool',
            'Integer': 'int64',
            'Number': 'string',
            'Null': 'string',
            'String': 'string'
        }
        self._structFormats = {
            'Record': self._formatRecord,
            'Choice': self._formatChoice,
            'Map': self._formatMap,
            'Enumerated': self._formatEnumerated,
            'Array': self._formatArray,
            'ArrayOf': self._formatArrayOf,
        }

    def proto_dump(self):
        """
        Converts the JADN schema to Protobuf3
        :return: Protobuf3 schema
        :rtype str
        """
        return '{header}{imports}{defs}'.format(**{
            'header': self.makeHeader(),
            'defs': self.makeStructures(),
            'imports': ''.join(['import \"{}\";\n'.format(i) for i in self._imports])

        })

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
        :rtype str
        """
        header = list([
            'syntax = "proto3";',
            '',
            'package {};'.format(self._meta['module'] or 'ProtoBuf_Schema'),
            ''
        ])

        header.extend(['// {} - {}'.format(k, v) for k, v in self._meta.items()])

        header.append('')

        return '\n'.join(header) + '\n'

    def makeStructures(self):
        """
        Create the type definitions for the schema
        :return: type definitions for the schema
        :rtype str
        """
        tmp = ''
        for t in self._types:
            if len(t) == 5:
                # print('type - {}'.format(t[:-1]))
                df = self._structFormats.get(t[1], None)

                if df is not None and t[1] in ['Record', 'Enumerated', 'Map']:
                    tmp += df(t)
                elif df is not None:
                    tmp += self._wrapAsRecord(df(t))

        return tmp

    def _wrapAsRecord(self, itm):
        """
        wraps the given item as a record for the schema
        :param itm: item to wrap
        :type s: str
        :return: item wrapped as a record for hte schema
        :rtype str
        """
        lines = itm.split('\n')[1:-1]
        if len(lines) > 1:
            n = re.search(r'\s[\w\d\_]+\s', lines[0]).group()[1:-1]
            tmp = "\nmessage {} {{\n".format(self.formatStr(n))
            for l in lines:
                tmp += '{}{}\n'.format(self.indent, l)
            tmp += '}\n'
            return tmp
        return ''

    def _fieldType(self, f):
        """
        Determines the field type for the schema
        :param f: current type
        :return: type mapped to the schema
        :rtype str
        """
        if re.search(r'(datetime|date|time)', f):
            if 'google/protobuf/timestamp.proto' not in self._imports:
                self._imports.append('google/protobuf/timestamp.proto')
            return 'google.protobuf.Timestamp'
        elif f not in self._fieldTypes:
            return 'string'
        # print(f)
        return self.formatStr(self._fieldMap.get(self._fields.get(f, f), f))

    # Structure Formats
    def _formatRecord(self, itm):
        """
        Formats records for the given schema type
        :param itm: record to format
        :return: formatted record
        :rtype str
        """
        tmp = "\nmessage {} {{".format(self.formatStr(itm[0]))
        tmp += '\n' if itm[-2] == '' else ' // {}\n'.format(itm[-2])
        for l in itm[-1]:
            tmp += '{}{} {} = {};'.format(self.indent, self._fieldType(l[2]), self.formatStr(l[1]), l[0])
            tmp += '\n' if l[-1] == '' else ' // {}\n'.format(l[-1])
        tmp += "}\n"

        return tmp

    def _formatChoice(self, itm):
        """
        Formats choice for the given schema type
        :param itm: choice to format
        :return: formatted choice
        :rtype str
        """
        tmp = '\n'
        tmp += "oneof {} {{".format(self.formatStr(itm[0]))
        tmp += '\n' if itm[-2] == '' else ' // {}\n'.format(itm[-2])
        for l in itm[-1]:
            tmp += '{}{} {} = {};'.format(self.indent, self._fieldType(l[2]), self.formatStr(l[1]), l[0])
            tmp += '\n' if l[-1] == '' else ' // {}\n'.format(l[-1])
        tmp += '}\n'
        return tmp

    def _formatMap(self, itm):
        """
        Formats map for the given schema type
        :param itm: map to format
        :return: formatted map
        :rtype str
        """
        return self._formatRecord(itm)

    def _formatEnumerated(self, itm):
        """
        Formats enum for the given schema type
        :param itm: enum to format
        :return: formatted enum
        :rtype str
        """
        tmp = '\nenum {} {{'.format(self.formatStr(itm[0]))
        tmp += '\n' if itm[-2] == '' else ' // {}\n'.format(itm[-2])

        lines = []
        default = True
        for l in itm[-1]:
            if l[0] == 0:
                default = False
            n = self.formatStr(l[1] or 'Unknown_{}_{}'.format(self.formatStr(itm[0]), l[0]))
            ltmp = '{}{} = {};'.format(self.indent, n, l[0])
            ltmp += '\n' if l[-1] == '' else ' // {}\n'.format(l[-1])
            lines.append(ltmp)

        if default:
            tmp += '{}Unknown_{} = 0; // required starting enum number for protobuf3\n'.format(self.indent, itm[0].replace('-', '_'))
        tmp += ''.join(lines)

        tmp += "}\n"
        return tmp

    def _formatArray(self, itm):
        """
        Formats array for the given schema type
        :param itm: array to format
        :return: formatted array
        :rtype str
        """
        return ''

    def _formatArrayOf(self, itm):
        """
        Formats arrayof for the given schema type
        :param itm: arrayof to format
        :return: formatted arrayof
        :rtype str
        """
        return ''


class JADNtoProto2(object):  # TODO: Validate for Protobuf2
    def __init__(self, jadn):
        """
        Schema Converter for JADN to ProtoBuf3
        :param jadn: str or dict of the JADN schema
        :type jadn: str
        """
        if type(jadn) is str:
            try:
                jadn = json.loads(jadn)
            except Exception as e:
                raise e

            self._meta = jadn['meta'] or None
            self._types = jadn['types'] or None

        elif type(jadn) is dict:
            self._meta = jadn['meta'] or None
            self._types = jadn['types'] or None

        else:
            raise TypeError('JADN improperly formatted')

        self._imports = []
        self.indent = '    '

        self._fields = {t[0]: t[1] for t in self._types if len(t) == 4}
        self._fieldTypes = [t[0] for t in self._types if len(t) == 5]
        self._fieldMap = {
            'Binary': 'string',
            'Boolean': 'bool',
            'Integer': 'int64',
            'Number': 'string',
            'Null': 'string',
            'String': 'string'
        }
        self._structFormats = {
            'Record': self._formatRecord,
            'Choice': self._formatChoice,
            'Map': self._formatMap,
            'Enumerated': self._formatEnumerated,
            'Array': self._formatArray,
            'ArrayOf': self._formatArrayOf,
        }

    def proto_dump(self):
        """
        Converts the JADN schema to Protobuf3
        :return: Protobuf3 schema
        :rtype str
        """
        return '{header}{imports}{defs}'.format(**{
            'header': self.makeHeader(),
            'defs': self.makeStructures(),
            'imports': ''.join(['import \"{}\";\n'.format(i) for i in self._imports])

        })

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
        :rtype str
        """
        header = list([
            'syntax = "proto3";',
            '',
            'package {};'.format(self._meta['module'] or 'ProtoBuf_Schema'),
            ''
        ])

        header.extend(['// {} - {}'.format(k, v) for k, v in self._meta.items()])

        header.append('')

        return '\n'.join(header) + '\n'

    def makeStructures(self):
        """
        Create the type definitions for the schema
        :return: type definitions for the schema
        :rtype str
        """
        tmp = ''
        for t in self._types:
            if len(t) == 5:
                # print('type - {}'.format(t[:-1]))
                df = self._structFormats.get(t[1], None)

                if df is not None and t[1] in ['Record', 'Enumerated', 'Map']:
                    tmp += df(t)
                elif df is not None:
                    tmp += self._wrapAsRecord(df(t))

        return tmp

    def _wrapAsRecord(self, itm):
        """
        wraps the given item as a record for the schema
        :param itm: item to wrap
        :type s: str
        :return: item wrapped as a record for hte schema
        :rtype str
        """
        lines = itm.split('\n')[1:-1]
        if len(lines) > 1:
            n = re.search(r'\s[\w\d\_]+\s', lines[0]).group()[1:-1]
            tmp = "\nmessage {} {{\n".format(self.formatStr(n))
            for l in lines:
                tmp += '{}{}\n'.format(self.indent, l)
            tmp += '}\n'
            return tmp
        return ''

    def _fieldType(self, f):
        """
        Determines the field type for the schema
        :param f: current type
        :return: type mapped to the schema
        :rtype str
        """
        if re.search(r'(datetime|date|time)', f):
            if 'google/protobuf/timestamp.proto' not in self._imports:
                self._imports.append('google/protobuf/timestamp.proto')
            return 'google.protobuf.Timestamp'
        elif f not in self._fieldTypes:
            return 'string'
        # print(f)
        return self.formatStr(self._fieldMap.get(self._fields.get(f, f), f))

    # Structure Formats
    def _formatRecord(self, itm):
        """
        Formats records for the given schema type
        :param itm: record to format
        :return: formatted record
        :rtype str
        """
        tmp = "\nmessage {} {{".format(self.formatStr(itm[0]))
        tmp += '\n' if itm[-2] == '' else ' // {}\n'.format(itm[-2])
        for l in itm[-1]:
            tmp += '{}{} {} = {};'.format(self.indent, self._fieldType(l[2]), self.formatStr(l[1]), l[0])
            tmp += '\n' if l[-1] == '' else ' // {}\n'.format(l[-1])
        tmp += "}\n"

        return tmp

    def _formatChoice(self, itm):
        """
        Formats choice for the given schema type
        :param itm: choice to format
        :return: formatted choice
        :rtype str
        """
        tmp = '\n'
        tmp += "oneof {} {{".format(self.formatStr(itm[0]))
        tmp += '\n' if itm[-2] == '' else ' // {}\n'.format(itm[-2])
        for l in itm[-1]:
            tmp += '{}{} {} = {};'.format(self.indent, self._fieldType(l[2]), self.formatStr(l[1]), l[0])
            tmp += '\n' if l[-1] == '' else ' // {}\n'.format(l[-1])
        tmp += '}\n'
        return tmp

    def _formatMap(self, itm):
        """
        Formats map for the given schema type
        :param itm: map to format
        :return: formatted map
        :rtype str
        """
        return self._formatRecord(itm)

    def _formatEnumerated(self, itm):
        """
        Formats enum for the given schema type
        :param itm: enum to format
        :return: formatted enum
        :rtype str
        """
        tmp = '\nenum {} {{'.format(self.formatStr(itm[0]))
        tmp += '\n' if itm[-2] == '' else ' // {}\n'.format(itm[-2])

        lines = []
        default = True
        for l in itm[-1]:
            if l[0] == 0:
                default = False
            n = self.formatStr(l[1] or 'Unknown_{}_{}'.format(self.formatStr(itm[0]), l[0]))
            ltmp = '{}{} = {};'.format(self.indent, n, l[0])
            ltmp += '\n' if l[-1] == '' else ' // {}\n'.format(l[-1])
            lines.append(ltmp)

        if default:
            tmp += '{}Unknown_{} = 0; // required starting enum number for protobuf3\n'.format(self.indent, itm[0].replace('-', '_'))
        tmp += ''.join(lines)

        tmp += "}\n"
        return tmp

    def _formatArray(self, itm):
        """
        Formats array for the given schema type
        :param itm: array to format
        :return: formatted array
        :rtype str
        """
        return ''

    def _formatArrayOf(self, itm):
        """
        Formats arrayof for the given schema type
        :param itm: arrayof to format
        :return: formatted arrayof
        :rtype str
        """
        return ''


class Proto3toJADN(object):
    def __init__(self):
        pass

    def jadn_dump(self):
        return ''


class Proto2toJADN(object):
    def __init__(self):
        pass

    def jadn_dump(self):
        return ''
