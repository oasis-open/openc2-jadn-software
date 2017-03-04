## JAEN
JSON Abstract Encoding Notation (JAEN, pronounced "Jane") is a JSON document format for defining abstract schemas.
Unlike concrete schema languages such as XSD and JSON Schema, JAEN defines the structure of datatypes independently
of the serialization used to communicate and store data objects.  An encoder/decoder (codec) validates the structure
of data objects against the JAEN schema and serializes/deserializes objects using a specified message format.

## JAS
JAEN Abstract Syntax (or perhaps JAen Source -- JAS) is a source format used to create JAEN files.  Although a JAEN
schema is a human-readable JSON document and can be edited directly, JAS is simpler to read and write, eliminating
the boilerplate (quotes, braces, brackets) inherent to JSON.  A converter utility translates a schema bidirectionally
between JAS and JAEN formats.

### JAEN Python package
The JAEN package contains two subpackages:
- Codec -- Validate messages against JAEN schema, serialize and deserialize messages
  - codec.py - Message encoder and decoder.
  - codec_utils.py - Utility routines used with the Codec class.
  - jaen.py - Load, validate, and save JAEN schemas.
- Convert -- Translate between JAEN, JAS, and property table files.
  - jas.ebnf - EBNF grammar for JAS files
  - jas_parse.py - JAS parser generated from EBNF by the Grako grammar compiler
  - tr_jas.py - load and save JAS files
  - tr_tables.py - generate property tables (.xlsx workbook format) from JAEN schema

### Scripts
The JAEN package was created using the Test Driven Development process, where tests containing desired results
are developed first, then software is written to make the tests pass.  Test scripts serve to document both
example data (good and bad cases) and calling conventions for the software.
- test_codec.py - Unit tests for encoder and decoder functions
- test_openc2.py - Unit tests for OpenC2 commands
   - This file contains example OpenC2 commands in API format and three JSON-encoded formats
   (Minified, Concise, and an unused format included for completeness of the codec test suite.)
- jaen-convert.py - Convert JAEN specifications between formats
   - openc2 - Schema that defines the OpenC2 message format, including the target data model.
   The ability to import data models is planned but not supported in the current version.

### Data
The converter utility reads `.jas` and `.jaen` schemas from an input directory (data) and writes
converted files to an output directory (data_gen).  Output files ending in `_genj` are
produced from JAEN sources, while those ending in `_gens` are produced from JAS sources.
After editing a JAS schema, the corresponding JAEN schema (`xxx_gens.jaen') should be moved
from the output to the input directory after deleting the source line at the top of the file.

### Getting Started
1. Use a Python 3 environment.  Install the jsonschema (for the codec)and XlsxWriter
(for the converter property table generator) packages if not already installed.
This software was developed under Python 3.5 and is not yet ported to Python 2.x.

2. Look at the test_openc2.py file for example OpenC2 commands in JSON format.

3. An OpenC2 producer application would create a python dict containing an OpenC2 command, load the
openc2.jaen schema, and encode the command:

```
import json
from jaen.codec.codec import Codec
from jaen.codec.jaen import jaen_load

command = {
    "action": "mitigate",
    "target": {
        "domain-name": {
            "value": "cdn.badco.org"}}}

schema = jaen_load("openc2.jaen")                           # Load and validate the OpenC2 schema
codec = Codec(schema, verbose_rec=True, verbose_str=True)   # Create an OpenC2 encoder/decoder (JSON-Verbose encoding)
message1 = codec.encode("OpenC2Command", command)           # Validate and encode the command
print("Sent Message =", json.dumps(message1))
```
4. An OpenC2 consumer application would receive an encoded message, then decode/validate it:
```
received_msg = '[34, {"7": ["cdn.badco.org"]}]'             # Received OpenC2 command in JSON-minified format
message2 = json.loads(received_msg)
codec.set_mode(verbose_rec=False, verbose_str=False)        # Tell codec to use JSON-minified encoding
command2 = codec.decode("OpenC2Command", message2)          # Validate and decode the command
print("Received Command =", command2)
```