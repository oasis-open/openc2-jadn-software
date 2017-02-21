import os
import unittest

from jaen.codec.codec import Codec
from jaen.codec.jaen import jaen_load


class OpenC2(unittest.TestCase):

    def setUp(self):
        jaen = jaen_load(os.path.join("data", "openc2.jaen"))
        self.tc = Codec(jaen)

    def test_query(self):
        cmd1_api = {"action": "query", "target": {"type": "commands"}}
        cmd1_flat = {"action": "query", "target.type": "commands"}
        cmd1_concise = ["query", ["commands"]]
        cmd1_noname = {1:3, 2:{1:2}}
        cmd1_min = [3,[2]]
                                        # Minified (list/tag)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd1_min), cmd1_api)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd1_api), cmd1_min)
        self.tc.set_mode(True, False)   # not named, but check dict/tag mode anyway
        self.assertEqual(self.tc.decode("OpenC2Command", cmd1_noname), cmd1_api)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd1_api), cmd1_noname)
        self.tc.set_mode(False, True)   # Concise (list/name)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd1_concise), cmd1_api)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd1_api), cmd1_concise)
        self.tc.set_mode(True, True)    # Verbose (dict/name)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd1_api), cmd1_api)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd1_api), cmd1_api)

if __name__ == "__main__":
    unittest.main()
