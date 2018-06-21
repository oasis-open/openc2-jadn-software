from __future__ import unicode_literals, print_function

import json
import re

from arpeggio import EOF, Optional, OneOrMore, OrderedChoice, ParserPython, PTNodeVisitor, visit_parse_tree, RegExMatch, UnorderedGroup, ZeroOrMore
from datetime import datetime
from ..utils import toStr, Utils

# For windows
lineSep = '\\r?\\n'


def ThriftRules():
    def endLine():
        # match - Line terminator
        return RegExMatch(r'({})?'.format(lineSep))

    def number():
        # match - Numbers
        return RegExMatch(r'\d*\.\d*|\d+')

    def commentBlock():
        # match - Any group of characters that are commented (/* & * & */)
        return RegExMatch(r'\/\*(.|{})*?\*\/'.format(lineSep)),

    def commentLine():
        # match - Any character, non line terminator
        return '//', RegExMatch(r'.*')

    def headerComments():
        return (
            OrderedChoice(
                ZeroOrMore(commentBlock),
                ZeroOrMore(commentLine)
            )
        )

    def header():
        return (
            headerComments,
            ''
        )

    def defHeader():
        return (
            # match - word or digit character one or more times
            RegExMatch(r'[\w\d]+'),  # name
            "{",
            # match - Any character (except line terminator) until # or line terminator
            Optional('//', RegExMatch(r'.*?(#|{})'.format(lineSep))),  # comment
            # match - Capture jadn_opts within comment, last } is matched one or more times
            Optional(RegExMatch(r'#?jadn_opts:{.*}+')),  # jadn options
            OneOrMore(endLine)
        )

    def defField():
        return (
            number,  # field number
            ':',
            # match - Any group until space
            RegExMatch(r'\w[\w\d\.]*?\s'),  # option
            # match - Any group until space OR any group enclosed within 'list<>'
            RegExMatch(r'\w[\w\d\.]*?\s|list\<([\w\d]+)\>*?\s'),  # type
            # match - Any group until space
            RegExMatch(r'(\w[\w\d]*?);'),  # name
            Optional(
                '//',
                # match - Any character (except line terminator) until # or line terminator
                RegExMatch(r'.*?(#|{})'.format(lineSep)),  # comment
                # match - Capture jadn_opts within comment, last } is matched one or more times
                Optional(RegExMatch(r'jadn_opts:{.*}+'))  # jadn options
            ),
            OneOrMore(endLine)
        )

    def structDef():
        return (
            'struct',
            defHeader,
            OneOrMore(defField),
            '}'
        )

    def enumField():
        return (
            # match - Any group until space
            RegExMatch(r'\w[\w\d]*?\s'),  # name
            '=',
            number,  # field number
            ';',
            Optional(
                '//',
                # match - Any character (except line terminator) until # or line terminator
                RegExMatch(r'.*?(#|{})'.format(lineSep)),  # comment
                # match - Capture jadn_opts within comment, last } is matched one or more times
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

    def wrappedDef():
        return (
            'struct',
            # match - Any group until a non word/digit
            RegExMatch(r'[\w\d]+'),
            '{',
            Optional(repeatedDef),
            '}'
        )

    def typeDefs():
        return OneOrMore(
            UnorderedGroup(
                ZeroOrMore(structDef),
                ZeroOrMore(enumDef),
                ZeroOrMore(wrappedDef)
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


class ThriftVisitor(PTNodeVisitor):
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
            # match - All information enclosed in {} from jadn_opts:
            optStr = re.sub(r'jadn_opts:(?P<opts>{.*?}+)', '\g<opts>', jadnString)

            try:
                optDict = json.loads(optStr)
                optDict['type'] = optDict['type'] if 'type' in optDict else defType
                optDict['options'] = Utils.opts_d2s(optDict['options']) if 'options' in optDict else []
            except Exception as e:
                print('Oops, cant load jadn')
                print(e)
        return optDict

    def visit_ThriftRules(self, node, children):
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
        # replace starting //(SPACE ONE OR MORE)
        return re.sub(r'^//\s*?', '', node.value)

    def visit_headerComments(self, node, children):
        if 'meta' not in self.data:
            self.data['meta'] = {}
        for child in children:
            if type(child) is list:
                for c in child:
                    # match - Starting (space)*(space)meta:
                    if re.match(r'^\s?\*\s?meta:', c):
                        # remove comment header so only the meta information is captured
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
            # Replace ending (space)#(space) with nothing
            re.sub(r'\s?#\S?$', '', children[1]) if len(children) >= 2 else ''  # comment
        ]

    def visit_defField(self, node, children):
        optDict = self.load_jadnOpts(children[-1], {
            'type': 'String',
            'options': []
        })

        return [
            children[0],  # field number
            # Replace starting or ending (space) with nothing
            re.sub(r'(^\s+|\s+$)', '', children[3].strip(';')),  # name
            self.repeatedTypes.get(optDict['type'], optDict['type']),  # type
            optDict['options'],  # options
            # Replace ending (space)#(space)
            re.sub(r'\s?#\S?$', '', children[4]) if len(children) >= 5 else ''  # comment
        ]

    def visit_structDef(self, node, children):
        msgFields = []
        for child in children[1:]:
            if type(child) is list:
                if child[2] in ['ArrayOf', 'Array']:
                    return [
                        children[0][0],  # name
                        child[2],  # type
                        child[3],  # options
                        child[4]   # comment
                    ]
                msgFields.append(child)
            else:
                print('Struct child not type list')
                print(child)

        children[0].append(msgFields)
        return children[0]

    def visit_enumField(self, node, children):
        if len(children) >= 3 and re.match(r'^required starting enum number for thrift', children[-1]):
            return

        return [
            children[1],  # field number
            # Replace ending (space)#(space)
            re.sub(r'(^\s+|\s+$)', '', children[0]),  # name
            # Replace (space)#(space) or (space)LINE TERMINATOR(space) with nothing
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
                    print('JADN Cusom Fields Failed.')
                    print(e)
            else:
                print('Custom Something..')
                print(child)


def thrift2jadn_dumps(thrift):
    """
    Produce jadn schema from thrift schema
    :arg thrift: Thrift Schema to convert
    :type thrift: str
    :return: jadn schema
    :rtype str
    """
    try:
        parser = ParserPython(ThriftRules)
        parse_tree = parser.parse(toStr(thrift))
        result = visit_parse_tree(parse_tree, ThriftVisitor())
        return Utils.jadnFormat(result, indent=2)

    except Exception as e:
        raise Exception('Thrift parsing error has occurred: {}'.format(e))


def thrift2jadn_dump(thrift, fname, source=""):
    with open(fname, "w") as f:
        if source:
            f.write("-- Generated from " + source + ", " + datetime.ctime(datetime.now()) + "\n\n")
        f.write(thrift2jadn_dumps(thrift))