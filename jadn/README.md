# Python JADN

## JADN
JSON Abstract Data Notation (JADN) is a language-neutral, platform-neutral,
and format-neutral mechanism for serializing structured data.  See [docs](docs/jadn-overview.md) for
information about the JADN language.

### Python package
The JADN package contains two subpackages:
- Codec -- Validate messages against JADN schema, serialize and deserialize messages
  - jadn-defs.py - Constant definitions for the JADN file format
  - jadn.py - Load, validate, and save JADN schemas
  - codec.py - Message encoder and decoder
  - codec_utils.py - Utility routines used with the Codec class
  - codec_format.py - Validation routines usable with the 'format' option
- Convert -- Translate a JADN schema to other formats.
  - w_markdown.py - Write schema as markdown tables
  - w_html - Write schema as html tables (prettier than markdown and customizable with css)
  - w_jas.py - Write schema in JAS IDL format (similar to ASN.1)
  - w_proto - Write schema in Proto3 IDL format
  - w_thrift - Write schema in Thrift IDL format

### Scripts
The JADN package was created using the Test Driven Development process, where tests containing desired results
are developed first, then software is written to make the tests pass.  Test scripts serve to document both
example data (good and bad cases) and calling conventions for the software.
- test_codec.py - Unit tests for encoder and decoder functions
- test_openc2.py - Unit tests for OpenC2 commands
- jadn-translate.py - Convert JADN schemas to other formats supported in the "convert" package

### Schemas
The jadn-translate utility reads `.jadn` schemas from an input directory (schema) and writes
converted files to an output directory (schema_gen).
- openc2-wd05.jadn - Schema that defines the OpenC2 message format as defined in the OpenC2
Language Specification, currently a work-in-progress document.  This schema is included
in the language specification and is used to generate the property tables in that spec.

## Building the python wheel package
- The wheel is build via GitLab CI
-  Building manually
	1. Install required packages for building - setuptools, wheel
		- setuptools should be installed with pip

		```bash
		pip install setuptools wheel
		```

	2. Run command to build the wheel
		
		```bash
		pip wheel . -w ./dist
		```
		
	3. Use the build whl as neeeded
		- The file is located in the dist folder named in the format of  
			{distribution}-{version}(-{build tag})?-{python tag}-{abi tag}-{platform tag}.whl

#### Note
- Oasis JADN [github](https://github.com/oasis-open/openc2-jadn/)
- Using [git flow](https://danielkummer.github.io/git-flow-cheatsheet/) for developement