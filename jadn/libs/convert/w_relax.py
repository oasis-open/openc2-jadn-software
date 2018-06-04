import json
import re
import sys
import xml.dom.minidom as md

from datetime import datetime

from ..codec.codec_utils import fopts_s2d, topts_s2d
from ..utils import toStr, Utils

primitives = [str, int, float]

if sys.version_info.major < 3:
    primitives.append(unicode)


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
            self._customFields.append(t[0])
            if t[1] in self._structFormats.keys():
                self._types.append(t)

                if t[1] == 'Record':
                    self._records.append(t[0])
            else:
                self._custom.append(t)

    def relax_dump(self):
        records = [self._formatTag('element', self._fieldType(r), name='message') for r in self._records]

        root_cont = [
            self._formatTag(
                'start',
                self._formatTag('choice', records)
            )
        ]

        root_cont.extend(self.makeStructures())

        root_cont.append(self._formatComment('Custom Defined Types'))

        root_cont.extend(self.makeCustom())

        root = self._formatTag(
            'grammar',
            root_cont,
            datatypeLibrary="http://www.w3.org/2001/XMLSchema-datatypes",
            xmlns="http://relaxng.org/ns/structure/1.0"
        )

        return '{header}{root}\n'.format(
            header=self.makeHeader(),
            root=self._formatPretty(root)
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
        header = ['<!-- meta: {} - {} -->'.format(k, re.sub(r'(^\"|\"$)', '', json.dumps(Utils.defaultDecode(v)))) for k, v in self._meta.items()]

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
                defs.append(df(t))

        return defs

    def makeCustom(self):
        defs = []

        for field in self._custom:
            com = '' if field[-1] == '' else field[-1]

            if len(field[-2]) >= 1:
                opts = {'options': field[-2]}
                com += ' #jadn_opts:{}'.format(json.dumps(opts))

            c = self._formatTag(
                'define',
                self._fieldType(field[1]),
                name=self.formatStr(field[0]),
                com=com
            )
            defs.append(c)

        return defs

    def _formatPretty(self, xml, indent=1):
        idn = '  ' * indent
        rtn_xml = '\n'.join([line for line in md.parseString(xml).toprettyxml(indent=idn).split('\n') if line.strip()])
        rtn_xml = re.sub(r'^<\?xml.*?\?>\n', '', rtn_xml)
        return rtn_xml

    def _formatTag(self, tag, contents='', com='', **kargs):
        ign = ['', None]

        if contents in ign and com in ign:
            elm = '<{tag}{attrs}/>'.format(
                tag=tag,
                attrs=''.join([' {k}={v}'.format(k=k, v=json.dumps(v)) for k, v in kargs.items()])
            )
        else:
            elm = '<{tag}{attrs}>'.format(
                tag=tag,
                attrs=''.join([' {k}={v}'.format(k=k, v=json.dumps(v)) for k, v in kargs.items()])
            )
            if com != '' and re.match(r'^<!--.*?-->', com):
                elm += com
            elif com != '':
                elm += self._formatComment(com)

            if type(contents) in primitives:
                elm += toStr(contents)

            elif type(contents) is list:
                for itm in contents:
                    if type(itm) is str:
                        elm += itm

            elif type(contents) is dict:
                # print('dict')
                for k, v in contents.items():
                    elm.append(self._formatTag(k, v))
            else:
                print('unprepared type: {}'.format(type(contents)))

            elm += '</{tag}>'.format(tag=tag)

        return elm

    def _formatComment(self, msg, **kargs):

        elm = '<!--'
        if msg not in ['', None, ' ']:
            elm += ' {msg}'.format(msg=msg)

        for k, v in kargs.items():
            elm += ' #{k}:{v}'.format(
                k=k,
                v=json.dumps(v)
            )

        elm += ' -->'

        return elm

    def _fieldType(self, f):
        """
        Determines the field type for the schema
        :param f: current type
        :return: type mapped to the schema
        :rtype str
        """
        if f in self._customFields:
            rtn = self._formatTag('ref', name=self.formatStr(f))

        elif f in self._fieldMap.keys():
            rtn = self.formatStr(self._fieldMap.get(f, f))
            rtn = self._formatTag('text') if rtn == '' else self._formatTag('data', type=rtn)

        else:
            rtn = self._formatTag('text')

        return rtn

    # Structure Formats
    def _formatRecord(self, itm):
        """
        Formats records for the given schema type
        :param itm: record to format
        :return: formatted record
        :rtype str
        """
        defs = []
        for l in itm[-1]:
            opts = {'type': l[2], 'field': l[0]}
            if len(l[-2]) > 0: opts['options'] = fopts_s2d(l[-2])

            ltmp = self._formatTag(
                'element',
                self._fieldType(l[2]),
                name=self.formatStr(l[1]),
                com=self._formatComment('' if l[-1] == '' else l[-1], jadn_opts=opts)
            )

            if '[0' in l[-2]:
                # optional
                defs.append(self._formatTag('optional', ltmp))
            else:
                defs.append(ltmp)

        opts = {'type': itm[1]}
        if len(itm[2]) > 0: opts['options'] = topts_s2d(l[-2])

        return self._formatTag(
            'define',
            self._formatTag('interleave', defs),
            com=self._formatComment('' if itm[-2] == '' else itm[-2], jadn_opts=opts),
            name=self.formatStr(itm[0])
        )

    def _formatChoice(self, itm):
        """
        Formats choice for the given schema type
        :param itm: choice to format
        :return: formatted choice
        :rtype str
        """
        defs = []
        for l in itm[-1]:
            n = self.formatStr(l[1] or 'Unknown_{}_{}'.format(self.formatStr(itm[0]), l[0]))
            opts = {'field': l[0], 'type': l[2]}

            defs.append(self._formatTag(
                'element',
                self._fieldType(l[2]),
                com=self._formatComment('' if l[-1] == '' else l[-1], jadn_opts=opts),
                name=n
            ))

        opts = {'type': itm[1]}
        if len(itm[2]) > 0: opts['options'] = topts_s2d(itm[2])

        return self._formatTag(
            'define',
            self._formatTag('choice', defs),
            com=self._formatComment('' if itm[-2] == '' else itm[-2], jadn_opts=opts),
            name=self.formatStr(itm[0])
        )

    def _formatMap(self, itm):
        """
        Formats map for the given schema type
        :param itm: map to format
        :return: formatted map
        :rtype str
        """
        defs = []

        for l in itm[-1]:
            opts = {'type': l[2], 'field': l[0]}
            if len(l[-2]) > 0: opts['options'] = fopts_s2d(l[-2])

            ltmp = self._formatTag(
                'element',
                self._fieldType(l[2]),
                name=self.formatStr(l[1]),
                com=self._formatComment('' if l[-1] == '' else l[-1], jadn_opts=opts)
            )

            if '[0' in l[-2]:
                # optional
                defs.append(self._formatTag('optional', ltmp))
            else:
                defs.append(ltmp)

        opts = {'type': itm[1]}
        if len(itm[2]) > 0: opts['options'] = topts_s2d(itm[2])

        return self._formatTag(
            'define',
            self._formatTag('interleave', defs),
            com=self._formatComment('' if itm[-2] == '' else itm[-2], jadn_opts=opts),
            name=self.formatStr(itm[0])
        )

    def _formatEnumerated(self, itm):
        """
        Formats enum for the given schema type
        :param itm: enum to format
        :return: formatted enum
        :rtype str
        """
        defs = []
        for l in itm[-1]:
            opts = {'field': l[0]}
            defs.append(self._formatTag(
                'value',
                self.formatStr(l[1] or 'Unknown_{}_{}'.format(self.formatStr(itm[0]), l[0])),
                com=self._formatComment('' if l[-1] == '' else l[-1], jadn_opts=opts)
            ))

        opts = {'type': itm[1]}
        if len(itm[2]) > 0: opts['options'] = topts_s2d(itm[2])

        return self._formatTag(
            'define',
            self._formatTag('choice', defs),
            com=self._formatComment('' if itm[-2] == '' else itm[-2], jadn_opts=opts),
            name=self.formatStr(itm[0])
        )

    def _formatArray(self, itm):  # TODO: what should this do??
        """
        Formats array for the given schema type
        :param itm: array to format
        :return: formatted array
        :rtype str
        """
        field_opts = topts_s2d(itm[2])

        opts = {'type': itm[1]}
        if len(itm[2]) > 0: opts['options'] = topts_s2d(itm[2])

        return self._formatTag(
            'define',
            self._formatTag(
                'list',
                self._fieldType(field_opts['aetype'])
            ),
            com=self._formatComment(itm[-1], jadn_opts=opts),
            name=self.formatStr(itm[0])
        )

    def _formatArrayOf(self, itm):  # TODO: what should this do??
        """
        Formats arrayof for the given schema type
        :param itm: arrayof to format
        :return: formatted arrayof
        :rtype str
        """
        field_opts = topts_s2d(itm[2])

        opts = {'type': itm[1]}
        if len(itm[2]) > 0: opts['options'] = topts_s2d(itm[2])

        return self._formatTag(
            'define',
            self._formatTag(
                'list',
                self._fieldType(field_opts['aetype'])
            ),
            com=self._formatComment(itm[-1], jadn_opts=opts),
            name=self.formatStr(itm[0])
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
