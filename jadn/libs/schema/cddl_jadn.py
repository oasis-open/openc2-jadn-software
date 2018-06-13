import re
import os
import json
from datetime import datetime

from ..utils import toStr, Utils


class CDDLtoJADN(object):
    def __init__(self, cddl):
        """
        Schema converter for CDDL to JADN
        :param cddl:
        """

        self._cddl = toStr(cddl)

        self._structs = [
            ['Record', self._format_record],
            ['Choice', self._format_choice],
            ['Map', self._format_map],
            ['Enumerated', self._format_enumerated],
            ['Array', self._format_tmp],  # tmp until we have a schema to go off of
            ['ArrayOf', self._format_array_of]
        ]

    def jadn_dump(self):
        """
        Converts CDDL schema to JADN
        :return: Produced JADN schema
        :rtype str
        """

        jadn = self.make_jadn()
        #(Utils.jadnFormat(jadn, indent=2))
        return Utils.jadnFormat(jadn, indent=2)

    def make_jadn(self):
        """
        Converts cddl schema in to jadn format
        :return: data in jadn readable format
        :rtype: dict
        """
        section = "meta"
        meta = {}
        types = []
        jadn = {
            'meta': meta,
            'types': types
        }

        data = self._cddl.split(os.linesep)
        type_def = []
        for line in data[1:-1]:
            if line == '; types':
                section = 'types'
                continue
            elif line == '; Custom Defined Types':
                section = 'custom'
                continue

            if section == 'meta' and len(line) > 0:
                meta.update(self.make_meta(line))
            elif section == 'types':
                if len(line) > 0:
                    type_def.append(line)
                else:
                    types.append(self.make_types(type_def))
                    type_def = []
            elif section == 'custom' and len(line) > 0:
                types.append(self.make_custom(line))

        return jadn

    def make_meta(self, meta_line):
        """
        Creates header/meta for JADN schema
        :return: header for schema
        :rtype dict
        """
        tmp = {}

        # removes leading '; ' from cddl
        line = re.sub(r'^;\smeta:\s', '', meta_line)
        entry = re.search(r'^([a-z]+)', line).group(1)
        data = re.search(r'-\s(.*)', line).group(1)

        # convert to jadn readable format
        try:
            tmp[entry] = json.loads(data)
        except Exception as e:
            tmp[entry] = data

        return tmp

    def make_types(self, current_type):
        """
        Creates type definitions for JADN schema
        :return: type definitions for schema
        :rtype list
        """
        type_def = current_type
        for item in self._structs:
            if item[0] in type_def[0]:
                return item[1](type_def)

        return self._format_array_of(type_def[0])

    def make_custom(self, current_custom):
        """
        Creates type definitions from custom types for JADN Schema
        - Assumes custom type is only a single line
        :param current_custom:
        :return:
        """
        custom_type = []

        name_type = current_custom.split(' = ')
        name = name_type[0][0:-1]
        type_comment = name_type[1]
        type = type_comment.split(';')[0][1:-1]
        if type == 'bstr':
            type = 'String'
        comment = type_comment.split(';')[1][1:]

        custom_type.append(name)
        custom_type.append(type)
        if 'TBD syntax' not in current_custom:
            custom_type.append(["@" + name])
        else:
            custom_type.append([])
        custom_type.append(comment)

        return custom_type



    def _format_record(self, item):
        """
        Formats the type: Record, under types, to the JADN schema
        :param item: data associated with entry
        :return: data formatted to JADN
        """
        record = []

        # format type heading
        record.append(item[0].split(' ')[0].replace("_", "-"))
        record.append('Record')
        record.append([])
        comment = re.search(r'; (.*) #', item[0])
        if comment:
            record.append(comment.group(1))
        else:
            record.append('')

        record_data = []
        for line in item[1:-1]:
            data_entry = []
            is_optional = False
            field_num = re.search(r'\"field\": ([0-9]+).', line)
            if field_num:
                data_entry.append(int(field_num.group(1)))

            pre_comment = line.split(';')[0]

            # value considered optional
            if '?' in pre_comment:
                is_optional = True
                pre_comment = pre_comment[2:]

            # remove whitespace/unwanted characters
            pre_comment = pre_comment[2:]
            data_entry.append(re.search(r'^(.*):', pre_comment).group(1))
            data_entry.append(re.search(r'type\":\s\"(.*?)\"', line).group(1))

            if is_optional:
                data_entry.append(["[0"])
            else:
                data_entry.append([])

            comment = re.search(r'; (.+) #', line).group(1)
            data_entry.append(comment)
            record_data.append(data_entry)

        record.append(record_data)
        return record

    def _format_enumerated(self, item):
        """
        Formats the type: Enumerated, under types, to the JADN schema
        :param item: data associated with entry
        :return: data formatted to JADN
        """
        enum = []
        enum.append(item[1].split(' ')[0].replace("_", "-"))
        enum.append("Enumerated")
        if "options" in item[0]:
            enum.append(["="])  # todo: double check this
        else:
            enum.append([])
        comment = re.search(r'; (.+) #', item[0])
        if comment:
            enum.append(comment.group(1))
        else:
            enum.append("")

        enum_data = []
        for line in item[1:]:
            data_entry = []
            field_num = re.search(r'\"field\": ([0-9]+).', line)
            if field_num:
                data_entry.append(int(field_num.group(1)))
            data_entry.append(re.search(r'= \"(.+)\" ;', line).group(1))
            data_entry.append(re.search(r'; (.+) #', line).group(1))
            enum_data.append(data_entry)

        enum.append(enum_data)
        return enum

    def _format_choice(self, item):
        """
        Formats the type: Choice, under types, to the JADN schema
        :param item: data to be converted
        :return: data in JADN format
        :rtype: list
        """
        choice = []
        choice.append(item[0].split(' ')[0].replace("_", "-"))
        choice.append("Choice")
        choice.append([])
        comment = re.search(r'], \"(.*)\"', item[0])
        if comment:
            choice.append(comment.group(1))
        else:
            choice.append("")

        choice_data = []
        for line in item[1:-1]:
            data_entry = []

            field_num = re.search(r'\"field\": ([0-9]+).', line)
            if field_num:
                data_entry.append(int(field_num.group(1)))

            data_entry.append(line.split(":")[0][2:])
            data_entry.append(re.search(r'type\": \"(.*)\"', line).group(1))
            data_entry.append([])

            comment = re.search(r'; (.*) #', line)
            if comment:
                data_entry.append(comment.group(1))
            else:
                data_entry.append("")

            choice_data.append(data_entry)

        choice.append(choice_data)
        return choice

    def _format_map(self, item):
        """
        Formats the type: Map, under types, to the JADN schema
        :param item: data to be converted
        :return: data in JADN format
        :rtype: list
        """
        map = []
        is_optional = False
        map.append(item[0].split(' ')[0].replace("_", "-"))
        map.append("Map")
        map.append([])
        comment = re.search(r'; (.*) #', item[0])
        if comment:
            map.append(comment.group(1))
        else:
            map.append("")

        map_data = []
        for line in item[1:-1]:
            data_entry = []
            pre_comment = line.split(';')[0]

            field_num = re.search(r'\"field\": ([0-9]+).', line)
            if field_num:
                data_entry.append(int(field_num.group(1)))

            if '?' in pre_comment:
                is_optional = True
                data_entry.append(re.search(r'\?\s+(.*):', pre_comment).group(1))
            else:
                data_entry.append(re.search(r'^\s+(.*):', pre_comment).group(1))

            data_entry.append(re.search(r'type\": \"(.*)\",', line).group(1))

            if is_optional:
                data_entry.append(["[0"])
            else:
                data_entry.append([])

            map_data.append(data_entry)
            comment = re.search(r'; (.*) #', line)
            if comment:
                data_entry.append(comment.group(1))
            else:
                data_entry.append("")

        map.append(map_data)
        return map

    def _format_array_of(self, item):
        """
        Converts item of type ArrayOf to JADN format
        - note: based off of one example in schema, ie. subject to change
        :param item:
        :return:
        """
        arrayOf = []
        arr_name = item.split('=')[0][:-1]
        arrayOf.append(arr_name)
        arrayOf.append('ArrayOf')

        # put values inside outer_values as workaround for the way the jadn formatter seems to be working
        outer_values = []
        values = []

        # parse down to the items within brackets
        data_values = re.search(r'\[(.*)\]', item).group(1)

        # parse out ex: 0*3 Query_Item
        min = int(re.search(r'^([0-9]+)', data_values).group(1))
        max = int(re.search(r'.([0-9]+)', data_values).group(1))
        expr = re.search(r'[0-9]+(.)[0-9]+', data_values).group(1)
        type = re.search(r'\s(.+)$', data_values).group(1)

        values.append(expr+type)
        values.append('[' + str(min))
        values.append(']' + str(max))
        values.append(item.split(';')[1][1:])

        outer_values.append(values)
        arrayOf.append(outer_values)
        return arrayOf

    def _format_tmp(self, item):
        return [" ", " "]

def cddl2jadn_dumps(cddl):
    """
    Produce JADN schema from cddl schema
    :param cddl: CUDDL schema to convert
    :return: CUDDL schema
    :rtype str
    """
    return CDDLtoJADN(cddl).jadn_dump()


def cddl2jadn_dump(cddl, fname, source=""):
    with open(fname, "w") as f:
        if source:
            f.write("-- Generated from " + source + ", " + datetime.ctime(datetime.now()) + "\n\n")
        f.write(cddl2jadn_dumps(cddl))
