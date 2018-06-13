import datetime
import json
import re

from ..codec.codec_utils import fopts_s2d, topts_s2d
from ..utils import Utils


class JADNtoThrift(object):
    def __init__(self, jadn):
        """
        Schema Converter for JADN to thrift
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

        self.indent = '    '

        self._fieldMap = {
            'Binary': 'binary',
            'Boolean': 'bool',
            'Integer': 'i64',
            'Number': 'double',
            'Null': 'null',
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

    def thrift_dump(self):
        """
        Converts the JADN schema to Thrift
        :return: thrift schema
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
            '/*'
        ])

        header.extend([' * meta: {} - {}'.format(k, re.sub(r'(^\"|\"$)', '', json.dumps(Utils.defaultDecode(v)))) for k, v in self._meta.items()])

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

            if df is not None:
                tmp += df(t)

        return tmp

    def _fieldType(self, f):
        """
        Determines the field type for the schema
        :param f: current type
        :return: type mapped to the schema
        :rtype str
        """
        if f in self._customFields:
            rtn = self.formatStr(f)

        elif f in self._fieldMap.keys():
            rtn = self.formatStr(self._fieldMap.get(f, f))

        else:
            rtn = 'string'
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
            if len(l[-2]) > 0:
                opts['options'] = fopts_s2d(l[-2])
                lines.append('{idn}{num}: {choice} {type} {name}; // {com}#jadn_opts:{opts}\n'.format(
                    idn=self.indent,
                    choice='optional',
                    type=self._fieldType(l[2]),
                    name=self.formatStr(l[1]),
                    num=l[0],
                    com='' if l[-1] == '' else l[-1]+' ',
                    opts=json.dumps(opts)
                ))
            else:
                lines.append('{idn}{num}: {choice} {type} {name}; // {com}#jadn_opts:{opts}\n'.format(
                    idn=self.indent,
                    choice='required',
                    type=self._fieldType(l[2]),
                    name=self.formatStr(l[1]),
                    num=l[0],
                    com='' if l[-1] == '' else l[-1] + ' ',
                    opts=json.dumps(opts)
                ))

        opts = {'type': itm[1]}
        if len(itm[2]) > 0: opts['options'] = topts_s2d(itm[2])

        return '\nstruct {name} {{ // {com}#jadn_opts:{opts}\n{req}}}\n'.format(
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
        # Thrift does not use choice, using struct
        lines = []
        for l in itm[-1]:
            opts = {'type': l[2]}
            if len(l[-2]) > 0: opts['options'] = fopts_s2d(l[-2])

            lines.append('{idn}{num}: {choice} {type} {name}; // {com}#jadn_opts:{opts}\n'.format(
                idn=self.indent,
                choice='optional',
                type=self._fieldType(l[2]),
                name=self.formatStr(l[1]),
                num=l[0],
                com='' if l[-1] == '' else l[-1]+' ',
                opts=json.dumps(opts)
            ))

        opts = {'type': itm[1]}
        if len(itm[2]) > 0: opts['options'] = topts_s2d(itm[2])

        return '\nstruct {name} {{ // {com}#jadn_opts:{opts}\n{req}}}\n'.format(
            name=self.formatStr(itm[0]),
            req=''.join(lines),
            com='' if itm[-2] == '' else itm[-2] + ' ',
            opts=json.dumps(opts)
        )

    def _formatMap(self, itm):
        """
        Formats map for the given schema type
        :param itm: map to format
        :return: formatted map
        :rtype str
        """
        # Thrift does not use maps in same way, using struct

        return self._formatChoice(itm)

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
            a = l[-1].split('-', 1)[0]
            if l[0] == 0: default = False
            lines.append('{idn}{name} = {num};{com}\n'.format(
                idn=self.indent,
                name=self.formatStr(l[1] or '{}'.format(a[0:-1])),
                num=l[0],
                com='' if l[-1] == '' else ' // {}'.format(l[-1])
            ))

        opts = {'type': itm[1]}
        if len(itm[2]) > 0: opts['options'] = topts_s2d(itm[2])

        return '\nenum {name} {{ // {com}#jadn_opts:{opts}\n{enum}}}\n'.format(
            idn=self.indent,
            name=self.formatStr(itm[0]),
            com='' if itm[-2] == '' else itm[-2] + ' ',
            opts=json.dumps(opts),
            enum=''.join(lines)
        )

    def _formatArray(self, itm):
        """
        Formats array for the given schema type
        :param itm: array to format
        :return: formatted array
        :rtype str
        """
        # Best method for creating some type of array

        return self._formatArrayOf(itm)

    def _formatArrayOf(self, itm):
        """
        Formats arrayof for the given schema type
        :param itm: arrayof to format
        :return: formatted arrayof
        :rtype str
        """
        # Best method for creating some type of array

        field_opts = topts_s2d(itm[2])
        opts = {
            'type': itm[1],
            'options': topts_s2d(itm[2])
        }

        return '\nstruct {name} {{\n{req}}}\n'.format(
            name=self.formatStr(itm[0]),
            req='{idn}{num}: {choice} list<{type}> {name};  // {com} #jadn_opts:{opts}\n'.format(
                idn=self.indent,
                num='1',
                choice='optional',
                type=self.formatStr(field_opts['rtype']),
                name='item',
                com=itm[3],
                opts=json.dumps(opts)
            ),
        )


def thrift_dumps(jadn):
    """
    Produce Thrift schema from JADN schema
    :arg jadn: JADN Schema to convert
    :type jadn: str or dict
    :return: Thrift schema
    :rtype str
    """
    return JADNtoThrift(jadn).thrift_dump()


def thrift_dump(jadn, fname, source=""):
    with open(fname, "w") as f:
        if source:
            f.write("-- Generated from " + source + ", " + datetime.ctime(datetime.now()) + "\n\n")
        f.write(thrift_dumps(jadn))