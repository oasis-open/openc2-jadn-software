import datetime
import json
import re

from ..codec.codec_utils import fopts_s2d, topts_s2d
from ..utils import Utils


class JADNtoProto3(object):
    def __init__(self, jadn):
        """
        Schema Converter for JADN to ProtoBuf3
        :param jadn: str or dict of the JADN schema
        :type jadn: str or dict
        """
        if type(jadn) is str:
            try:
                jadn = json.loads(jadn)
            except Exception as e:
                raise e
        elif type(jadn) is dict:
            pass

        else:
            raise TypeError('JADN improperly formatted')

        self.indent = '  '

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

        self._imports = []
        self._meta = jadn['meta'] or []
        self._types = []
        self._custom = []
        self._customFields = []  # [t[0] for t in self._types]

        for t in jadn['types']:
            if t[1] in self._structFormats.keys():
                self._types.append(t)
                self._customFields.append(t[0])
            else:
                self._custom.append(t)

    def proto_dump(self):
        """
        Converts the JADN schema to Protobuf3
        :return: Protobuf3 schema
        :rtype str
        """
        return '{header}{imports}{defs}\n/* JADN Custom Fields\n[\n{jadn_fields}\n]\n*/'.format(
            idn=self.indent,
            header=self.makeHeader(),
            defs=self.makeStructures(),
            imports=''.join(['import \"{}\";\n'.format(i) for i in self._imports]),
            jadn_fields=',\n'.join([self.indent+f.__str__() for f in Utils.defaultDecode(self._custom)])
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
        :rtype str
        """
        header = list([
            'syntax = "proto3";',
            '',
            'package {};'.format(self._meta['module'] or 'ProtoBuf_Schema'),
            '',
            '/* meta'
        ])

        header.extend([' * {} - {}'.format(k, v) for k, v in self._meta.items()])

        header.append('*/')

        return '\n'.join(header) + '\n\n'

    def makeStructures(self):
        """
        Create the type definitions for the schema
        :return: type definitions for the schema
        :rtype str
        """
        tmp = ''
        for t in self._types:
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
        rtn = 'string'
        if re.search(r'(datetime|date|time)', f):
            if 'google/protobuf/timestamp.proto' not in self._imports:
                self._imports.append('google/protobuf/timestamp.proto')
            rtn = 'google.protobuf.Timestamp'

        if f in self._customFields:
            rtn = self.formatStr(f)

        elif f in self._fieldMap.keys():
            rtn = self.formatStr(self._fieldMap.get(f, f))
        return rtn

    # Structure Formats
    def _formatRecord(self, itm):
        """
        Formats records for the given schema type
        :param itm: record to format
        :return: formatted record
        :rtype str
        """
        lines = []
        for l in itm[-1]:
            opts = {'type': l[2]}
            if len(l[-2]) > 0: opts['options'] = fopts_s2d(l[-2])

            lines.append('{idn}{type} {name} = {num}; // {com}#jadn_opts:{opts}\n'.format(
                idn=self.indent,
                type=self._fieldType(l[2]),
                name=self.formatStr(l[1]),
                num=l[0],
                com='' if l[-1] == '' else l[-1]+' ',
                opts=json.dumps(opts)
            ))

        opts = {'type': itm[1]}
        if len(itm[2]) > 0: opts['options'] = topts_s2d(itm[2])

        return '\nmessage {name} {{ // {com}#jadn_opts:{opts}\n{req}}}\n'.format(
            name=self.formatStr(itm[0]),
            req=''.join(lines),
            com='' if itm[-2] == '' else itm[-2] + ' ',
            opts=json.dumps(opts)
        )

    def _formatChoice(self, itm):
        """
        Formats choice for the given schema type
        :param itm: choice to format
        :return: formatted choice
        :rtype str
        """
        lines = []
        for l in itm[-1]:
            opts = {'type': l[2]}
            if len(l[-2]) > 0: opts['options'] = fopts_s2d(l[-2])

            lines.append('{idn}{type} {name} = {num}; // {com}#jadn_opts:{opts}\n'.format(
                idn=self.indent,
                type=self._fieldType(l[2]),
                name=self.formatStr(l[1]),
                num=l[0],
                com='' if l[-1] == '' else l[-1]+' ',
                opts=json.dumps(opts)
            ))

        opts = {'type': itm[1]}
        if len(itm[2]) > 0: opts['options'] = topts_s2d(itm[2])

        return '\noneof {name} {{ // {com}#jadn_opts:{opts}\n{req}}}\n'.format(
            idn=self.indent,
            name=self.formatStr(itm[0]),
            com='' if itm[-2] == '' else itm[-2] + ' ',
            opts=json.dumps(opts),
            req=''.join(lines)
        )

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
        lines = []
        default = True
        for l in itm[-1]:
            if l[0] == 0: default = False
            lines.append('{idn}{name} = {num};{com}\n'.format(
                idn=self.indent,
                name=self.formatStr(l[1] or 'Unknown_{}_{}'.format(self.formatStr(itm[0]), l[0])),
                num=l[0],
                com='' if l[-1] == '' else ' // {}'.format(l[-1])
            ))

        opts = {'type': itm[1]}
        if len(itm[2]) > 0: opts['options'] = topts_s2d(itm[2])

        return '\nenum {name} {{ // {com}#jadn_opts:{opts}\n{default}{enum}}}\n'.format(
            idn=self.indent,
            name=self.formatStr(itm[0]),
            com='' if itm[-2] == '' else itm[-2] + ' ',
            opts=json.dumps(opts),
            default='{}Unknown_{} = 0; // required starting enum number for protobuf3\n'.format(self.indent, itm[0].replace('-', '_')) if default else '',
            enum=''.join(lines)
        )

    def _formatArray(self, itm):  # TODO: what should this do??
        """
        Formats array for the given schema type
        :param itm: array to format
        :return: formatted array
        :rtype str
        """
        print('Array: {}'.format(itm))
        return ''

    def _formatArrayOf(self, itm):  # TODO: what should this do??
        """
        Formats arrayof for the given schema type
        :param itm: arrayof to format
        :return: formatted arrayof
        :rtype str
        """
        field_opts = topts_s2d(itm[2])

        print('ArrayOf {aetype} - min:{min}, max:{max}'.format(**field_opts))

        return ''


def proto_dumps(jadn):
    """
    Produce Protobuf3 schema from JADN schema
    :arg jadn: JADN Schema to convert
    :type jadn: str or dict
    :return: Protobuf3 schema
    :rtype str
    """
    return JADNtoProto3(jadn).proto_dump()


def proto_dump(jadn, fname, source=""):
    with open(fname, "w") as f:
        if source:
            f.write("-- Generated from " + source + ", " + datetime.ctime(datetime.now()) + "\n\n")
        f.write(proto_dumps(jadn))
