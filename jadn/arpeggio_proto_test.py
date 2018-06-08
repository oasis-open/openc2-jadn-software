from __future__ import unicode_literals, print_function

import os
import re

from arpeggio import Optional, ZeroOrMore, OneOrMore, EOF, ParserPython, PTNodeVisitor, visit_parse_tree
from arpeggio import RegExMatch, UnorderedGroup

from libs.utils import toStr, Utils


def ProtoRules():
    endLine = re.sub(r'[\'\"]', '', repr(os.linesep))

    def number(): return RegExMatch(r'\d*\.\d*|\d+')

    def string(): return RegExMatch(r'\".*?\"')

    def syntax(): return RegExMatch(r'syntax\s?=\s?[\'\"].*?[\'\"];?({})?'.format(endLine))

    def package(): return RegExMatch(r'package\s?[\'\"]?.*?[\'\"]?;?({})?'.format(endLine))

    def headerComment(): return (
        RegExMatch(r'/\*'),
        # RegExMatch(r'(.|{})*'.format(endLine)),
        # RegExMatch(r'\*/')
    )

    def header():
        return UnorderedGroup(
            syntax,
            package,
            headerComment,
            OneOrMore(RegExMatch(r'(.|{})*'.format(endLine)))
        )

    return (
        header,
        OneOrMore(RegExMatch(r'.*')),
        EOF
    )


class ProtoVisitor(PTNodeVisitor):
    data = {}

    def visit__default__(self, node, children):
        # print(node.rule_name)
        if node.rule_name == 'ProtoRules':
            return self.data

        return PTNodeVisitor.visit__default__(self, node, children)


parser = ParserPython(ProtoRules)

schema = toStr(open(os.path.join('.', 'schema_gen_test', 'openc2-wd06.proto'), 'rb').read())

parse_tree = parser.parse(schema)

result = visit_parse_tree(parse_tree, ProtoVisitor())

jadn = Utils.jadnFormat(result, indent=2)

open(os.path.join('.', 'schema_gen_test', 'openc2-wd06_arpeggio.proto.jadn'), 'w+').write(jadn)
