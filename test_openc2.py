import os
import unittest

from jaen.codec.codec import Codec
from jaen.codec.jaen import jaen_load
from jaen.codec.codec_utils import flatten, fluff


class OpenC2(unittest.TestCase):

    def setUp(self):
        jaen = jaen_load(os.path.join("data", "openc2.jaen"))
        self.tc = Codec(jaen)

    def test1_mitigate(self):
        cmd_api = {
            "action": "mitigate",
            "target": {
                "domain-name": {"value": "cdn.badco.org"}}}
        cmd_noname = {'1': 34, '2': {'7': {'1': 'cdn.badco.org'}}}
        cmd_concise = ["mitigate",{"domain-name": ["cdn.badco.org"]}]
        cmd_min = [34, {'7': ['cdn.badco.org']}]

                                            # Minified (list/tag)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_min)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_min), cmd_api)
        self.tc.set_mode(False, True)       # Concise (list/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_concise)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_concise), cmd_api)
        self.tc.set_mode(True, False)       # unused (dict/tag)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_noname)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_noname), cmd_api)
        self.tc.set_mode(True, True)        # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)

    def test2_deny(self):
        cmd_api = {
            "action": "deny",
            "target": {
                "ip-connection": {
                    "src-addr": {
                        "dns": {"value": "www.badco.com"}
                    },
                    "src-port": {
                        "protocol": "https"
                    },
                    "dst-addr": {
                        "v4": {"value": "192.168.1.1"}
                    },
                    "layer4-protocol": "TCP"
                }
            },
            "actuator": {
                "network-firewall": {"asset_id": "30"}},
            "modifiers": {
                "id": "pf17_8675309",
                "context_ref": 91,
                "datetime": "2016-11-25T08:10:31-04:00",
                "duration": "PT2M30S"}}

        cmd_noname = {
            "1": 7,
            "2": {"15": {
                "1": {"4": {"1": "www.badco.com"}},
                "2": {"2": 443},
                "3": {"1": {"1": "192.168.1.1"}},
                "6": 6}},
            "3": {"14": {"2": "30"}},
            "4": {
                "2": "PT2M30S",
                "4": "2016-11-25T08:10:31-04:00",
                "8": 91,
                "9": "pf17_8675309"}}

        cmd_concise = [
            "deny",
            {"ip-connection": [
                {"dns": ["www.badco.com"]},
                {"protocol": "https"},
                {"v4": ["192.168.1.1"]},
                None,
                None,
                "TCP"]},
            {"network-firewall": [None, "30"]},
            {"context_ref": 91,
            "datetime": "2016-11-25T08:10:31-04:00",
            "duration": "PT2M30S",
            "id": "pf17_8675309"}]

        cmd_min = [7,
            {"15": [
                {"4": ["www.badco.com"]},
                {"2": 443},
                {"1": ["192.168.1.1"]},
                None,
                None,
                6]},
            {"14": [None, "30"]},
            {"2": "PT2M30S",
            "4": "2016-11-25T08:10:31-04:00",
            "8": 91,
            "9": "pf17_8675309"}]

        """
        # Legacy schema:
        Actuator ::= RECORD {
            type         ActuatorType,
            specifiers   ActuatorObject.&type OPTIONAL
        }
        "actuator": {
            "type": "network-firewall",
            "specifiers": {
                "asset_id": "30"}}
        """
                                            # Minified (list/tag)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_min)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_min), cmd_api)
        self.tc.set_mode(False, True)       # Concise (list/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_concise)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_concise), cmd_api)
        self.tc.set_mode(True, False)       # unused (dict/tag)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_noname)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_noname), cmd_api)
        self.tc.set_mode(True, True)        # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)

    def test3_query1(self):
        cmd_api = {"action": "query", "target": {"commands":"schema"}}
        cmd_noname = {"1":3, "2":{"2":2}}
        cmd_concise = ["query", {"commands":"schema"}]
        cmd_min = [3,{"2":2}]

                                            # Minified (list/tag)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_min)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_min), cmd_api)
        self.tc.set_mode(False, True)       # Concise (list/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_concise)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_concise), cmd_api)
        self.tc.set_mode(True, False)       # unused (dict/tag)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_noname)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_noname), cmd_api)
        self.tc.set_mode(True, True)        # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)

    def test4_query2(self):
        '''
        # Alternate Target Data Model Schemas
        cmd_api2 = {           # Literal STIX Object
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

        cmd_api3 = {           # Type-Specifiers
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

        cmd_api = {           # API / Verbose (dict/name)
            "action": "scan",
            "target": {
                "domain-name": {
                    "value": "www.example.com",
                    "resolves_to": [
                        {"v4": {"value": "198.51.100.2"}},
                        {"name": {"value": "ms34.example.com"}}]}}}
        cmd_noname = {         # unused (dict/tag)
            "1": 1,
            "2": {
                "7": {
                    "1": "www.example.com",
                    "2": [
                        {"1":{"1": "198.51.100.2"}},
                        {"3":{"1": "ms34.example.com"}}]}}}
        cmd_concise = [        # Concise (list/name)
            "scan",
            {
                "domain-name": [
                    "www.example.com",
                    [
                        {"v4": ["198.51.100.2"]},
                        {"name": ["ms34.example.com"]}]]}]
        cmd_min = [1,{"7":["www.example.com",[{"1":["198.51.100.2"]},{"3":["ms34.example.com"]}]]}]

                                            # Minified (list/tag)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_min)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_min), cmd_api)
        self.tc.set_mode(False, True)       # Concise (list/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_concise)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_concise), cmd_api)
        self.tc.set_mode(True, False)       # unused (dict/tag)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_noname)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_noname), cmd_api)
        self.tc.set_mode(True, True)        # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)

    def test5_flat(self):       # Copy of api commands from separate test cases
        cmd1_api = {"action": "query", "target": {"commands":"schema"}}
        cmd1_flat = {"action": "query", "target.commands":"schema"}
        cmd2_api = {            # API / Verbose (dict/name)
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
