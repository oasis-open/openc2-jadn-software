# Information Modeling Tools
This repo contains software to:
* Process [JADN](https://docs.oasis-open.org/openc2/jadn/v1.0/cs01/jadn-v1.0-cs01.html)
information models (abstract schemas) used to define the
[OpenC2 Language Specification](http://docs.oasis-open.org/openc2/oc2ls/v1.0/oc2ls-v1.0.html)
and associated actuator profiles
* Validate OpenC2 data against an information model.

## Process Information Models
### Prerequisite
Install JADN software into a Python 3.8 or newer environment: `pip install jadn`

### Translate Information Models into Multiple Formats
The `make-artifacts.py` script 
### Resolve Namespaced References
### Create Device Schema

## Validate

--------------------------- obsolete below --------------------------------

JADN Abstract Syntax (or perhaps JADN Source -- JAS) is a source format used to create JADN files.  Although a JADN
schema is a human-readable JSON document and can be edited directly, JAS is simpler to read and write, eliminating
the boilerplate (quotes, braces, brackets) inherent to JSON.  A converter utility translates a schema bidirectionally
between JAS and JADN formats.

### JADN Python package
The JADN package contains two subpackages:
- Codec -- Validate messages against JADN schema, serialize and deserialize messages
  - codec.py - Message encoder and decoder.
  - codec_utils.py - Utility routines used with the Codec class.
  - jadn.py - Load, validate, and save JADN schemas.
- Convert -- Translate between JADN, JAS, and property table files.
  - jas.ebnf - EBNF grammar for JAS files
  - jas_parse.py - JAS parser generated from EBNF by the Grako grammar compiler
  - tr_jas.py - load and save JAS files
  - tr_tables.py - generate property tables (.xlsx workbook format) from JADN schema

### Scripts
The JADN package was created using the Test Driven Development process, where tests containing desired results
are developed first, then software is written to make the tests pass.  Test scripts serve to document both
example data (good and bad cases) and calling conventions for the software.
- test_codec.py - Unit tests for encoder and decoder functions
- test_openc2.py - Unit tests for OpenC2 commands
   - This file contains example OpenC2 commands in API format and four JSON-based formats:
   Verbose, Minified, Concise, and an unused format included for completeness of the codec test suite.
   The API format is the Python literal representation of a data item, similar but not identical to the
   JSON-Verbose serialization of that item ('single' vs. "double" quoted strings, True vs. true,
   None vs. null, etc.)
- jadn-convert.py - Convert JADN specifications between formats (Current: JAS, JADN, and property
 tables.  Potential: JSON schema, XSD, CDDL)

### Schemas
The converter utility reads `.jas` and `.jadn` schemas from an input directory (schema) and writes
converted files to an output directory (schema_gen).  Output files ending in `_genj` are
produced from JADN sources, while those ending in `_gens` are produced from JAS sources.
After editing a JAS schema, the corresponding JADN schema (`xxx_gens.jadn') should be moved
from the output to the input directory after deleting the source line at the top of the file.
- openc2.jadn - Schema that defines the OpenC2 message format, including the target data model.  The
ability to import data models from multiple schema files is planned but not supported
in the current version.

### Getting Started
1. Use a Python 3 environment.  Install the jsonschema (for the codec) and XlsxWriter
(for the converter property table generator) packages if not already installed.
This software was developed under Python 3.3-3.5 and is not yet ported to Python 2.x.

2. Look at the [examples](examples) folder for example OpenC2 commands in JSON format.
These files are generated automatically by the `test_openc2.py` unit test.

3. An OpenC2 producer application would create a python dict containing an OpenC2 command, load the
openc2.jadn schema, and encode the command:

```
import json
from libs.codec.codec import Codec
from libs.codec.jadn import jadn_load

command = {
    "action": "mitigate",
    "target": {
        "domain_name": {
            "value": "cdn.badco.org"}}}

schema = jadn_load("openc2.jadn")                           # Load and validate the OpenC2 schema
codec = Codec(schema, verbose_rec=True, verbose_str=True)   # Create an OpenC2 encoder/decoder (JSON-Verbose encoding)
message1 = codec.encode("OpenC2Command", command)           # Validate and encode the command
print("Sent Message =", json.dumps(message1))
```
4. An OpenC2 consumer application would receive an encoded message, then decode/validate it:
```
received_msg = '[32,{"7":["cdn.badco.org"]}]'               # Received OpenC2 command in JSON-minified format
message2 = json.loads(received_msg)
codec.set_mode(verbose_rec=False, verbose_str=False)        # Tell codec to use JSON-minified encoding
command2 = codec.decode("OpenC2Command", message2)          # Validate and decode the command
print("Received Command =", command2)
```
