from __future__ import unicode_literals, print_function

import json
import re
import os

from arpeggio import EOF, Optional, OneOrMore, ParserPython, PTNodeVisitor, visit_parse_tree, RegExMatch, OrderedChoice, UnorderedGroup, ZeroOrMore

from libs.utils import toStr, Utils
lineSep = '\\r?\\n'


def CddlRules():

    def endLine():
        return RegExMatch(r'({})?'.format(lineSep))

    def commentLine():
        return ZeroOrMore(RegExMatch(r'\s*;.*'))

    def metaLine():
        # match:  "; meta: (COMMENT)"
        return RegExMatch(r'\s*;\smeta:\s*(.*)')

    def headerComments():
        return ZeroOrMore(metaLine)

    def header():
        return ZeroOrMore(headerComments)

    def defHeader():
        return (
            # matches name: "(NAME) = { ... }"
            ZeroOrMore(RegExMatch(r'^[\w]+')),
            # matches line up to jadn_opts
            ZeroOrMore(RegExMatch(r'.*?(#|{})')),
            # matches jadn_opts
            ZeroOrMore(RegExMatch(r'#?jadn_opts:{.*}+')),
            OneOrMore(endLine)
        )

    def defField():
        return (
            Optional('?'),
            # matches (TYPE) : ...
            RegExMatch(r'\s*[\w]+'),  # type
            # matches type : (NAME), ...
            RegExMatch(r':\s*[\w]+\s*,*'),  # name
            Optional('//'),
            Optional(
                ';',
                RegExMatch(r'.*?(#|{})'.format(lineSep)),  # comment
                Optional(RegExMatch(r'jadn_opts:{.*}+'))  # jadn options
            ),
            OneOrMore(endLine)
        )

    def recordDef():
        return (
            defHeader,
            OneOrMore(defField),
            Optional('}'), Optional(')'), Optional(']')
        )

    def enumField():
        return (
            # matches (ENUM) = ...
            RegExMatch(r'[\w]+'),  # enum name
            Optional('/='), Optional('='),
            # matches ... = (NAME)
            RegExMatch(r'\"[\w]+\"'),  # item name
            ';',
            Optional(
                RegExMatch(r'.*?(#|{})'.format(lineSep)),  # comment
                Optional(RegExMatch(r'jadn_opts:{.*}+'))  # jadn options
            ),
            OneOrMore(endLine)
        )

    def enumDef():
        return (
            defHeader,
            OneOrMore(enumField),
            OneOrMore(endLine)
        )

    def arrayOfDef():
        return (
            ZeroOrMore(RegExMatch(r'[\w]+')),  # name
            OneOrMore(RegExMatch(r'.*\]')),  # data up to comment
            ZeroOrMore(RegExMatch(r';[\s*\w]+'))
        )

    def typeDefs():
        return (OneOrMore(UnorderedGroup(
            ZeroOrMore(recordDef),
            ZeroOrMore(enumDef),
            ZeroOrMore(arrayOfDef)
        )))

    def customFields():
            return (
            ZeroOrMore(RegExMatch(r'[\w]+')),  # name
            ZeroOrMore('='),
            ZeroOrMore(RegExMatch(r'[\w]+')),  # type
            ZeroOrMore(RegExMatch(r';.*'))  # comment
        )

    def customDefs():
        return(OrderedChoice(
            Optional(commentLine),
            ZeroOrMore(customFields)
        ))

    return (
        header,
        typeDefs,
        customDefs,
        EOF
    )


