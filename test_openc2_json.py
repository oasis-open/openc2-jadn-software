import json
import jsonschema
import os
import unittest


class OpenC2(unittest.TestCase):

    # openc2_schema.json -- lenient
    # openc2_schema.strict.json -- strict
    # openc2_schema.strict.modified.json -- strict but no checks on specifiers

    def setUp(self):
        with open(os.path.join("schema", "openc2_schema.strict.json")) as f:
            self.openc2_schema = json.load(f)

    def test1_mitigate(self):
        cmd_api = {
            "action": "mitigate",
            "target": {
                "domain_name": {"value": "cdn.badco.org"}}}
        jsonschema.Draft4Validator(self.openc2_schema).validate(cmd_api)

    def test2_contain(self):
        cmd_api = {
            "action": "contain",
            "target": {
                "user_account":{
                    "user_id": "21942",
                    "account_login": "jsmith",
                    "is_disabled": True,
                    "account_last_login": "2017-03-16T07:38:12-04:00"}}}
        jsonschema.Draft4Validator(self.openc2_schema).validate(cmd_api)

    def test3_deny(self):
        cmd_api = {
            "action": "deny",
            "target": {
                "ip_connection": {
                    "src_addr": {"name": {"value": "www.badco.com"}},
                    "src_port": {"protocol": "https"},
                    "dst_addr": {"ipv4": {"value": "192.168.1.1"}},
                    "layer4_protocol": "TCP"
                }},
            "actuator": {
                "network_firewall": {"asset_id": "30"}},
            "modifiers": {
                "command_id": "pf17_8675309",
                "context": "91",
                "start_time": "2016-11-25T08:10:31-04:00",
                "duration": "PT2M30S"}}
        jsonschema.Draft4Validator(self.openc2_schema).validate(cmd_api)

    def test4_query(self):
        cmd_api = {"action": "query", "target": {"commands":"schema"}}
        jsonschema.Draft4Validator(cmd_api).validate(self.openc2_schema)

    def test5_scan(self):
        cmd_api = {           # API / Verbose (dict/name)
            "action": "scan",
            "target": {
                "domain_name": {
                    "value": "www.example.com",
                    "resolves_to": [
                        {"ipv4": {"value": "198.51.100.2"}},
                        {"name": {"value": "ms34.example.com"}}]}}}
        jsonschema.Draft4Validator(self.openc2_schema).validate(cmd_api)

    def test6_update_usecase(self):
        cmd_api = {         # API / Verbose (dict/name)
            "action": "update",
            "target": {
                "software": {
                    "name": "VirusBeGone",
                    "vendor": "McAfmantec"}},
            "actuator": {
                "process_remediation_service": {
                    "actuator_id": "dns://host03274.example.org"}},
            "modifiers": {
                "command_id": "5ce72...",
                "command_src": "dns://orch.example.org",
                "response": "ack",
                "source": "https://updates.example.org/win7_x64/patch_201704_0137.cab"}}
        jsonschema.Draft4Validator(self.openc2_schema).validate(cmd_api)

        # -- Response

        rsp_api = {
            "status": "Processing",
            "statusText": "Updating McAfmantec VirusBeGone ...",
            "response_src": "dns://orch.example.org",
            "command_id": "5ce72..."}

    def test7_joe(self):
        cmd_api = {
            "action": "update",
            "target": {
                "file": {
                    "parent_directory": {
                        "path":"\\\\someshared-drive\\somedirectory\\configurations"},
                    "name": "firewallconfiguration.txt"
                }
            },
            "actuator": {
                "network_firewall": {}
            }
        }
        jsonschema.Draft4Validator(self.openc2_schema).validate(cmd_api)

    def testb1_foo(self):       # Unknown action
        cmd_api = {
            "action": "foo",
            "target": {"device": {"model": "bar"}}}
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.Draft4Validator(self.openc2_schema).validate(cmd_api)

    def testb2_scan(self):      # Unknown target device property
        cmd_api = {
            "action": "scan",
            "target": {
                "device": {"dummy": "bar"}
                }}
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.Draft4Validator(self.openc2_schema).validate(cmd_api)

    def testb3_scan(self):      # Extra targets
        cmd_api = {
            "action": "scan",
            "target": {
                "device": {"model": "bar"},
                "author": "Charles Dickens",
                "title": "A Tale of Two Cities",
                "quote": "We had everything before us, we had nothing before us, we were all going direct to Heaven, "
                    "we were all going direct the other way— in short, the period was so far like the present period, "
                    "that some of its noisiest authorities insisted on its being received, for good or for evil, in the "
                    "superlative degree of comparison only."
                }}
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.Draft4Validator(self.openc2_schema).validate(cmd_api)

if __name__ == "__main__":
    unittest.main()
