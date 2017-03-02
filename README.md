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