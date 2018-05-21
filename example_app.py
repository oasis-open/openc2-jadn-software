import os
import json
from libs.codec.codec import Codec
from libs.codec.codec_utils import flatten
from libs.codec.jadn import jadn_load

# OpenC2 producer application:

command1 = {                     # Python literals use either single or double quotes - no difference in API object
    "action": "mitigate",
    'target': {
        "domain_name": 'cdn.badco.org'}}

schema = jadn_load(os.path.join("schema", "openc2.jadn"))   # Load and validate the OpenC2 schema
codec = Codec(schema, verbose_rec=True, verbose_str=True)   # Create an OpenC2 encoder/decoder (JSON-Verbose encoding)
message1 = codec.encode("OpenC2Command", command1)          # Validate and encode the command
print("Command to be sent (API)         =", command1)
print("Sent Message (JSON-v string)     =", json.dumps(message1))   # Single quotes are invalid in JSON

# OpenC2 consumer application:

message2 = '[32,{"7":"cdn.badco.org"}]'                     # Received OpenC2 command in JSON-minified format
codec.set_mode(verbose_rec=False, verbose_str=False)        # Tell codec to use JSON-minified encoding
command2 = codec.decode("OpenC2Command", json.loads(message2))      # Validate and decode the command
print("Received Message (JSON-m string) =", message2)
print("Decoded Command (API)            =", command2)
print("Decoded Command (API flat)       =", flatten(command2))