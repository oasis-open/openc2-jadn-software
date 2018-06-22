from __future__ import unicode_literals, print_function

import json
import re

from arpeggio import EOF, Optional, OneOrMore, ParserPython, PTNodeVisitor, visit_parse_tree, RegExMatch, OrderedChoice, UnorderedGroup, ZeroOrMore
from datetime import datetime

from ..utils import toStr, Utils
lineSep = '\\r?\\n'


def ProtoRules():
    def endLine():
        # match - Line terminator (windows and unix style)
        return RegExMatch(r'({})?'.format(lineSep))

    def number():
        # match - numbers with and without decimals
        return RegExMatch(r'\d*\.\d*|\d+')

    def string():
        # match - any characters enclosed with single/double quotes
        return RegExMatch(r'[\'\"].*?[\'\"]')

    def commentBlock():
        # match - any characters (line terminators included) enclosed with block quote signifier (/* and */)
        return RegExMatch(r'\/\*(.|{})*?\*\/'.format(lineSep)),

    def commentLine():
        # match - any character, non line terminator
        return '//', RegExMatch(r'.*')

    def syntax():
        # match - syntax = ['"]SYNTAX['"](;)
        return RegExMatch(r'syntax\s?=\s?[\'\"].*[\'\"]\;?'), OneOrMore(endLine)

    def package():
        # match - package ('")PACKAGE('")(;)
        return RegExMatch(r'package\s?[\'\"]?.*[\'\"]?\;?'), OneOrMore(endLine)

    def pkgImports():
        # match - import ['"]PACKAGE['"](;)
        return RegExMatch(r'import\s?[\'\"].*[\'\"]\;?'), OneOrMore(endLine)

    def headerComments():
        return (
            OrderedChoice(
                ZeroOrMore(commentBlock),
                ZeroOrMore(commentLine)
            )
        )

    def header():
        return UnorderedGroup(
            syntax,
            package,
            headerComments,
            ZeroOrMore(pkgImports)
        )

    def defHeader():
        return (
            # match - word or digit character one or more times
            RegExMatch(r'[\w\d]+'),  # name
            "{",
            Optional(
                '//',
                # match - any character (except line terminator) until # or line terminator
                RegExMatch(r'.*?(#|{})'.format(lineSep))  # comment
            ),
            # match - (#)jadn_opts:{JADN OPTS}
            # last } is matched one or more times
            Optional(RegExMatch(r'#?jadn_opts:{.*}+')),  # jadn options
            OneOrMore(endLine)
        )

    def defField():
        return (
            # match - any word character followed by one or more word or digit characters until a space
            RegExMatch(r'\w[\w\d\.]*?\s'),  # type
            # match - any word character followed by one or more word or digit characters until a space
            RegExMatch(r'\w[\w\d]*?\s'),  # name
            '=',
            number,  # field number
            ';',
            Optional(
                '//',
                # match - any character (except line terminator) until # or line terminator
                RegExMatch(r'.*?(#|{})'.format(lineSep)),  # comment
                # match - (#)jadn_opts:{JADN OPTS}
                # last } is matched one or more times
                Optional(RegExMatch(r'jadn_opts:{.*}+'))  # jadn options
            ),
            OneOrMore(endLine)
        )

    def messageDef():
        return (
            'message',
            defHeader,
            OneOrMore(defField),
            '}'
        )

    def enumField():
        return (
            # match - any word character followed by one or more word or digit characters until a space
            RegExMatch(r'\w[\w\d]*?\s'),  # name
            '=',
            number,  # field number
            ';',
            Optional(
                '//',
                # match - any character (except line terminator) until # or line terminator
                RegExMatch(r'.*?(#|{})'.format(lineSep)),  # comment
                # match - (#)jadn_opts:{JADN OPTS}
                # last } is matched one or more times
                Optional(RegExMatch(r'jadn_opts:{.*}+'))  # jadn options
            ),
            OneOrMore(endLine)
        )

    def enumDef():
        return (
            'enum',
            defHeader,
            OneOrMore(enumField),
            '}',
        )

    def repeatedDef():
        return (
            'repeated',
            defField
        )

    def oneofDef():
        return (
            'oneof',
            defHeader,
            OneOrMore(defField),
            '}'
        )

    def wrappedDef():
        return (
            'message',
            # match - any word or digit character one or more word or digit characters until a non word/digit character
            RegExMatch(r'[\w\d]+'),
            '{',
            OrderedChoice(
                Optional(oneofDef),
                Optional(repeatedDef)
            ),
            '}'
        )

    def typeDefs():
        return OneOrMore(
            UnorderedGroup(
                ZeroOrMore(messageDef),
                ZeroOrMore(wrappedDef),
                ZeroOrMore(enumDef),
            )
        )

    def customDef():
        return OrderedChoice(
            ZeroOrMore(commentBlock),
            ZeroOrMore(commentLine)
        )

    return (
        header,
        typeDefs,
        Optional(customDef),
        EOF
    )


