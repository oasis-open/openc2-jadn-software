import json
import os
import unittest

from libs.codec.codec import Codec
from libs.codec.jadn import jadn_load
from libs.codec.codec_utils import flatten, fluff, dlist


class OpenC2(unittest.TestCase):

    def _write_examples(self, name, cmds):
        """
        Create example JSON files as a side effect of running unit tests
        """

        if True:        # Set to False to not write example files
            for n, encoding in enumerate(["", "_flat", "_concise", "_min"]):
                if cmds[n] is not None:
                    with open(os.path.join("examples", name + encoding + ".json"), "w") as f:
                        f.write(json.dumps(cmds[n]))

    def setUp(self):
        schema = jadn_load(os.path.join("schema", "openc2.jadn"))
        self.tc = Codec(schema)

    def test01_mitigate_domain(self):
        cmd_api = {
            "action": "mitigate",
            "target": {
                "domain_name": "cdn.badco.org"}}
        cmd_flat = {
            "action": "mitigate",
            "target.domain_name": "cdn.badco.org"
        }
        cmd_noname = {"1": 32, "2": {"7": "cdn.badco.org"}}
        cmd_concise = ["mitigate",{"domain_name": "cdn.badco.org"}]
        cmd_min = [32, {"7": "cdn.badco.org"}]

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
        self.assertEqual(flatten(cmd_api), cmd_flat)
        self.assertEqual(fluff(cmd_flat), cmd_api)
        self._write_examples("t01_mitigate_domain", [cmd_api, cmd_flat, cmd_concise, cmd_min])

    def test02_query_actions(self):
        cmd_api = {"action": "query", "target": {"openc2": {"actions":""}}}
        rsp_api = {
            "status": "OK",
            "results": {
                "strings":
                    ["query", "report", "notify", "start", "stop", "set", "delete", "update",
                     "investigate", "mitigate", "remediate"]}}

        self.tc.set_mode(True, True)        # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        self._write_examples("t02_query_actions", [cmd_api, None, None, None])
        self.assertEqual(self.tc.encode("OpenC2Response", rsp_api), rsp_api)
        self.assertEqual(self.tc.decode("OpenC2Response", rsp_api), rsp_api)
        self._write_examples("t02_query_actions_response", [rsp_api, None, None, None])

    def test02_query_schema(self):
        cmd_api = {"action": "query", "target": {"openc2": {"schema":""}}}
        schema = {          # JSON does not allow line breaks within strings for readability.  So encode struct into string.
            "meta": {
                "module": "openc2"
            },
            "types": [
                ["OpenC2Command", "Record", [], "", [
                    [1, "action", "Action", [], ""],
                    [2, "target", "Target", [], ""],
                    [3, "actuator", "Actuator", ["?"], ""],
                    [4, "modifiers", "Modifiers", ["?"], ""]]]]}
        rsp_api = {
            "status": "OK",
            "results": {"string": json.dumps(schema)}}

        self.tc.set_mode(True, True)        # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        self._write_examples("t02_query_schema", [cmd_api, None, None, None])
        self.assertEqual(self.tc.encode("OpenC2Response", rsp_api), rsp_api)
        self.assertEqual(self.tc.decode("OpenC2Response", rsp_api), rsp_api)
        self._write_examples("t02_query_schema_response", [rsp_api, None, None, None])

    def test03_contain_user(self):
        cmd_api = {
            "action": "contain",
            "target": {
                "user_account":{
                    "user_id": "21942",
                    "account_login": "jsmith",
                    "is_disabled": True,
                    "account_last_login": "2017-03-16T07:38:12-04:00"}}}

        cmd_flat = {
            "action": "contain",
            "target.user_account.user_id": "21942",
            "target.user_account.account_login": "jsmith",
            "target.user_account.is_disabled": True,
            "target.user_account.account_last_login": "2017-03-16T07:38:12-04:00"
        }

        cmd_noname = {
            "1":7,
            "2":{
                "19":{
                    "1": "21942",
                    "2": "jsmith",
                    "8": True,
                    "13": "2017-03-16T07:38:12-04:00"}}}

        cmd_concise = [
            "contain",{
                "user_account":{
                    "user_id": "21942",
                    "account_login": "jsmith",
                    "is_disabled": True,
                    "account_last_login": "2017-03-16T07:38:12-04:00"}}]

        cmd_min = [7,{"19":{"1":"21942","2":"jsmith","8": True,"13":"2017-03-16T07:38:12-04:00"}}]

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
        self.assertEqual(flatten(cmd_api), cmd_flat)
        self.assertEqual(fluff(cmd_flat), cmd_api)
        self._write_examples("t03_contain_user", [cmd_api, cmd_flat, cmd_concise, cmd_min])

    def test03_notify_email_addr(self):
        cmd_api = {
            "action": "notify",
            "target": {
                "email_addr":{
                    "value": "bruce@example.com",
                    "display_name": "Bruce Wayne"}}
        }

        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        self._write_examples("t03_notify_email_addr", [cmd_api, None, None, None])

    def test04_deny_ip(self):
        cmd_api = {
            "action": "deny",
            "target": {
                "ip_connection": {
                    "layer4_protocol": "TCP",
                    "src_addr": {"ipv6": "2001:0db8:85a3:0000:0000:8a2e:0370:7334"},
                    "src_port": {"number": 10996},
                    "dst_addr": {"ipv4": "1.2.3.5"},
                    "dst_port": {"protocol": "https"}
                }},
            "actuator": {
                "network_firewall": {"asset_id": "30"}},
            "modifiers": {
                "command_id": "pf17_8675309",
                "context": "91",
                "start_time": "2016-11-25T08:10:31-04:00",
                "duration": "PT2M30S"}}

        cmd_flat = {
            "action": "deny",
            "target.ip_connection.layer4_protocol": "TCP",
            "target.ip_connection.src_addr.ipv6": "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
            "target.ip_connection.src_port.number": 10996,
            "target.ip_connection.dst_addr.ipv4": "1.2.3.5",
            "target.ip_connection.dst_port.protocol": "https",
            "actuator.network_firewall.asset_id": "30",
            "modifiers.command_id": "pf17_8675309",
            "modifiers.context": "91",
            "modifiers.start_time": "2016-11-25T08:10:31-04:00",
            "modifiers.duration": "PT2M30S"
        }

        cmd_noname = {
            "1": 6,
            "2": {"15": {
                "1": {"2": "2001:0db8:85a3:0000:0000:8a2e:0370:7334"},
                "2": {"1": 10996},
                "3": {"1": "1.2.3.5"},
                "4": {"2": 443},
                "5": 6}},
            "3": {"14": {"2": "30"}},
            "4": {
                "1": "91",
                "2": "2016-11-25T08:10:31-04:00",
                "4": "PT2M30S",
                "6": "pf17_8675309"}}

        cmd_concise = [
            "deny",
            {"ip_connection": [
                {"ipv6": "2001:0db8:85a3:0000:0000:8a2e:0370:7334"},
                {"number": 10996},
                {"ipv4": "1.2.3.5"},
                {"protocol": "https"},
                "TCP"]},
            {"network_firewall": [None, "30"]},
            {"context": "91",
            "start_time": "2016-11-25T08:10:31-04:00",
            "duration": "PT2M30S",
            "command_id": "pf17_8675309"}]

        cmd_min = [6,
            {"15": [
                {"2": "2001:0db8:85a3:0000:0000:8a2e:0370:7334"},
                {"1": 10996},
                {"1": "1.2.3.5"},
                {"2": 443},
                6]},
            {"14": [None, "30"]},
            {"1": "91",
             "2": "2016-11-25T08:10:31-04:00",
             "4": "PT2M30S",
             "6": "pf17_8675309"}]

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
        self.assertEqual(flatten(cmd_api), cmd_flat)
        self.assertEqual(fluff(cmd_flat), cmd_api)
        self._write_examples("t04_deny_ip", [cmd_api, cmd_flat, cmd_concise, cmd_min])

    def test05_scan_domain(self):
        cmd_api = {           # API / Verbose (dict/name)
            "action": "scan",
            "target": {
                "domain_name": "www.example.com"}}

        cmd_flat = {
            "action": "scan",
            "target.domain_name": "www.example.com"}

        cmd_noname = {         # unused (dict/tag)
            "1": 1,
            "2": {
                "7": "www.example.com"}}

        cmd_concise = [        # Concise (list/name)
            "scan", {
                "domain_name": "www.example.com"}]

        cmd_min = [1,{"7":"www.example.com"}]

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
        self.assertEqual(flatten(cmd_api), cmd_flat)
        self.assertEqual(dlist(fluff(cmd_flat)), cmd_api)       # Convert numeric dict to list
        self._write_examples("t05_scan_domain", [cmd_api, cmd_flat, cmd_concise, cmd_min])

    def test06_update_software(self):
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
                "command_id": "474074afb389",
                "command_src": "dns://orch.example.org",
                "response": "ack",
                "source": "https://updates.example.org/win7_x64/patch_201704_0137.cab"}}

        cmd_flat = {
            "action": "update",
            "target.software.vendor": "McAfmantec",
            "target.software.name": "VirusBeGone",
            "actuator.process_remediation_service.actuator_id": "dns://host03274.example.org",
            "modifiers.command_id": "474074afb389",
            "modifiers.command_src": "dns://orch.example.org",
            "modifiers.response": "ack",
            "modifiers.source": "https://updates.example.org/win7_x64/patch_201704_0137.cab"}

        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(flatten(cmd_api), cmd_flat)
        self.assertEqual(dlist(fluff(cmd_flat)), cmd_api)  # Convert numeric dict to list
        self._write_examples("t06_update_software", [cmd_api, cmd_flat, None, None])

        # -- Response

        rsp_api = {
            "status": "Processing",
            "statusText": "Updating McAfmantec VirusBeGone ...",
            "response_src": "dns://orch.example.org",
            "command_ref": "474074afb389"}

        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Response", rsp_api), rsp_api)
        self.assertEqual(self.tc.decode("OpenC2Response", rsp_api), rsp_api)
        self._write_examples("t06_update_software_rsp", [rsp_api, None, None, None])

    def test07_update_file(self):
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
                "network_firewall": {"actuator_id": "dns://host03274.example.org"}}
        }
        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        self._write_examples("t07_update_file", [cmd_api, None, None, None])

    def test08_negotiation(self):
        cmd_api = {
            "action": "query",
            "target": {
                "openc2": {"comm_supported":""}
            },
            "actuator": {
                "any": {"actuator_id": "https://router7319.example.org"}}
        }
        rsp_api = {
            "status": "OK",
            "results": {
                "comms": {
                    "serialization": ["JSON", "JSON-min", "XML", "Protobuf"],
                    "connection": [{"DXL": {"channel": "c2-channel"}}]
                }
            }
        }
        cmd2_api = {
            "action": "set",
            "target": {
                "openc2": {
                    "comm_selected":{
                        "serialization": "Protobuf",
                        "connection": {
                            "REST": {
                                "port": {"protocol":"https"}}}}}},
            "actuator": {
                "any": {"actuator_id": "https://router7319.example.org"}}
        }
        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.encode("OpenC2Response", rsp_api), rsp_api)
        self.assertEqual(self.tc.decode("OpenC2Response", rsp_api), rsp_api)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd2_api), cmd2_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd2_api), cmd2_api)
        self._write_examples("t08_negotiation1", [cmd_api, None, None, None])
        self._write_examples("t08_negotiation2", [rsp_api, None, None, None])
        self._write_examples("t08_negotiation3", [cmd2_api, None, None, None])

    def test09_cancel_command(self):
        cmd_api = {
            "action": "cancel",
            "target": {
                "openc2": {"command": "b33cd1d4-aeb4-43a3-bfe9-806f4a84ef79"}}}

        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        self._write_examples("t09_cancel_command", [cmd_api, None, None, None])

    def test10_delete_email(self):
        cmd_api = {
            "action": "delete",
            "target": {
                "email_message": {
                    "date": "2017-06-07T14:30:31-04:00",
                    "from": {"value": "ginsu@spamco.org"},
                    "subject": "Special Offer!"
                }}}

        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        self._write_examples("t10_delete_email", [cmd_api, None, None, None])

    def test11_restart_process(self):      # TODO: use a real actuator
        cmd_api = {
            "action": "restart",
            "target": {
                "process": {
                    "pid": 17325,
                    "name": "rm -rf /*.*"
                }},
            "actuator": {
                "endpoint": {"actuator_id": "dns://i3494.hosts.example.com"}
            },
            "modifiers": {
                "method": {"stop": "graceful"}
            }
        }

        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        self._write_examples("t11_restart_process", [cmd_api, None, None, None])

    def test11_snapshot_process(self):      # TODO: use a real actuator
        cmd_api = {
            "action": "snapshot",
            "target": {
                "process": {
                    "creator_user": {"user_id": "jjadmin"}}},
            "actuator": {
                "endpoint": {"actuator_id": "dns://i3494.hosts.example.com"}
            },
            "modifiers": {
                "method": {"stop": "graceful"}
            }
        }

        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        self._write_examples("t11_snapshot_process", [cmd_api, None, None, None])

    def test12_locate_ipaddr(self):
        cmd_api = {
            "action": "locate",
            "target": {
                "ipv4_addr": "209.59.128.0/18"}}

        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        self._write_examples("t12_locate_ipaddr", [cmd_api, None, None, None])

    def test13_redirect_url(self):
        cmd_api = {
            "action": "redirect",
            "target": {
                "url": "https://www.shezuly.com/qqmusic.exe" }
        }

        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        self._write_examples("t13_redirect_url", [cmd_api, None, None, None])

    def test14_stop_user_session(self):
        cmd_api = {
            "action": "stop",
            "target": {
                "user_session": {
                    "effective-user": "john.public",
                    "effective-user-id": "17239",
                    "login-time": "2017-07-03T15:27:14-07:00"}}
        }

        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        self._write_examples("t14_stop_user_session", [cmd_api, None, None, None])

    def test15_report_artifact(self):
        cmd_api = {
            "action": "report",
            "target": {
                "artifact": {
                    "mime_type": "image/jpeg",
                    "hashes": {
                        "MD5": "79bdd30dca09def5b87c55a422382039",
                        "SHA-256": "1cb611150cc54216470836003c503b77b6a6840afd695cb7528b1ca40b82d4e7"}}}
        }

        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        self._write_examples("t15_report_artifact", [cmd_api, None, None, None])

    def test16_set_registry(self):
        cmd_api = {
            "action": "set",
            "target": {
                "windows_registry_key": {
                    "key": "HKEY_LOCAL_MACHINE\\System\Foo\Bar",
                    "values": [
                        {"name": "Foo", "data": "qwerty", "data_type": "REG_SZ"}
                    ]}}
        }

        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        self._write_examples("t16_set_registry", [cmd_api, None, None, None])

    def test17_investigate_x509_certificate(self):
        cmd_api = {
            "action": "investigate",
            "target": {
                "x509_certificate": {
                    "issuer": "C=ZA, ST=Western Cape, L=Cape Town, O=Thawte Consulting cc, "
                        "OU=Certification Services Division, CN=Thawte Server CA/emailAddress=server-cert@thawte.com",
                    "subject": "C=US, ST=Maryland, L=Pasadena, O=Brent Baccala, OU=FreeSoft, "
                        "CN=www.freesoft.org/emailAddress=baccala@freesoft.org",
                    "validity_not_before": "2016-03-12T12:00:00Z",
                    "validity_not_after": "2016-08-21T12:00:00Z"
                }}
        }

        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        self._write_examples("t17_investigate_x509_certificate", [cmd_api, None, None, None])

    def test18_allow_directory(self):
        cmd_api = {
            "action": "allow",
            "target": {
                "directory": {"path": "C:\\Windows\\System32"}}
        }

        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        self._write_examples("t18_allow_directory", [cmd_api, None, None, None])

    def test19_start_device(self):
        cmd_api = {
            "action": "start",
            "target": {
                "device": {
                    "manufacturer": "Dell",
                    "model": "E3500",
                    "serial_number": "12345CX678"
                }}
        }

        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        self._write_examples("t19_start_device", [cmd_api, None, None, None])

    def testb1_foo(self):       # Unknown action
        cmd_api = {
            "action": "foo",
            "target": {"device": {"model": "bar"}}}
        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        with self.assertRaises(ValueError):
            self.tc.encode("OpenC2Command", cmd_api)
        with self.assertRaises(ValueError):
            self.tc.decode("OpenC2Command", cmd_api)

    def testb2_scan(self):      # Unknown target device property
        cmd_api = {
            "action": "scan",
            "target": {
                "device": {"dummy": "bar"}
                }}
        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        with self.assertRaises(ValueError):
            self.tc.encode("OpenC2Command", cmd_api)
        with self.assertRaises(ValueError):
            self.tc.decode("OpenC2Command", cmd_api)


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
        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        with self.assertRaises(ValueError):
            self.tc.encode("OpenC2Command", cmd_api)
        with self.assertRaises(ValueError):
            self.tc.decode("OpenC2Command", cmd_api)

if __name__ == "__main__":
    unittest.main()
