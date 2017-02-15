# JAEN
JSON Abstract Encoding Notation (JAEN, pronounced "Jane") is a JSON document format for defining abstract schemas.  Unlike concrete schema languages such as XSD and JSON Schema, JAEN defines the structure of datatypes independently of the serialization used to communicate and store data objects.  An encoder/decoder (codec) validates the structure of data objects against the JAEN schema and serializes/deserializes objects using a specified message format.

## JAS
JAEN Abstract Syntax (or perhaps JAen Source -- JAS) is a source format used to create JAEN files.  Although a JAEN schema is a human-readable JSON document and can be edited directly, JAS is simpler to read and write, eliminating boilerplate (quotes, braces, brackets) inherent in the JSON format.  A converter utility translates a schema bidirectionally between JAS and JAEN formats.
## Structure
