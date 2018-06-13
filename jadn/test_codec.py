# This Python file uses the following encoding: utf-8
from __future__ import unicode_literals

import binascii
import unittest

from libs.codec.codec import Codec
from libs.codec.jadn import jadn_check

schema_basic = {                # JADN schema for datatypes used in Basic Types tests
    "meta": {"module": "unittests-BasicTypes"},
    "types": [
        ["t_bool", "Boolean", [], ""],
        ["t_int", "Integer", [], ""],
        ["t_num", "Number", [], ""],
        ["t_str", "String", [], ""],
        ["t_bin", "Binary", [], ""],
        ["t_array_of", "ArrayOf", ["*Integer"], ""],
        ["t_choice", "Choice", [], "", [
            [1, "type1", "String", [], ""],
            [4, "type2", "Boolean", [], ""],
            [7, "type3", "Integer", [], ""]]
        ],
        ["t_enum", "Enumerated", [], "", [
            [1, "first", ""],
            [15, "extra", ""],
            [8, "Chunk", ""]]
        ],
        ["t_enum_c", "Enumerated", ["="], "", [
            [1, "first", ""],
            [15, "extra", ""],
            [8, "Chunk", ""]]
         ],
        ["t_array", "Array", [], "", [
            [1, "fbool", "Boolean", ["[0"], ""],
            [2, "fint", "Integer", [], ""],
            [3, "fnum", "Number", [], ""],
            [4, "fstr", "String", ["[0"], ""],
            [5, "farr", "t_arr", ["[0"], ""],
            [6, "fao", "t_ao", ["[0"], ""]]
         ],
        ["t_arr", "Array", [], "", [
            [1, "", "Integer", [], ""],
            [2, "", "String", [], ""]]
        ],
        ["t_ao", "ArrayOf", ["*Integer"], ""],
        ["t_map", "Map", [], "", [
            [2, "red", "Integer", [], ""],
            [4, "green", "Integer", ["[0"], ""],
            [6, "blue", "Integer", [], ""],
            [9, "alpha", "Integer", ["[0"], ""]]
        ],
        ["t_rec", "Record", [], "", [
            [1, "red", "Integer", [], ""],
            [2, "green", "Integer", ["[0"], ""],
            [3, "blue", "Integer", [], ""],
            [4, "alpha", "Integer", ["[0"], ""]]
        ]
    ]}


