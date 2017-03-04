import os
import json
from jaen.codec.codec import Codec
from jaen.codec.jaen import jaen_load

# OpenC2 producer application:

command = {
    "action": "mitigate",
    "target": {
        "domain-name": {
            "value": "cdn.badco.org"}}}

schema = jaen_load(os.path.join("data", "openc2.jaen"))     # Load and validate the OpenC2 schema
codec = Codec(schema, verbose_rec=True, verbose_str=True)   # Create an OpenC2 encoder/decoder (JSON-Verbose encoding)
message1 = codec.encode("OpenC2Command", command)           # Validate and encode the command
print("Sent Message =", json.dumps(message1))

# OpenC2 consumer application:

received_msg = '[34, {"7": ["cdn.badco.org"]}]'             # Received OpenC2 command in JSON-minified format
message2 = json.loads(received_msg)
codec.set_mode(verbose_rec=False, verbose_str=False)        # Tell codec to use JSON-minified encoding
command2 = codec.decode("OpenC2Command", message2)          # Validate and decode the command
print("Received Command =", command2)