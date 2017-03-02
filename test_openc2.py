import os
import unittest

from jaen.codec.codec import Codec
from jaen.codec.jaen import jaen_load
from jaen.codec.codec_utils import flatten, fluff


class OpenC2(unittest.TestCase):

    def setUp(self):
        jaen = jaen_load(os.path.join("data", "openc2.jaen"))
        self.tc = Codec(jaen)

    def test_query1(self):
        cmd1_min = [3,{"2":2}]
        cmd1_concise = ["query", {"commands":"schema"}]
        cmd1_noname = {"1":3, "2":{"2":2}}
        cmd1_api = {"action": "query", "target": {"commands":"schema"}}

                                        # Minified (list/tag)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd1_min), cmd1_api)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd1_api), cmd1_min)
        self.tc.set_mode(False, True)   # Concise (list/name)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd1_concise), cmd1_api)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd1_api), cmd1_concise)
        self.tc.set_mode(True, False)   # not used, but check dict/tag mode anyway
        self.assertEqual(self.tc.decode("OpenC2Command", cmd1_noname), cmd1_api)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd1_api), cmd1_noname)
        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd1_api), cmd1_api)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd1_api), cmd1_api)

    def test_query2(self):
        '''
        # Alternate Target Data Model Schemas
        cmd2_api2 = {           # Literal STIX Object
            "action": "scan",
            "target": {
                "0": {
                    "type": "domain-name",
                    "value": "www.example.com",
                    "resolves_to_refs": ["1", "2"]
                },
                "1": {
                    "type": "ipv4-addr",
                    "value": "198.51.100.2"
                },
                "2": {
                    "type": "domain-name",
                    "value": "ms34.example.com"
                }
            }
        }

        cmd2_api3 = {           # Type-Specifiers
            "action": "scan",
            "target": {
                "type": "domain-name",
                "specifiers": {
                    "value": "www.example.com",
                    "resolves_to": [{
                        "type": "ipv4-addr",
                        "value": "198.51.100.2"
                    },{
                        "type": "domain-name",
                        "value": "ms34.example.com"
                    }]
                }
            }
        }
        '''

        cmd2_min = [1,{"7":["www.example.com",[{"1":["198.51.100.2"]},{"3":["ms34.example.com"]}]]}]

        cmd2_concise = [        # Concise (list/name)
            "scan",
            {
                "domain-name": [
                    "www.example.com",
                    [
                        {"v4": ["198.51.100.2"]},
                        {"name": ["ms34.example.com"]}]]}]

        cmd2_noname = {         # unused (dict/tag)
            "1": 1,
            "2": {
                "7": {
                    "1": "www.example.com",
                    "2": [
                        {"1":{"1": "198.51.100.2"}},
                        {"3":{"1": "ms34.example.com"}}]}}}

        cmd2_api = {           # API / Verbose (dict/name)
            "action": "scan",
            "target": {
                "domain-name": {
                    "value": "www.example.com",
                    "resolves_to": [
                        {"v4": {"value": "198.51.100.2"}},
                        {"name": {"value": "ms34.example.com"}}]}}}

                                            # Minified (list/tag)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd2_api), cmd2_min)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd2_min), cmd2_api)
        self.tc.set_mode(False, True)       # Concise (list/name)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd2_concise), cmd2_api)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd2_api), cmd2_concise)
        self.tc.set_mode(True, False)       # unused (dict/tag)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd2_noname), cmd2_api)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd2_api), cmd2_noname)
        self.tc.set_mode(True, True)        # API / Verbose (dict/name)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd2_api), cmd2_api)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd2_api), cmd2_api)

    def test_flat(self):    # Copy of api commands from separate test cases
        cmd1_api = {"action": "query", "target": {"commands":"schema"}}
        cmd1_flat = {"action": "query", "target.commands":"schema"}
        cmd2_api = {           # API / Verbose (dict/name)
            "action": "scan",
            "target": {
                "domain-name": {
                    "value": "www.example.com",
                    "resolves_to": [
                        {"v4": {"value": "198.51.100.2"}},
                        {"name": {"value": "ms34.example.com"}}]}}}

        cmd2_flat = {           # Flattened
            "action": "scan",
            "target.domain-name.value": "www.example.com",
            "target.domain-name.resolves_to": [     # TODO: develop array notation for flattened values
                {"v4.value": "198.51.100.2"},
                {"name.value": "ms34.example.com"}]}

        self.assertEqual(flatten(cmd1_api), cmd1_flat)
        self.assertEqual(fluff(cmd1_flat), cmd1_api)
        f = flatten(cmd2_api)
        self.assertEqual(flatten(cmd2_api), cmd2_flat)
        self.assertEqual(fluff(cmd2_flat), cmd2_api)


if __name__ == "__main__":
    unittest.main()