class BasicTypes(unittest.TestCase):            # TODO: Test Array

    def setUp(self):
        jadn_check(schema_basic)
        self.tc = Codec(schema_basic)

    def test_primitive(self):   # Non-composed types (bool, int, num, str)
        self.assertEqual(self.tc.decode("t_bool", True), True)
        self.assertEqual(self.tc.decode("t_bool", False), False)
        self.assertEqual(self.tc.encode("t_bool", True), True)
        self.assertEqual(self.tc.encode("t_bool", False), False)
        with self.assertRaises(TypeError):
            self.tc.decode("t_bool", "True")
        with self.assertRaises(TypeError):
            self.tc.decode("t_bool", 1)
        with self.assertRaises(TypeError):
            self.tc.encode("t_bool", "True")
        with self.assertRaises(TypeError):
            self.tc.encode("t_bool", 1)

        self.assertEqual(self.tc.decode("t_int", 35), 35)
        self.assertEqual(self.tc.encode("t_int", 35), 35)
        with self.assertRaises(TypeError):
            self.tc.decode("t_int", 35.4)
        with self.assertRaises(TypeError):
            self.tc.decode("t_int", True)
        with self.assertRaises(TypeError):
            self.tc.decode("t_int", "hello")
        with self.assertRaises(TypeError):
            self.tc.encode("t_int", 35.4)
        with self.assertRaises(TypeError):
            self.tc.encode("t_int", True)
        with self.assertRaises(TypeError):
            self.tc.encode("t_int", "hello")

        self.assertEqual(self.tc.decode("t_num", 25.96), 25.96)
        self.assertEqual(self.tc.decode("t_num", 25), 25)
        self.assertEqual(self.tc.encode("t_num", 25.96), 25.96)
        self.assertEqual(self.tc.encode("t_num", 25), 25)
        with self.assertRaises(TypeError):
            self.tc.decode("t_num", True)
        with self.assertRaises(TypeError):
            self.tc.decode("t_num", "hello")
        with self.assertRaises(TypeError):
            self.tc.encode("t_num", True)
        with self.assertRaises(TypeError):
            self.tc.encode("t_num", "hello")

        self.assertEqual(self.tc.decode("t_str", "parrot"), "parrot")
        self.assertEqual(self.tc.encode("t_str", "parrot"), "parrot")
        with self.assertRaises(TypeError):
            self.tc.decode("t_str", True)
        with self.assertRaises(TypeError):
            self.tc.decode("t_str", 1)
        with self.assertRaises(TypeError):
            self.tc.encode("t_str", True)
        with self.assertRaises(TypeError):
            self.tc.encode("t_str", 1)

    def test_array_of(self):
        self.assertEqual(self.tc.decode("t_array_of", [1, 4, 9, 16]), [1, 4, 9, 16])
        self.assertEqual(self.tc.encode("t_array_of", [1, 4, 9, 16]), [1, 4, 9, 16])
        with self.assertRaises(TypeError):
            self.tc.decode("t_array_of", [1, "4", 9, 16])
        with self.assertRaises(TypeError):
            self.tc.decode("t_array_of", 9)
        with self.assertRaises(TypeError):
            self.tc.encode("t_array_of", [1, "4", 9, 16])
        with self.assertRaises(TypeError):
            self.tc.decode("t_array_of", 9)

    B1b = b"data to be encoded"
    B1s = "ZGF0YSB0byBiZSBlbmNvZGVk"
    B2b = "data\nto be ëncoded 旅程".encode(encoding="UTF-8")
    B2s = "ZGF0YQp0byBiZSDDq25jb2RlZCDml4XnqIs="
    B3b = binascii.a2b_hex("18e0c9987b8f32417ca6744f544b815ad2a6b4adca69d2c310bd033c57d363e3")
    B3s = "GODJmHuPMkF8pnRPVEuBWtKmtK3KadLDEL0DPFfTY+M="
    B_bad1b = "string"
    B_bad2b = 394
    B_bad3b = True
    B_bad1s = "ZgF%&0B++"

    def test_binary(self):
        self.assertEqual(self.tc.decode("t_bin", self.B1s), self.B1b)
        self.assertEqual(self.tc.decode("t_bin", self.B2s), self.B2b)
        self.assertEqual(self.tc.decode("t_bin", self.B3s), self.B3b)
        self.assertEqual(self.tc.encode("t_bin", self.B1b), self.B1s)
        self.assertEqual(self.tc.encode("t_bin", self.B2b), self.B2s)
        self.assertEqual(self.tc.encode("t_bin", self.B3b), self.B3s)
        with self.assertRaises((TypeError, binascii.Error)):
            self.tc.decode("t_bin", self.B_bad1s)
        with self.assertRaises(TypeError):
            self.tc.encode("t_bin", self.B_bad1b)
        with self.assertRaises(TypeError):
            self.tc.encode("t_bin", self.B_bad2b)
        with self.assertRaises(TypeError):
            self.tc.encode("t_bin", self.B_bad3b)

    C1a = {"type1": "foo"}
    C2a = {"type2": False}
    C3a = {"type3": 42}
    C1m = {"1": "foo"}
    C2m = {"4": False}
    C3m = {"7": 42}
    C1_bad1a = {"type1": 15}
    C1_bad2a = {"type5": "foo"}
    C1_bad3a = {"type1": "foo", "type2": False}
    C1_bad1m = {"1": 15}
    C1_bad2m = {"3": "foo"}
    C1_bad3m = {"1": "foo", "4": False}
    C1_bad4m = {1: "foo"}

    def test_choice_min(self):
        self.assertEqual(self.tc.decode("t_choice", self.C1m), self.C1a)
        self.assertEqual(self.tc.decode("t_choice", self.C2m), self.C2a)
        self.assertEqual(self.tc.decode("t_choice", self.C3m), self.C3a)
        self.assertEqual(self.tc.encode("t_choice", self.C1a), self.C1m)
        self.assertEqual(self.tc.encode("t_choice", self.C2a), self.C2m)
        self.assertEqual(self.tc.encode("t_choice", self.C3a), self.C3m)
        with self.assertRaises(TypeError):
            self.tc.decode("t_choice", self.C1_bad1m)
        with self.assertRaises(ValueError):
            self.tc.decode("t_choice", self.C1_bad2m)
        with self.assertRaises(ValueError):
            self.tc.decode("t_choice", self.C1_bad3m)
        with self.assertRaises(ValueError):
            self.tc.decode("t_choice", self.C1_bad4m)
        with self.assertRaises(TypeError):
            self.tc.encode("t_choice", self.C1_bad1a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_choice", self.C1_bad2a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_choice", self.C1_bad3a)


    def test_choice_verbose(self):
        self.tc.set_mode(True, True)
        self.assertEqual(self.tc.decode("t_choice", self.C1a), self.C1a)
        self.assertEqual(self.tc.decode("t_choice", self.C2a), self.C2a)
        self.assertEqual(self.tc.decode("t_choice", self.C3a), self.C3a)
        self.assertEqual(self.tc.encode("t_choice", self.C1a), self.C1a)
        self.assertEqual(self.tc.encode("t_choice", self.C2a), self.C2a)
        self.assertEqual(self.tc.encode("t_choice", self.C3a), self.C3a)

        with self.assertRaises(TypeError):
            self.tc.decode("t_choice", self.C1_bad1a)
        with self.assertRaises(ValueError):
            self.tc.decode("t_choice", self.C1_bad2a)
        with self.assertRaises(ValueError):
            self.tc.decode("t_choice", self.C1_bad3a)
        with self.assertRaises(TypeError):
            self.tc.encode("t_choice", self.C1_bad1a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_choice", self.C1_bad2a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_choice", self.C1_bad3a)


    def test_enumerated_min(self):
        self.assertEqual(self.tc.decode("t_enum", 15), "extra")
        self.assertEqual(self.tc.encode("t_enum", "extra"), 15)
        with self.assertRaises(ValueError):
            self.tc.decode("t_enum", 13)
        with self.assertRaises(TypeError):
            self.tc.decode("t_enum", "extra")
        with self.assertRaises(TypeError):
            self.tc.decode("t_enum", ["first"])
        with self.assertRaises(ValueError):
            self.tc.encode("t_enum", "foo")
        with self.assertRaises(TypeError):
            self.tc.encode("t_enum", 15)
        with self.assertRaises(TypeError):
            self.tc.encode("t_enum", [1])

    def test_enumerated_verbose(self):
        self.tc.set_mode(True, True)
        self.assertEqual(self.tc.decode("t_enum", "extra"), "extra")
        self.assertEqual(self.tc.encode("t_enum", "extra"), "extra")
        with self.assertRaises(ValueError):
            self.tc.decode("t_enum", "foo")
        with self.assertRaises(TypeError):
            self.tc.decode("t_enum", 42)
        with self.assertRaises(TypeError):
            self.tc.decode("t_enum", ["first"])
        with self.assertRaises(ValueError):
            self.tc.encode("t_enum", "foo")
        with self.assertRaises(TypeError):
            self.tc.encode("t_enum", 42)
        with self.assertRaises(TypeError):
            self.tc.encode("t_enum", ["first"])

    def test_enumerated_comp_min(self):
        self.assertEqual(self.tc.decode("t_enum_c", 15), 15)
        self.assertEqual(self.tc.encode("t_enum_c", 15), 15)
        with self.assertRaises(TypeError):
            self.tc.decode("t_enum_c", "extra")
        with self.assertRaises(TypeError):
            self.tc.encode("t_enum_c", "extra")

    def test_enumerated_comp_verbose(self):
        self.tc.set_mode(True, True)
        self.assertEqual(self.tc.decode("t_enum_c", 15), 15)
        self.assertEqual(self.tc.encode("t_enum_c", 15), 15)
        with self.assertRaises(TypeError):
            self.tc.decode("t_enum_c", "extra")
        with self.assertRaises(TypeError):
            self.tc.encode("t_enum_c", "extra")

    RGB1 = {"red": 24, "green": 120, "blue": 240}    # API (decoded) and verbose values Map and Record
    RGB2 = {"red": 50, "blue": 100}
    RGB3 = {"red": 9, "green": 80, "blue": 96, "alpha": 128}
    RGB_bad1a = {"red": 24, "green": 120}
    RGB_bad2a = {"red": 9, "green": 80, "blue": 96, "beta": 128}
    RGB_bad3a = {"red": 9, "green": 80, "blue": 96, "alpha": 128, "beta": 196}
    RGB_bad4a = {"red": "four", "green": 120, "blue": 240}
    RGB_bad5a = {"red": 24, "green": "120", "blue": 240}
    RGB_bad6a = {"red": 24, "green": 120, "bleu": 240}
    RGB_bad7a = {2: 24, "green": 120, "blue": 240}

    Map1m = {"2": 24, "4": 120, "6": 240}                  # Encoded values Map (minimized and dict/tag mode)
    Map2m = {"2": 50, "6": 100}
    Map3m = {"2": 9, "4": 80, "6": 96, "9": 128}
    Map_bad1m = {"2": 24, "4": 120}
    Map_bad2m = {"2": 9, "4": 80, "6": 96, "9": 128, "12": 42}
    Map_bad3m = {"2": "four", "4": 120, "6": 240}
    Map_bad4m = {2: 24, 4: 120, 6: 240}
    Map_bad5m = [24, 120, 240]

    Rec1m = [24, 120, 240]                          # Encoded values Record (minimized) and API+encoded Array values
    Rec2m = [50, None, 100]
    Rec3m = [9, 80, 96, 128]
    Rec_bad1m = [24, 120]
    Rec_bad2m = [9, 80, 96, 128, 42]
    Rec_bad3m = ["four", 120, 240]

    Rec1n = {"1": 24, "2": 120, "3": 240}                  # Encoded values Record (unused dict/tag mode)
    Rec2n = {"1": 50, "3": 100}
    Rec3n = {"1": 9, "2": 80, "3": 96, "4": 128}
    Rec_bad1n = {"1": 24, "2": 120}
    Rec_bad2n = {"1": 9, "2": 80, "3": 96, "4": 128, "5": 42}
    Rec_bad3n = {"1": "four", "2": 120, "3": 240}
    Rec_bad4n = {1: 24, 2: 120, 3: 240}

    RGB1c = [24, 120, 240]                           # Encoded values Record (concise)
    RGB2c = [50, None, 100]
    RGB3c = [9, 80, 96, 128]
    RGB_bad1c = [24, 120]
    RGB_bad2c = [9, 80, 96, 128, 42]
    RGB_bad3c = ["four", 120, 240]

    def test_map_min(self):             # dict structure, identifier tag
        self.assertDictEqual(self.tc.decode("t_map", self.Map1m), self.RGB1)
        self.assertDictEqual(self.tc.decode("t_map", self.Map2m), self.RGB2)
        self.assertDictEqual(self.tc.decode("t_map", self.Map3m), self.RGB3)
        self.assertDictEqual(self.tc.encode("t_map", self.RGB1), self.Map1m)
        self.assertDictEqual(self.tc.encode("t_map", self.RGB2), self.Map2m)
        self.assertDictEqual(self.tc.encode("t_map", self.RGB3), self.Map3m)
        with self.assertRaises(ValueError):
            self.tc.decode("t_map", self.Map_bad1m)
        with self.assertRaises(ValueError):
            self.tc.decode("t_map", self.Map_bad2m)
        with self.assertRaises(TypeError):
            self.tc.decode("t_map", self.Map_bad3m)
        with self.assertRaises(ValueError):
            self.tc.decode("t_map", self.Map_bad4m)
        with self.assertRaises(TypeError):
            self.tc.decode("t_map", self.Map_bad5m)
        with self.assertRaises(ValueError):
            self.tc.encode("t_map", self.RGB_bad1a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_map", self.RGB_bad2a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_map", self.RGB_bad3a)
        with self.assertRaises(TypeError):
            self.tc.encode("t_map", self.RGB_bad4a)
        with self.assertRaises(TypeError):
            self.tc.encode("t_map", self.RGB_bad5a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_map", self.RGB_bad6a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_map", self.RGB_bad7a)

    def test_map_unused(self):         # dict structure, identifier tag
        self.tc.set_mode(True, False)
        self.assertDictEqual(self.tc.decode("t_map", self.Map1m), self.RGB1)
        self.assertDictEqual(self.tc.decode("t_map", self.Map2m), self.RGB2)
        self.assertDictEqual(self.tc.decode("t_map", self.Map3m), self.RGB3)
        self.assertDictEqual(self.tc.encode("t_map", self.RGB1), self.Map1m)
        self.assertDictEqual(self.tc.encode("t_map", self.RGB2), self.Map2m)
        self.assertDictEqual(self.tc.encode("t_map", self.RGB3), self.Map3m)
        with self.assertRaises(ValueError):
            self.tc.decode("t_map", self.Map_bad1m)
        with self.assertRaises(ValueError):
            self.tc.decode("t_map", self.Map_bad2m)
        with self.assertRaises(TypeError):
            self.tc.decode("t_map", self.Map_bad3m)
        with self.assertRaises(ValueError):
            self.tc.decode("t_map", self.Map_bad4m)
        with self.assertRaises(ValueError):
            self.tc.encode("t_map", self.RGB_bad1a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_map", self.RGB_bad2a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_map", self.RGB_bad3a)
        with self.assertRaises(TypeError):
            self.tc.encode("t_map", self.RGB_bad4a)
        with self.assertRaises(TypeError):
            self.tc.encode("t_map", self.RGB_bad5a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_map", self.RGB_bad6a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_map", self.RGB_bad7a)

    def test_map_concise(self):         # dict structure, identifier name
        self.tc.set_mode(False, True)
        self.assertDictEqual(self.tc.decode("t_map", self.RGB1), self.RGB1)
        self.assertDictEqual(self.tc.decode("t_map", self.RGB2), self.RGB2)
        self.assertDictEqual(self.tc.decode("t_map", self.RGB3), self.RGB3)
        self.assertDictEqual(self.tc.encode("t_map", self.RGB1), self.RGB1)
        self.assertDictEqual(self.tc.encode("t_map", self.RGB2), self.RGB2)
        self.assertDictEqual(self.tc.encode("t_map", self.RGB3), self.RGB3)
        with self.assertRaises(ValueError):
            self.tc.decode("t_map", self.RGB_bad1a)
        with self.assertRaises(ValueError):
            self.tc.decode("t_map", self.RGB_bad2a)
        with self.assertRaises(ValueError):
            self.tc.decode("t_map", self.RGB_bad3a)
        with self.assertRaises(TypeError):
            self.tc.decode("t_map", self.RGB_bad4a)
        with self.assertRaises(TypeError):
            self.tc.decode("t_map", self.RGB_bad5a)
        with self.assertRaises(ValueError):
            self.tc.decode("t_map", self.RGB_bad6a)
        with self.assertRaises(ValueError):
            self.tc.decode("t_map", self.RGB_bad7a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_map", self.RGB_bad1a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_map", self.RGB_bad2a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_map", self.RGB_bad3a)
        with self.assertRaises(TypeError):
            self.tc.encode("t_map", self.RGB_bad4a)
        with self.assertRaises(TypeError):
            self.tc.encode("t_map", self.RGB_bad5a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_map", self.RGB_bad6a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_map", self.RGB_bad7a)

    def test_map_verbose(self):     # dict structure, identifier name
        self.tc.set_mode(True, True)
        self.assertDictEqual(self.tc.decode("t_map", self.RGB1), self.RGB1)
        self.assertDictEqual(self.tc.decode("t_map", self.RGB2), self.RGB2)
        self.assertDictEqual(self.tc.decode("t_map", self.RGB3), self.RGB3)
        self.assertDictEqual(self.tc.encode("t_map", self.RGB1), self.RGB1)
        self.assertDictEqual(self.tc.encode("t_map", self.RGB2), self.RGB2)
        self.assertDictEqual(self.tc.encode("t_map", self.RGB3), self.RGB3)
        with self.assertRaises(ValueError):
            self.tc.decode("t_map", self.RGB_bad1a)
        with self.assertRaises(ValueError):
            self.tc.decode("t_map", self.RGB_bad2a)
        with self.assertRaises(ValueError):
            self.tc.decode("t_map", self.RGB_bad3a)
        with self.assertRaises(TypeError):
            self.tc.decode("t_map", self.RGB_bad4a)
        with self.assertRaises(TypeError):
            self.tc.decode("t_map", self.RGB_bad5a)
        with self.assertRaises(ValueError):
            self.tc.decode("t_map", self.RGB_bad6a)
        with self.assertRaises(ValueError):
            self.tc.decode("t_map", self.RGB_bad7a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_map", self.RGB_bad1a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_map", self.RGB_bad2a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_map", self.RGB_bad3a)
        with self.assertRaises(TypeError):
            self.tc.encode("t_map", self.RGB_bad4a)
        with self.assertRaises(TypeError):
            self.tc.encode("t_map", self.RGB_bad5a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_map", self.RGB_bad6a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_map", self.RGB_bad7a)

    def test_record_min(self):
        self.assertDictEqual(self.tc.decode("t_rec", self.Rec1m), self.RGB1)
        self.assertDictEqual(self.tc.decode("t_rec", self.Rec2m), self.RGB2)
        self.assertDictEqual(self.tc.decode("t_rec", self.Rec3m), self.RGB3)
        self.assertEqual(self.tc.encode("t_rec", self.RGB1), self.Rec1m)
        self.assertEqual(self.tc.encode("t_rec", self.RGB2), self.Rec2m)
        self.assertEqual(self.tc.encode("t_rec", self.RGB3), self.Rec3m)
        with self.assertRaises(ValueError):
            self.tc.decode("t_rec", self.Rec_bad1m)
        with self.assertRaises(ValueError):
            self.tc.decode("t_rec", self.Rec_bad2m)
        with self.assertRaises(TypeError):
            self.tc.decode("t_rec", self.Rec_bad3m)
        with self.assertRaises(ValueError):
            self.tc.encode("t_rec", self.RGB_bad1a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_rec", self.RGB_bad2a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_rec", self.RGB_bad3a)
        with self.assertRaises(TypeError):
            self.tc.encode("t_rec", self.RGB_bad4a)
        with self.assertRaises(TypeError):
            self.tc.encode("t_rec", self.RGB_bad5a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_rec", self.RGB_bad6a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_rec", self.RGB_bad7a)

    def test_record_unused(self):
        self.tc.set_mode(True, False)
        self.assertDictEqual(self.tc.decode("t_rec", self.Rec1n), self.RGB1)
        self.assertDictEqual(self.tc.decode("t_rec", self.Rec2n), self.RGB2)
        self.assertDictEqual(self.tc.decode("t_rec", self.Rec3n), self.RGB3)
        self.assertEqual(self.tc.encode("t_rec", self.RGB1), self.Rec1n)
        self.assertEqual(self.tc.encode("t_rec", self.RGB2), self.Rec2n)
        self.assertEqual(self.tc.encode("t_rec", self.RGB3), self.Rec3n)
        with self.assertRaises(ValueError):
            self.tc.decode("t_rec", self.Rec_bad1n)
        with self.assertRaises(ValueError):
            self.tc.decode("t_rec", self.Rec_bad2n)
        with self.assertRaises(TypeError):
            self.tc.decode("t_rec", self.Rec_bad3n)
        with self.assertRaises(ValueError):
            self.tc.decode("t_rec", self.Rec_bad4n)
        with self.assertRaises(ValueError):
            self.tc.encode("t_rec", self.RGB_bad1a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_rec", self.RGB_bad2a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_rec", self.RGB_bad3a)
        with self.assertRaises(TypeError):
            self.tc.encode("t_rec", self.RGB_bad4a)
        with self.assertRaises(TypeError):
            self.tc.encode("t_rec", self.RGB_bad5a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_rec", self.RGB_bad6a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_rec", self.RGB_bad7a)

    def test_record_concise(self):
        self.tc.set_mode(False, True)
        self.assertDictEqual(self.tc.decode("t_rec", self.RGB1c), self.RGB1)
        self.assertDictEqual(self.tc.decode("t_rec", self.RGB2c), self.RGB2)
        self.assertDictEqual(self.tc.decode("t_rec", self.RGB3c), self.RGB3)
        self.assertEqual(self.tc.encode("t_rec", self.RGB1), self.RGB1c)
        self.assertEqual(self.tc.encode("t_rec", self.RGB2), self.RGB2c)
        self.assertEqual(self.tc.encode("t_rec", self.RGB3), self.RGB3c)
        with self.assertRaises(ValueError):
            self.tc.decode("t_rec", self.RGB_bad1c)
        with self.assertRaises(ValueError):
            self.tc.decode("t_rec", self.RGB_bad2c)
        with self.assertRaises(TypeError):
            self.tc.decode("t_rec", self.RGB_bad3c)
        with self.assertRaises(ValueError):
            self.tc.encode("t_rec", self.RGB_bad1a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_rec", self.RGB_bad2a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_rec", self.RGB_bad3a)
        with self.assertRaises(TypeError):
            self.tc.encode("t_rec", self.RGB_bad4a)
        with self.assertRaises(TypeError):
            self.tc.encode("t_rec", self.RGB_bad5a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_rec", self.RGB_bad6a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_rec", self.RGB_bad7a)

    def test_record_verbose(self):
        self.tc.set_mode(True, True)
        self.assertDictEqual(self.tc.decode("t_rec", self.RGB1), self.RGB1)
        self.assertDictEqual(self.tc.decode("t_rec", self.RGB2), self.RGB2)
        self.assertDictEqual(self.tc.decode("t_rec", self.RGB3), self.RGB3)
        self.assertDictEqual(self.tc.encode("t_rec", self.RGB1), self.RGB1)
        self.assertDictEqual(self.tc.encode("t_rec", self.RGB2), self.RGB2)
        self.assertDictEqual(self.tc.encode("t_rec", self.RGB3), self.RGB3)
        with self.assertRaises(ValueError):
            self.tc.decode("t_rec", self.RGB_bad1a)
        with self.assertRaises(ValueError):
            self.tc.decode("t_rec", self.RGB_bad2a)
        with self.assertRaises(ValueError):
            self.tc.decode("t_rec", self.RGB_bad3a)
        with self.assertRaises(TypeError):
            self.tc.decode("t_rec", self.RGB_bad4a)
        with self.assertRaises(TypeError):
            self.tc.decode("t_rec", self.RGB_bad5a)
        with self.assertRaises(ValueError):
            self.tc.decode("t_rec", self.RGB_bad6a)
        with self.assertRaises(ValueError):
            self.tc.decode("t_rec", self.RGB_bad7a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_rec", self.RGB_bad1a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_rec", self.RGB_bad2a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_rec", self.RGB_bad3a)
        with self.assertRaises(TypeError):
            self.tc.encode("t_rec", self.RGB_bad4a)
        with self.assertRaises(TypeError):
            self.tc.encode("t_rec", self.RGB_bad5a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_rec", self.RGB_bad6a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_rec", self.RGB_bad7a)


    Arr1 = [True, 3, 2.71828, "Red"]
    Arr2 = [None, 3, 2.71828]
    Arr3 = [True, 3, 2.71828, "Red", [1, "Blue"], [2, 3]]
    Arr4 = [True, 3, 2.71828, None, [1, "Blue"], [2, 3]]
    Arr_bad1 = [True, 3, None, "Red"]
    Arr_bad2 = [True, 3, False, "Red"]
    Arr_bad3 = [True, 3, 2.71828, "Red", []]
    Arr_bad4 = [True, 3, 2.71828, "Red", None, []]

    def test_array(self):

        def ta():
            self.assertListEqual(self.tc.encode("t_array", self.Arr1), self.Arr1)
            self.assertListEqual(self.tc.decode("t_array", self.Arr1), self.Arr1)
            self.assertListEqual(self.tc.encode("t_array", self.Arr2), self.Arr2)
            self.assertListEqual(self.tc.decode("t_array", self.Arr2), self.Arr2)
            self.assertListEqual(self.tc.encode("t_array", self.Arr3), self.Arr3)
            self.assertListEqual(self.tc.decode("t_array", self.Arr3), self.Arr3)
            self.assertListEqual(self.tc.encode("t_array", self.Arr4), self.Arr4)
            self.assertListEqual(self.tc.decode("t_array", self.Arr4), self.Arr4)
            with self.assertRaises(ValueError):
                self.tc.encode("t_array", self.Arr_bad1)
            with self.assertRaises(ValueError):
                self.tc.decode("t_array", self.Arr_bad1)
            with self.assertRaises(TypeError):
                self.tc.encode("t_array", self.Arr_bad2)
            with self.assertRaises(TypeError):
                self.tc.decode("t_array", self.Arr_bad2)
            with self.assertRaises(ValueError):
                self.tc.encode("t_array", self.Arr_bad3)
            with self.assertRaises(ValueError):
                self.tc.decode("t_array", self.Arr_bad3)
            with self.assertRaises(ValueError):
                self.tc.encode("t_array", self.Arr_bad4)
            with self.assertRaises(ValueError):
                self.tc.decode("t_array", self.Arr_bad4)

        # Ensure that mode has no effect on array serialization

        self.tc.set_mode(False, False)
        ta()
        self.tc.set_mode(False, True)
        ta()
        self.tc.set_mode(True, False)
        ta()
        self.tc.set_mode(True, True)
        ta()

schema_compound = {
    "meta": {"module": "unittests-Compound"},
    "types": [
        ["t_choice", "Choice", [], "", [
            [10, "rec", "t_crec", [], ""],
            [11, "map", "t_cmap", [], ""],
            [12, "array", "t_carray", [], ""],
            [13, "choice", "t_cchoice", [], ""]]
        ],
        ["t_crec", "Record", [], "", [
            [1, "a", "Integer", [], ""],
            [2, "b", "String", [], ""]]
        ],
        ["t_cmap", "Map", [], "", [
            [4, "c", "Integer", [], ""],
            [6, "d", "String", [], ""]]
        ],
        ["t_carray", "Array", [], "", [
            [3, "e", "Integer", [], ""],
            [5, "f", "String", [], ""]]
        ],
        ["t_cchoice", "Choice", [], "", [
            [7, "g", "Integer", [], ""],
            [8, "h", "String", [], ""]]
        ],
    ]}

class Compound(unittest.TestCase):      # TODO: arrayOf(rec,map,array,arrayof,choice), array(), map(), rec()

    def setUp(self):
        jadn_check(schema_compound)
        self.tc = Codec(schema_compound)

    C4a = {"rec": {"a": 1, "b": "c"}}
    C4m = {"10":[1,"c"]}

    def test_choice_rec_verbose(self):
        self.tc.set_mode(True, True)
        self.assertEqual(self.tc.decode("t_choice", self.C4a), self.C4a)
        self.assertEqual(self.tc.encode("t_choice", self.C4a), self.C4a)

    def test_choice_rec_min(self):
        self.tc.set_mode(False, False)
        self.assertEqual(self.tc.decode("t_choice", self.C4m), self.C4a)
        self.assertEqual(self.tc.encode("t_choice", self.C4a), self.C4m)


schema_selectors = {                # JADN schema for selector tests
    "meta": {"module": "unittests-Selectors"},
    "types": [
        ["t_attribute", "Record", [], "", [
            [1, "type", "String", [], ""],
            [2, "value", "", ["&type"], ""]]
        ],
        ["t_property_implicit_primitive", "Record", [], "", [
            [1, "foo", "String", [], ""],
            [2, "*", "Primitive", [], ""]]
        ],
        ["t_property_explicit_primitive", "Record", [], "", [
            [1, "foo", "String", [], ""],
            [2, "data", "Primitive", [], ""]]
        ],
        ["t_property_implicit_category", "Record", [], "", [
            [1, "foo", "String", [], ""],
            [2, "*", "Category", [], ""]]
         ],
        ["t_property_explicit_category", "Record", [], "", [
            [1, "foo", "String", [], ""],
            [2, "data", "Category", [], ""]]
         ],

        ["Primitive", "Choice", [], "", [
            [1, "name", "String", [], ""],
            [4, "flag", "Boolean", [], ""],
            [7, "count", "Integer", [], ""]]
        ],
        ["Category", "Choice", [], "", [
            [2, "animal", "Animals", [], ""],
            [6, "color", "Colors", [], ""]]
        ],
        ["Animals", "Map", [], "", [
            [3, "cat", "String", ["[0"], ""],
            [4, "dog", "Integer", ["[0"], ""],
            [5, "rat", "Rattrs", ["[0"], ""]]
        ],
        ["Colors", "Enumerated", [], "", [
            [2, "red", ""],
            [3, "green", ""],
            [4, "blue", ""]]
         ],
        ["Rattrs", "Record", [], "", [
            [1, "length", "Integer", [], ""],
            [2, "weight", "Number", [], ""]]
        ]
    ]}


class Selectors(unittest.TestCase):         # TODO: bad schema - verify * field has only Choice type
                                            # TODO: add test cases to decode multiple values for Choice (bad)
    def setUp(self):
        jadn_check(schema_selectors)
        self.tc = Codec(schema_selectors)

    attr1_api = {"type": "Integer", "value": 17}
    attr2_api = {"type": "Primitive", "value": {"count": 17}}
    attr3_api = {"type": "Category", "value": {"animal": {"rat": {"length": 21, "weight": .342}}}}
    attr4_bad_api = {"type": "Vegetable", "value": "turnip"}
    attr5_bad_api = {"type": "Category", "value": {"animal": {"fish": 10}}}

    def test_attribute_verbose(self):
        self.tc.set_mode(True, True)
        self.assertDictEqual(self.tc.encode("t_attribute", self.attr1_api), self.attr1_api)
        self.assertDictEqual(self.tc.decode("t_attribute", self.attr1_api), self.attr1_api)
        self.assertDictEqual(self.tc.encode("t_attribute", self.attr2_api), self.attr2_api)
        self.assertDictEqual(self.tc.decode("t_attribute", self.attr2_api), self.attr2_api)
        self.assertDictEqual(self.tc.encode("t_attribute", self.attr3_api), self.attr3_api)
        self.assertDictEqual(self.tc.decode("t_attribute", self.attr3_api), self.attr3_api)
        with self.assertRaises(ValueError):
            self.tc.encode("t_attribute", self.attr4_bad_api)
        with self.assertRaises(ValueError):
            self.tc.decode("t_attribute", self.attr4_bad_api)
        with self.assertRaises(ValueError):
            self.tc.encode("t_attribute", self.attr5_bad_api)
        with self.assertRaises(ValueError):
            self.tc.decode("t_attribute", self.attr5_bad_api)

    attr1_min = ["Integer", 17]
    attr2_min = ["Primitive", {"7": 17}]
    attr3_min = ["Category", {'2': {'5': [21, 0.342]}}]
    attr4_bad_min = ["Vegetable", {"7": 17}]
    attr5_bad_min = ["Category", {'2': {'9': 10}}]

    def test_attribute_min(self):
        self.tc.set_mode(False, False)
        self.assertListEqual(self.tc.encode("t_attribute", self.attr1_api), self.attr1_min)
        self.assertDictEqual(self.tc.decode("t_attribute", self.attr1_min), self.attr1_api)
        self.assertListEqual(self.tc.encode("t_attribute", self.attr2_api), self.attr2_min)
        self.assertDictEqual(self.tc.decode("t_attribute", self.attr2_min), self.attr2_api)
        self.assertListEqual(self.tc.encode("t_attribute", self.attr3_api), self.attr3_min)
        self.assertDictEqual(self.tc.decode("t_attribute", self.attr3_min), self.attr3_api)
        with self.assertRaises(ValueError):
            self.tc.encode("t_attribute", self.attr4_bad_api)
        with self.assertRaises(ValueError):
            self.tc.decode("t_attribute", self.attr4_bad_min)
        with self.assertRaises(ValueError):
            self.tc.encode("t_attribute", self.attr5_bad_api)
        with self.assertRaises(ValueError):
            self.tc.decode("t_attribute", self.attr5_bad_min)

    pep_api = {"foo": "bar", "data": {"count": 17}}
    pec_api = {"foo": "bar", "data": {"animal": {"rat": {"length": 21, "weight": .342}}}}
    pep_bad_api = {"foo": "bar", "data": {"turnip": ""}}

    def test_property_explicit_verbose(self):
        self.tc.set_mode(True, True)
        self.assertDictEqual(self.tc.encode("t_property_explicit_primitive", self.pep_api), self.pep_api)
        self.assertDictEqual(self.tc.decode("t_property_explicit_primitive", self.pep_api), self.pep_api)
        self.assertDictEqual(self.tc.encode("t_property_explicit_category", self.pec_api), self.pec_api)
        self.assertDictEqual(self.tc.decode("t_property_explicit_category", self.pec_api), self.pec_api)
        with self.assertRaises(ValueError):
            self.tc.encode("t_property_explicit_primitive", self.pep_bad_api)
        with self.assertRaises(ValueError):
            self.tc.decode("t_property_explicit_primitive", self.pep_bad_api)

    pep_min = ['bar', {'7': 17}]
    pec_min = ['bar', {'2': {'5': [21, 0.342]}}]
    pep_bad_min = ['bar', {'6': 17}]

    def test_property_explicit_min(self):
        self.tc.set_mode(False, False)
        self.assertListEqual(self.tc.encode("t_property_explicit_primitive", self.pep_api), self.pep_min)
        self.assertDictEqual(self.tc.decode("t_property_explicit_primitive", self.pep_min), self.pep_api)
        self.assertListEqual(self.tc.encode("t_property_explicit_category", self.pec_api), self.pec_min)
        self.assertDictEqual(self.tc.decode("t_property_explicit_category", self.pec_min), self.pec_api)
        with self.assertRaises(ValueError):
            self.tc.encode("t_property_explicit_primitive", self.pep_bad_api)
        with self.assertRaises(ValueError):
            self.tc.decode("t_property_explicit_primitive", self.pep_bad_min)

    pip_api = {"foo": "bar", "count": 17}
    pic_api = {"foo": "bar", "animal": {"rat": {"length": 21, "weight": .342}}}
    pip_bad1_api = {"foo": "bar", "value": "turnip"}
    pip_bad2_api = {"foo": "bar", "value": {"turnip": ""}}

    def test_property_implicit_verbose(self):
        self.tc.set_mode(True, True)
        self.assertDictEqual(self.tc.encode("t_property_implicit_primitive", self.pip_api), self.pip_api)
        self.assertDictEqual(self.tc.decode("t_property_implicit_primitive", self.pip_api), self.pip_api)
        self.assertDictEqual(self.tc.encode("t_property_implicit_category", self.pic_api), self.pic_api)
        self.assertDictEqual(self.tc.decode("t_property_implicit_category", self.pic_api), self.pic_api)
        with self.assertRaises(ValueError):
            self.tc.encode("t_property_implicit_primitive", self.pip_bad1_api)
        with self.assertRaises(ValueError):
            self.tc.decode("t_property_implicit_primitive", self.pip_bad1_api)
        with self.assertRaises(ValueError):
            self.tc.encode("t_property_implicit_primitive", self.pip_bad2_api)
        with self.assertRaises(ValueError):
            self.tc.decode("t_property_implicit_primitive", self.pip_bad2_api)

    pip_min = ["bar", {"7": 17}]
    pic_min = ["bar", {"2": {"5": [21, .342]}}]
    pip_bad1_min = []
    pip_bad2_min = []

    def test_property_implicit_min(self):
        self.tc.set_mode(False, False)
        self.assertListEqual(self.tc.encode("t_property_implicit_primitive", self.pip_api), self.pip_min)
        self.assertDictEqual(self.tc.decode("t_property_implicit_primitive", self.pip_min), self.pip_api)
        self.assertListEqual(self.tc.encode("t_property_implicit_category", self.pic_api), self.pic_min)
        self.assertDictEqual(self.tc.decode("t_property_implicit_category", self.pic_min), self.pic_api)
        with self.assertRaises(ValueError):
            self.tc.encode("t_property_implicit_primitive", self.pip_bad1_api)
        with self.assertRaises(ValueError):
            self.tc.decode("t_property_implicit_primitive", self.pip_bad1_min)
        with self.assertRaises(ValueError):
            self.tc.encode("t_property_implicit_primitive", self.pip_bad2_api)
        with self.assertRaises(ValueError):
            self.tc.decode("t_property_implicit_primitive", self.pip_bad2_min)


schema_listfield = {                # JADN schema for fields with cardinality > 1 (e.g., list of x)
    "meta": {"module": "unittests-ListField"},
    "types": [
        ["t_array", "ArrayOf", ["*String", "]2"], ""],  # Min array length default = 1, Max = 2
        ["t_opt_list", "Record", [], "", [
            [1, "string", "String", [], ""],
            [2, "list", "t_array", ["[0"], ""]]         # Min = 0, Max default = 1  (Array is optional)
        ],
        ["t_list_1_2", "Record", [], "", [
            [1, "string", "String", [], ""],
            [2, "list", "String", ["]2"], ""]]          # Min default = 1, Max = 2
        ],
        ["t_list_0_2", "Record", [], "", [
            [1, "string", "String", [], ""],
            [2, "list", "String", ["[0", "]2"], ""]]    # Min = 0, Max = 2
        ],
        ["t_list_2_3", "Record", [], "", [
            [1, "string", "String", [], ""],
            [2, "list", "String", ["[2","]3"], ""]]     # Min = 2, Max = 3
        ],
        ["t_list_1_n", "Record", [], "", [
            [1, "string", "String", [], ""],
            [2, "list", "String", ["]0"], ""]]          # Min default = 1, Max = 0 -> n
        ]]}

class ListField(unittest.TestCase):      # TODO: arrayOf(rec,map,array,arrayof,choice), array(), map(), rec()

    def setUp(self):
        jadn_check(schema_listfield)
        self.tc = Codec(schema_listfield)

    Lna = {"string": "cat"}                     # Cardinality 0..n field doesn't omit empty list.  Use ArrayOf type.
    Lsa = {"string": "cat", "list": "red"}      # Always invalid, value is a string, not a list of one string.
    L0a = {"string": "cat", "list": []}         # List fields SHOULD have minimum cardinality 1 to prevent this ambiguity.
    L1a = {"string": "cat", "list": ["red"]}
    L2a = {"string": "cat", "list": ["red", "green"]}
    L3a = {"string": "cat", "list": ["red", "green", "blue"]}

    def test_opt_list_verbose(self):        # n-P, s-F, 0-F, 1-P, 2-P, 3-F
        self.tc.set_mode(True, True)
        self.assertDictEqual(self.tc.encode("t_opt_list", self.Lna), self.Lna)
        self.assertDictEqual(self.tc.decode("t_opt_list", self.Lna), self.Lna)
        with self.assertRaises(TypeError):
            self.tc.encode("t_opt_list", self.Lsa)
        with self.assertRaises(TypeError):
            self.tc.decode("t_opt_list", self.Lsa)
        with self.assertRaises(ValueError):
            self.tc.encode("t_opt_list", self.L0a)
        with self.assertRaises(ValueError):
            self.tc.decode("t_opt_list", self.L0a)
        self.assertDictEqual(self.tc.encode("t_opt_list", self.L1a), self.L1a)
        self.assertDictEqual(self.tc.decode("t_opt_list", self.L1a), self.L1a)
        self.assertDictEqual(self.tc.encode("t_opt_list", self.L2a), self.L2a)
        self.assertDictEqual(self.tc.decode("t_opt_list", self.L2a), self.L2a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_opt_list", self.L3a)
        with self.assertRaises(ValueError):
            self.tc.decode("t_opt_list", self.L3a)

    def test_list_1_2_verbose(self):        # n-F, s-F, 0-F, 1-P, 2-P, 3-F
        self.tc.set_mode(True, True)
        with self.assertRaises(ValueError):
            self.tc.encode("t_list_1_2", self.Lna)
        with self.assertRaises(ValueError):
            self.tc.decode("t_list_1_2", self.Lna)
        with self.assertRaises(TypeError):
            self.tc.encode("t_list_1_2", self.Lsa)
        with self.assertRaises(TypeError):
            self.tc.decode("t_list_1_2", self.Lsa)
        with self.assertRaises(ValueError):
            self.tc.encode("t_list_1_2", self.L0a)
        with self.assertRaises(ValueError):
            self.tc.decode("t_list_1_2", self.L0a)
        self.assertDictEqual(self.tc.encode("t_list_1_2", self.L1a), self.L1a)
        self.assertDictEqual(self.tc.decode("t_list_1_2", self.L1a), self.L1a)
        self.assertDictEqual(self.tc.encode("t_list_1_2", self.L2a), self.L2a)
        self.assertDictEqual(self.tc.decode("t_list_1_2", self.L2a), self.L2a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_list_1_2", self.L3a)
        with self.assertRaises(ValueError):
            self.tc.decode("t_list_1_2", self.L3a)

    def test_list_0_2_verbose(self):        # n-P, s-F, 0-F, 1-P, 2-P, 3-F
        self.tc.set_mode(True, True)
        self.assertDictEqual(self.tc.encode("t_list_0_2", self.Lna), self.Lna)
        self.assertDictEqual(self.tc.decode("t_list_0_2", self.Lna), self.Lna)
        with self.assertRaises(TypeError):
            self.tc.encode("t_list_0_2", self.Lsa)
        with self.assertRaises(TypeError):
            self.tc.decode("t_list_0_2", self.Lsa)
        with self.assertRaises(ValueError):
            self.tc.encode("t_list_0_2", self.L0a)
        with self.assertRaises(ValueError):
            self.tc.decode("t_list_0_2", self.L0a)
        self.assertDictEqual(self.tc.encode("t_list_0_2", self.L1a), self.L1a)
        self.assertDictEqual(self.tc.decode("t_list_0_2", self.L1a), self.L1a)
        self.assertDictEqual(self.tc.encode("t_list_0_2", self.L2a), self.L2a)
        self.assertDictEqual(self.tc.decode("t_list_0_2", self.L2a), self.L2a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_list_0_2", self.L3a)
        with self.assertRaises(ValueError):
            self.tc.decode("t_list_0_2", self.L3a)

    def test_list_2_3_verbose(self):        # n-F, 0-F, 1-F, 2-P, 3-P
        self.tc.set_mode(True, True)
        with self.assertRaises(ValueError):
            self.tc.encode("t_list_2_3", self.Lna)
        with self.assertRaises(ValueError):
            self.tc.decode("t_list_2_3", self.Lna)
        with self.assertRaises(ValueError):
            self.tc.encode("t_list_2_3", self.L0a)
        with self.assertRaises(ValueError):
            self.tc.decode("t_list_2_3", self.L0a)
        with self.assertRaises(ValueError):
            self.tc.encode("t_list_2_3", self.L1a)
        with self.assertRaises(ValueError):
            self.tc.decode("t_list_2_3", self.L1a)
        self.assertDictEqual(self.tc.encode("t_list_2_3", self.L2a), self.L2a)
        self.assertDictEqual(self.tc.decode("t_list_2_3", self.L2a), self.L2a)
        self.assertDictEqual(self.tc.encode("t_list_2_3", self.L3a), self.L3a)
        self.assertDictEqual(self.tc.decode("t_list_2_3", self.L3a), self.L3a)

    def test_list_1_n_verbose(self):        # n-F, 0-F, 1-P, 2-P, 3-P
        self.tc.set_mode(True, True)
        with self.assertRaises(ValueError):
            self.tc.encode("t_list_1_n", self.Lna)
        with self.assertRaises(ValueError):
            self.tc.decode("t_list_1_n", self.Lna)
        with self.assertRaises(ValueError):
            self.tc.encode("t_list_1_n", self.L0a)
        with self.assertRaises(ValueError):
            self.tc.decode("t_list_1_n", self.L0a)
        self.assertDictEqual(self.tc.encode("t_list_1_n", self.L1a), self.L1a)
        self.assertDictEqual(self.tc.decode("t_list_1_n", self.L1a), self.L1a)
        self.assertDictEqual(self.tc.encode("t_list_1_n", self.L2a), self.L2a)
        self.assertDictEqual(self.tc.decode("t_list_1_n", self.L2a), self.L2a)
        self.assertDictEqual(self.tc.encode("t_list_1_n", self.L3a), self.L3a)
        self.assertDictEqual(self.tc.decode("t_list_1_n", self.L3a), self.L3a)


class Bounds(unittest.TestCase):        # TODO: check max and min string length, integer values, array sizes
                                        # TODO: Schema default and options
    def setUp(self):
        jadn_check(schema_bounds)
        self.tc = Codec(schema_bounds)


if __name__ == "__main__":
    unittest.main()
