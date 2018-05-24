import datetime
import json
import re


class JADNtoRelaxNG(object):
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

        self.indent = '  '

        self._fieldMap = {
            'Binary': 'base64Binary',
            'Boolean': 'boolean',
            'Integer': 'integer',
            'Number': 'float',
            'Null': '',
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

        self._meta = jadn['meta'] or []
        self._types = []
        self._custom = []
        self._records = []
        self._customFields = []

        for t in jadn['types']:
            if t[1] in self._structFormats.keys():
                self._types.append(t)
                self._customFields.append(t[0])
                if t[1] == 'Record':
                    self._records.append(t[0])
            else:
                self._custom.append(t)

    def relax_dump(self):
        records = ['{idn}{idn}{idn}<element name="message">{rec}</element>'.format(
            idn=self.indent,
            rec=self._fieldType(r)
        ) for r in self._records]

        return '{header}<grammar datatypeLibrary="http://www.w3.org/2001/XMLSchema-datatypes" ' \
               'ns="http://relaxng.org/ns/structure/1.0" xmlns="http://relaxng.org/ns/structure/1.0">\n' \
               '{idn}<start>\n{root}\n{idn}</start>\n{defs}\n</grammar>\n'.format(
                    idn=self.indent,
                    header=self.makeHeader(),
                    root='{idn}{idn}<choice>\n{recs}\n{idn}{idn}</choice>'.format(
                        idn=self.indent,
                        recs='\n'.join(records)
                    ),
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
        header = ['<!-- {} - {} -->'.format(k, v) for k, v in self._meta.items()]

        return '\n'.join(header) + '\n\n'

    def makeStructures(self):
        """
        Create the type definitions for the schema
        :return: type definitions for the schema
        :rtype str
        """
        defs = []
        for t in self._types:
            df = self._structFormats.get(t[1], None)

            if df is not None:
                defs.append('\n' + '\n'.join([re.sub(r'^', self.indent, l) for l in df(t).split('\n')]))

        return '\n'.join(defs)

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
            rtn = '<ref name=\"{}\"/>'.format(self.formatStr(f))

        elif f in self._fieldMap.keys():
            rtn = self.formatStr(self._fieldMap.get(f, f))
            rtn = '<text/>' if rtn == '' else '<data type="{}"/>'.format(rtn)

        else:
            rtn = '<text/>'

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
        lines = {
            'req': [],
            'opt': []
        }
        for l in itm[-1]:
            opts = {'type': l[2], 'field': l[0]}
            if len(l[-2]) > 0: opts['options'] = l[-2]

            ltmp = '{idn}<element name=\"{name}\">{fType}</element> <!-- {com}#jadn_opts:{opts} -->\n'.format(
                idn=self.indent + self.indent if '[0' in l[-2] else self.indent,
                name=self.formatStr(l[1]),
                fType=self._fieldType(l[2]),
                com='' if l[-1] == '' else l[-1] + ' ',
                opts=json.dumps(opts)
            )
            lines['opt' if '[0' in l[-2] else 'req'].append(ltmp)

        opts = {'type': itm[1]}
        if len(itm[2]) > 0: opts['options'] = itm[2]

        return '<define name="{name}"> <!-- {com}#jadn_opts:{opts} -->\n{req}{opt}\n</define>'.format(
            name=self.formatStr(itm[0]),
            req=''.join(lines['req']),
            opt='' if len(lines['opt']) == 0 else '{idn}<optional>\n{opts}{idn}</optional>'.format(idn=self.indent, opts=''.join(lines['opt'])),
            com='' if itm[-2] == '' else itm[-2] + ' ',
            opts=json.dumps(opts),
            idn=self.indent
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
            n = self.formatStr(l[1] or 'Unknown_{}_{}'.format(self.formatStr(itm[0]), l[0]))
            opts = {'field': l[0]}

            lines.append('{idn}{idn}{idn}<element name=\"{name}\">{val}</element> <!-- {com}#jadn_opts:{opts} -->\n'.format(
                idn=self.indent,
                name=n,
                val=self._fieldType(l[2]),
                com='' if l[-1] == '' else l[-1] + ' ',
                opts=json.dumps(opts)
            ))

        opts = {'type': itm[1]}
        if len(itm[2]) > 0: opts['options'] = itm[2]

        return '<define name="{name}"> <!-- {com}#jadn_opts:{opts} -->\n{idn}{idn}<choice>\n{req}{idn}{idn}</choice>\n</define>'.format(
            idn=self.indent,
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
        lines = {
            'req': [],
            'opt': []
        }

        for l in itm[-1]:
            opts = {'type': l[2], 'field': l[0]}
            if len(l[-2]) > 0: opts['options'] = l[-2]

            ltmp = '{idn}<element name=\"{name}\">{fType}</element> <!-- {com}#jadn_opts:{opts}-->\n'.format(
                idn=self.indent+self.indent if '[0' in l[-2] else self.indent,
                name=self.formatStr(l[1]),
                fType=self._fieldType(l[2]),
                com='' if l[-1] == '' else l[-1] + ' ',
                opts=json.dumps(opts)
            )

            lines['opt' if '[0' in l[-2] else 'req'].append(ltmp)

        opts = {'type': itm[1]}
        if len(itm[2]) > 0: opts['options'] = itm[2]

        return '<define name="{name}"> <!-- {com}#jadn_opts:{opts} -->\n{req}{opt}\n</define>'.format(
            idn=self.indent,
            name=self.formatStr(itm[0]),
            req=''.join(lines['req']),
            opt='' if len(lines['opt']) == 0 else '{idn}<optional>\n{opts}{idn}</optional>'.format(idn=self.indent, opts=''.join(lines['opt'])),
            com='' if itm[-2] == '' else itm[-2] + ' ',
            opts=json.dumps(opts)
        )

    def _formatEnumerated(self, itm):
        """
        Formats enum for the given schema type
        :param itm: enum to format
        :return: formatted enum
        :rtype str
        """
        lines = []
        for l in itm[-1]:
            n = self.formatStr(l[1] or 'Unknown_{}_{}'.format(self.formatStr(itm[0]), l[0]))
            opts = {'field': l[0]}
            lines.append('{idn}{idn}{idn}<value>{val}</value> <!-- {com}#jadn_opts:{opts} -->\n'.format(
                idn=self.indent,
                val=n,
                com='' if l[-1] == '' else l[-1] + ' ',
                opts=json.dumps(opts)
            ))

        opts = {'type': itm[1]}
        if len(itm[2]) > 0: opts['options'] = itm[2]

        return '<define name="{name}"> <!-- {com}#jadn_opts:{opts} -->\n{idn}{idn}<choice>\n{req}{idn}{idn}</choice>\n</define>'.format(
            idn=self.indent,
            name=self.formatStr(itm[0]),
            req=''.join(lines),
            com='' if itm[-2] == '' else itm[-2] + ' ',
            opts=json.dumps(opts)
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
        of_type = filter(lambda x: x.startswith('#'), itm[2])
        of_type = of_type[0][1:] if len(of_type) == 1 else 'UNKNOWN'
        '''
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
        '''

        opts = {'type': itm[1]}
        if len(itm[2]) > 0: opts['options'] = itm[2]

        return '<define name="{name}"> <!-- {com}#jadn_opts:{opts} -->\n{idn}<zeroOrMore>\n{idn}{idn}{type}\n{idn}</zeroOrMore>\n</define>'.format(
            idn=self.indent,
            name=self.formatStr(itm[0]),
            type=self._fieldType(of_type),
            com=itm[-1],
            opts=json.dumps(opts)
        )


def relax_dumps(jadn):
    """
    Produce CDDL schema from JADN schema
    :arg jadn: JADN Schema to convert
    :type jadn: str or dict
    :return: Protobuf3 schema
    :rtype str
    """
    return JADNtoRelaxNG(jadn).relax_dump()


def relax_dump(jadn, fname, source=""):
    with open(fname, "w") as f:
        if source:
            f.write("-- Generated from " + source + ", " + datetime.ctime(datetime.now()) + "\n\n")
        f.write(relax_dumps(jadn))