class ProtoVisitor(PTNodeVisitor):
    data = {}
    repeatedTypes = {
        'arrayOf': 'ArrayOf',
        'array': 'Array'
    }

    def load_jadnOpts(self, jadnString, defaultDict):
        jadnString = toStr(jadnString)
        defType = defaultDict['type'] if 'type' in defaultDict else 'String'
        optDict = {
            'type': 'String',
            'options': []
        }
        optDict.update(defaultDict)

        if re.match(r'^jadn_opts:', jadnString):
            optStr = re.sub(r'jadn_opts:(?P<opts>{.*?}+)', '\g<opts>', jadnString)

            try:
                optDict = json.loads(optStr)
                optDict['type'] = optDict['type'] if 'type' in optDict else defType
                optDict['options'] = Utils.opts_d2s(optDict['options']) if 'options' in optDict else []
            except Exception as e:
                print('Oops, cant load jadn')
                print(e)

        return optDict

    def visit_ProtoRules(self, node, children):
        return self.data

    def visit_number(self, node, children):
        try:
            return float(node.value) if '.' in node.value else int(node.value)
        except Exception as e:
            print(e)

        return node.value

    def visit_string(self, node, children):
        return node.value.strip('\'\"')

    def visit_commentBlock(self, node, children):
        com = re.compile(r'(^(/\*)?(\s+)?|(\s+)?(\*/)?$)', re.MULTILINE).sub('', node.value)
        com = re.split(r'{}'.format(lineSep), com)
        com = com[1:] if com[0] == '' else com
        com = com[:-1] if com[-1] == '' else com
        return com

    def visit_commentLine(self, node, children):
        return re.sub(r'^//\s*?', '', node.value)

    def visit_headerComments(self, node, children):
        if 'meta' not in self.data:
            self.data['meta'] = {}

        for child in children:
            if type(child) is list:
                for c in child:
                    if re.match(r'^\s?\*\s?meta:', c):
                        line = re.sub(r'(\s?\*\s?meta:\s+|{})'.format(lineSep), '', c).split(' - ')

                        try:
                            self.data['meta'][line[0]] = json.loads(' - '.join(line[1:]))
                        except Exception as e:
                            self.data['meta'][line[0]] = ' - '.join(line[1:])

    def visit_typeDefs(self, node, children):
        if 'types' not in self.data:
            self.data['types'] = []

        for child in children:
            if type(child) is list:
                self.data['types'].append(child)
            else:
                print('type child is not type list')
                print(child)

    def visit_defHeader(self, node, children):
        optDict = self.load_jadnOpts(children[-1], {
            'type': 'Record',
            'options': []
        })

        return [
            children[0],  # Type Name
            optDict['type'],  # Type
            optDict['options'],  # Options
            re.sub(r'\s?#\S?$', '', children[1]) if len(children) >= 2 else ''  # comment
        ]

    def visit_defField(self, node, children):
        optDict = self.load_jadnOpts(children[-1], {
            'type': 'String',
            'options': []
        })

        return [
            children[2],  # field number
            re.sub(r'(^\s+|\s+$)', '', children[1]),  # name
            self.repeatedTypes.get(optDict['type'], optDict['type']),  # type
            optDict['options'],  # options
            re.sub(r'\s?#\S?$', '', children[3]) if len(children) >= 4 else ''  # comment
        ]

    def visit_messageDef(self, node, children):
        msgFields = []

        for child in children[1:]:
            if type(child) is list:
                msgFields.append(child)
            else:
                print('Message child not type list')
                print(child)

        children[0].append(msgFields)
        return children[0]

    def visit_enumField(self, node, children):
        if len(children) >= 3 and re.match(r'^required starting enum number for protobuf3', children[-1]):
            return

        return [
            children[1],  # field number
            re.sub(r'(^\s+|\s+$)', '', children[0]),  # name
            re.sub(r'\s?(#|{})\S?$'.format(lineSep), '', children[2]) if len(children) >= 3 else ''  # comment
        ]

    def visit_enumDef(self, node, children):
        enumFields = []
        name = children[0][0]

        for child in children[1:]:
            if type(child) is list and not (child[0] == 0 and re.match(r'^Unknown_{}'.format(name), child[1])):
                enumFields.append(child)
            elif child[0] == 0 and re.match(r'^Unknown_{}'.format(name), child[1]):
                print('Enumerated field is placeholder')
                print(child)
            else:
                print('Enumerated field not type list')
                print(child)

        children[0].append(enumFields)
        return children[0]

    def visit_repeatedDef(self, node, children):
        if len(children) > 1:
            print('RepeatedDef Error')
            return
        else:
            children = children[0]

        return children[2:]

    def visit_oneofDef(self, node, children):
        oneofFields = []

        for child in children[1:]:
            if type(child) is list:
                oneofFields.append(child)
            else:
                print('OneOf child not type list')
                print(child)

        children[0].append(oneofFields)
        return children[0]

    def visit_wrappedDef(self, node, children):
        if children[0] == children[1][0]:
            return children[1]

        elif children[1][0] in self.repeatedTypes.values():
            repeated = [children[0]]
            repeated.extend(children[1])
            return repeated

        else:
            print('Invalid Wrapped Def')
            print(children[1])

    def visit_customDef(self, node, children):
        if 'types' not in self.data:
            self.data['types'] = []

        for child in children:
            if type(child) is list and 'JADN Custom Fields' in child[0]:
                try:
                    self.data['types'].extend(json.loads(''.join(child[1:])))
                except Exception as e:
                    print(e)
            else:
                print('Custom Something..')
                print(child)


def proto2jadn_dumps(proto):
    """
    Produce jadn schema from proto3 schema
    :arg proto: Proto3 Schema to convert
    :type proto: str
    :return: jadn schema
    :rtype str
    :exception Exception - parsing error
    """
    try:
        parser = ParserPython(ProtoRules)
        parse_tree = parser.parse(toStr(proto))
        result = visit_parse_tree(parse_tree, ProtoVisitor())
        return Utils.jadnFormat(result, indent=2)

    except Exception as e:
        raise Exception('Proto parsing error has occurred: {}'.format(e))


def proto2jadn_dump(proto, fname, source=""):
    with open(fname, "w") as f:
        if source:
            f.write("-- Generated from " + source + ", " + datetime.ctime(datetime.now()) + "\n\n")
        f.write(proto2jadn_dumps(proto))
