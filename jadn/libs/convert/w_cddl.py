import datetime
import json
import re


class JADNtoCDDL(object):
    def __init__(self, jadn):
        """
        Schema Converter for JADN to CDDL
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

        self._meta = jadn['meta'] or []
        self._types = [t for t in jadn['types'] if len(t) == 5 or t[1].lower() in ['arrayof', 'array']]
        self._custom = [t for t in jadn['types'] if len(t) == 4 and t[1].lower() not in ['arrayof', 'array']]

        self.indent = '    '

        self._customFields = [t[0] for t in self._custom] + [t[0] for t in self._types]

        self._fieldMap = {
            'Binary': 'bstr',
            'Boolean': 'bool',
            'Integer': 'int64',
            'Number': 'float64',
            'Null': 'null',
            'String': 'bstr'
        }
        self._structFormats = {
            'Record': self._formatRecord,
            'Choice': self._formatChoice,
            'Map': self._formatMap,
            'Enumerated': self._formatEnumerated,
            'Array': self._formatArray,
            'ArrayOf': self._formatArrayOf,
        }

    def cddl_dump(self):
        return '{header}{defs}\n{custom}'.format(
            header=self.makeHeader(),
            defs=self.makeStructures(),
            custom=self.makeCustom()
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
        header = ['; {} - {}'.format(k, v) for k, v in self._meta.items()]

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

    def makeCustom(self):
        defs = []
        for field in self._custom:
            line = '{name} = {type} ; {com}'.format(
                name=self.formatStr(field[0]),
                type=self._fieldType(field[1]),
                com=field[-1]
            )
            defs.append(line)

        return '\n'.join(defs)

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
            rtn = 'bstr'

        # print(f, rtn)
        return rtn

    # Structure Formats
    def _formatRecord(self, itm):
        """
        Formats records for the given schema type
        :param itm: record to format
        :return: formatted record
        :rtype str
        """
        tmp = "\n{} = {{".format(self.formatStr(itm[0]))
        opts = {'type': itm[1]}
        if len(itm[2]) > 0: opts['options'] = itm[2]
        tmp += ' ; {}#jadn_opts:{}\n'.format('' if itm[-2] == '' else itm[-2]+' ', json.dumps(opts))

        i = 1
        for l in itm[-1]:
            tmp += '{idn}{pre_opts}{name}: {fType}{com}'.format(
                idn=self.indent,
                pre_opts='? ' if '[0' in l[-2] else '',
                name=self.formatStr(l[1]),
                fType=self._fieldType(l[2]),
                com=',' if i < len(itm[-1]) else ''
            )
            opts = {'type': l[2], 'field': l[0]}
            if len(l[-2]) > 0: opts['options'] = l[-2]
            tmp += ' ; {}#jadn_opts:{}\n'.format('' if l[-1] == '' else l[-1]+' ', json.dumps(opts))
            i += 1
        tmp += "}\n"

        return tmp

    def _formatChoice(self, itm):
        """
        Formats choice for the given schema type
        :param itm: choice to format
        :return: formatted choice
        :rtype str
        """
        opts = {'type': itm[1]}
        if len(itm[2]) > 0: opts['options'] = itm[2]
        tmp = "{} = ( ; {}#jadn_opts:{}\n".format(self.formatStr(itm[0]), '' if itm[-2] == '' else itm[-2]+' ', json.dumps(opts))

        lines = []
        i = 1
        for l in itm[-1]:
            ltmp = '{}: {}{}'.format(self.formatStr(l[1]), self._fieldType(l[2]), ' //' if i < len(itm[-1]) else '')
            opts = {'type': l[2], 'field': l[0]}
            if len(l[-2]) > 0: opts['options'] = l[-2]
            ltmp += ' ; {}#jadn_opts:{}'.format('' if l[-1] == '' else l[-1]+' ', json.dumps(opts))
            lines.append(ltmp)
            i += 1

        return '\n{head}{idn}{defs}\n)\n'.format(
            head=tmp,
            idn=self.indent,
            defs='\n{}'.format(self.indent).join(lines)
        )

    def _formatMap(self, itm):
        """
        Formats map for the given schema type
        :param itm: map to format
        :return: formatted map
        :rtype str
        """
        tmp = "\n{} = [".format(self.formatStr(itm[0]))
        opts = {'type': itm[1]}
        if len(itm[2]) > 0: opts['options'] = itm[2]
        tmp += ' ; {}#jadn_opts:{}\n'.format('' if itm[-2] == '' else itm[-2] + ' ', json.dumps(opts))

        i = 1
        for l in itm[-1]:
            tmp += '{idn}{pre_opts}{name}: {fType}{com}'.format(
                idn=self.indent,
                pre_opts='? ' if '[0' in l[-2] else '',
                name=self.formatStr(l[1]),
                fType=self._fieldType(l[2]),
                com=',' if i < len(itm[-1]) else ''
            )
            opts = {'type': l[2], 'field': l[0]}
            if len(l[-2]) > 0: opts['options'] = l[-2]
            tmp += ' ; {}#jadn_opts:{}\n'.format('' if l[-1] == '' else l[-1] + ' ', json.dumps(opts))
            i += 1
        tmp += "]\n"
        return tmp

    def _formatEnumerated(self, itm):
        """
        Formats enum for the given schema type
        :param itm: enum to format
        :return: formatted enum
        :rtype str
        """
        opts = {'type': itm[1]}
        if len(itm[2]) > 0: opts['options'] = itm[2]
        tmp = '\n; {}#jadn_opts:{}\n'.format('' if itm[-2] == '' else itm[-2] + ' ', json.dumps(opts))
        tmp += '{} = '.format(self.formatStr(itm[0]))

        lines = []
        for l in itm[-1]:
            n = self.formatStr(l[1] or 'Unknown_{}_{}'.format(self.formatStr(itm[0]), l[0]))
            ltmp = '\"{}\"'.format(n)
            opts = {'field': l[0]}
            ltmp += ' ; {}#jadn_opts:{}\n'.format('' if l[-1] == '' else l[-1] + ' ', json.dumps(opts))
            lines.append(ltmp)
        tmp += '{} /= '.format(self.formatStr(itm[0])).join(lines)

        return tmp

    def _formatArray(self, itm):  # TODO: what should this do??
        """
        Formats array for the given schema type
        :param itm: array to format
        :return: formatted array
        :rtype str
        """
        return ''

    def _formatArrayOf(self, itm):  # TODO: what should this do??
        """
        Formats arrayof for the given schema type
        :param itm: arrayof to format
        :return: formatted arrayof
        :rtype str
        """
        of_type = filter(lambda x: x.startswith('#'), itm[2])
        of_type = of_type[0][1:] if len(of_type) == 1 else 'UNKNOWN'

        min_n = filter(lambda x: x.startswith('['), itm[2])
        min_n = min_n[0][1:] if len(min_n) == 1 else ''
        min_n = int(min_n) if min_n.isdigit() else ''

        max_n = filter(lambda x: x.startswith(']'), itm[2])
        max_n = max_n[0][1:] if len(max_n) == 1 else ''
        max_n = int(max_n) if max_n.isdigit() else ''

        field_type = '[{min}*{max} {type}]'.format(
            min='' if min_n == 0 else min_n,
            max='' if max_n == 0 else max_n,
            type=self._fieldType(of_type)
        )

        line = '\n{name} = {type} ; {com}\n'.format(
            name=self.formatStr(itm[0]),
            type=field_type,
            com=itm[-1]
        )

        return line


def cddl_dumps(jadn):
    """
    Produce CDDL schema from JADN schema
    :arg jadn: JADN Schema to convert
    :type jadn: str or dict
    :return: Protobuf3 schema
    :rtype str
    """
    return JADNtoCDDL(jadn).cddl_dump()


def cddl_dump(jadn, fname, source=""):
    with open(fname, "w") as f:
        if source:
            f.write("-- Generated from " + source + ", " + datetime.ctime(datetime.now()) + "\n\n")
        f.write(cddl_dumps(jadn))