class CddlVisitor(PTNodeVisitor):

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

    def visit_CddlRules(self, node, children):
        return self.data

    def visit_number(self, node, children):
        try:
            return float(node.value) if '.' in node.value else int(node.value)
        except Exception as e:
            print(e)

        return node.value

    def visit_metaLine(self, node, children):
        # removes "; meta: " from beginning of meta comment
        return re.sub(r';\s*meta:\s*', '', node.value)

    def visit_headerComments(self, node, children):
        if 'meta' not in self.data:
            self.data['meta'] = {}
        for child in children:
            line = child.split(' - ')
            try:
                self.data['meta'][line[0]] = json.loads(line[1])
            except Exception as e:
                self.data['meta'][line[0]] = (line[1][:-1])

    def visit_typeDefs(self, node, children):
        if 'types' not in self.data:
            self.data['types'] = []

        for child in children:
            if type(child) is list:
                self.data['types'].append(child)
            else:
                print('type child is not type list')

    def visit_defHeader(self, node, children):
        optDict = self.load_jadnOpts(children[-1], {
            'type': 'Record',
            'options': []
        })
        # remove unnecessary leading/trailing symbols from string "= { ; ... #"
        children[1] = re.sub(r'=|\(|;|\[|\{|#', '', children[1])
        # remove leading spaces
        children[1] = re.sub(r'^\s*', '', children[1])
        # remove trailing spaces
        children[1] = re.sub(r'\s*$', '', children[1])

        return [
            children[0],  # Type Name
            optDict['type'],  # Type
            optDict['options'],  # Options
            # remove unnecessary leading/trailing symbols from string "= { ; ... #"
            children[1] if len(children) >= 2 and 'jadn_opts' not in children[1] else ''  # comment
        ]

    def visit_defField(self, node, children):
        optDict = self.load_jadnOpts(children[-1], {
            'type': 'String',
            'options': []
        })

        if children[0] == '?':
            children = children[1:]
        return [
            optDict['field'] if 'field' in optDict else 0,
            re.sub(r'(:\s*)', '', children[0]),  # name
            optDict['type'] if 'type' in optDict else children[1],
            optDict['options'],  # options
            re.sub(r'\s?#\S?$', '', children[-2]) if children[-2] else ''  # comment
        ]

    def visit_recordDef(self, node, children):
        msgFields = []

        for child in children[1:-1]:
            if type(child) is list:
                msgFields.append(child)
            else:
                print('Message child not type list')
                print(child)

        children[0].append(msgFields)
        return children[0]

    def visit_enumHeader(self, node, children):
        optDict = self.load_jadnOpts(re.sub(r';\s*#', '', children[0]), {
            'type': 'String',
            'options': []
        })
        enumHeader = [
            "",
            optDict['type'],
            optDict['options'],
            # removes unnecessary characters '={;#'
            re.sub(r'=\s*{\s*;\s*|\s*#', '', children[1]) if len(children) >= 2 else ''  # comment
        ]
        return enumHeader

    def visit_enumField(self, node, children):
        optDict = self.load_jadnOpts(re.sub(r';\s*#', '', children[-1]), {
            'type': 'String',
            'options': [],
        })

        enumField = [
            children[0],
            optDict['field'],  # field number
            #removes leading/trailing spaces
            re.sub(r'(^\s+|\s+$)', '', children[2][1:-1]),  # name
            # removes unnecessary characters '={;#'
            re.sub(r'\s?(#|{})\S?$', '', children[3]) if len(children) >= 3 else ''  # comment
        ]
        return enumField

    def visit_enumDef(self, node, children):
        enumFields = []

        children[0][0] = children[1][0]
        name = children[0][0]

        for child in children[1:]:
            if type(child) is list and not (child[0] == 0 and re.match(r'^Unknown_{}'.format(name), child[1])):
                enumFields.append(child[1:])
            elif child[0] == 0 and re.match(r'^Unknown_{}'.format(name), child[1]):
                print('Enumerated field is placeholder')
                print(child)
            else:
                print('Enumerated field not type list')
                print(child)

        children[0].append(enumFields)
        return children[0]

    def visit_arrayOfDef(self, node, children):
        values = []
        data_values = re.search(r'(\[.*\])', children[1]).group(1)

        # parse out ex: 0*3 Query_Item
        min = int(re.search(r'(\d+)', data_values).group(1))
        max = int(re.search(r'.(\d+)', data_values).group(1))
        expr = re.search(r'[0-9]+(.)[0-9]+', data_values).group(1)
        type = re.search(r'\s([\w]+)', data_values).group(1)

        # result looks like ["*Query-Item", "[0", "]3"]
        values.append(expr+type)
        values.append('[' + str(min))
        values.append(']' + str(max))
        return [
            children[0],
            'ArrayOf',
            values,
            re.sub(r';\s*|\s*$', '', children[2])  # remove semi-colon and trailing spaces
        ]

    def visit_customFields(self, node, children):
        return [
            children[0],
            "String" if children[2] == 'bstr' else children[2],
            ["@"+children[0]] if 'TBD syntax' not in children[3] else [],
            re.sub(r';\s*', '', children[3][:-1]) if len(children) > 3 else ""
        ]

    def visit_customDefs(self, node, children):
        if 'types' not in self.data:
            self.data['types'] = []

        for child in children[1:]:
            if type(child) is list:
                self.data['types'].append(child)
            else:
                print('type child is not type list')


if __name__ == '__main__':
    debug = False
    debugDraw = (debug and False)
    schemaFile = 'openc2-wd06.cddl'

    parser = ParserPython(CddlRules, debug=False)
    schema = open(os.path.join('.', 'schema_gen_test', schemaFile), 'rb').read()
    parse_tree = parser.parse(toStr(schema))
    result = visit_parse_tree(parse_tree, CddlVisitor())

    jadn = Utils.jadnFormat(result, indent=2)
    open(os.path.join('.', 'schema_gen_test', schemaFile + '.jadn'), 'w+').write(jadn)
