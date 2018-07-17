<<<<<<< HEAD
## JADN
JSON Abstract Data Notation (JADN) is a JSON document format for defining abstract schemas.
Unlike concrete schema languages such as XSD and JSON Schema, JADN defines the structure of datatypes independently
of the serialization used to communicate and store data objects.  An encoder/decoder (codec) validates the structure
of data objects against the JADN schema and serializes/deserializes objects using a specified message format.  The
codec currently supports four JSON-based serialization formats, and can be extended to support XML and binary (CBOR,
Protocol Buffers, etc) serializations.

## JAS
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
=======
<div>
<h1>README</h1>

<div>
<h2><a id="readme-general">OASIS TC Open Repository: openc2-jadn</a></h2>

<p>This GitHub public repository ( <b><a href="https://github.com/oasis-open/openc2-jadn">https://github.com/oasis-open/openc2-jadn</a></b> ) was created at the request of the <a href="https://www.oasis-open.org/committees/openc2/">OASIS Open Command and Control (OpenC2) TC</a> as an <a href="https://www.oasis-open.org/resources/open-repositories/">OASIS TC Open Repository</a> to support development of open source resources related to Technical Committee work.</p>

<p>While this TC Open Repository remains associated with the sponsor TC, its development priorities, leadership, intellectual property terms, participation rules, and other matters of governance are <a href="https://github.com/oasis-open/openc2-jadn/blob/master/CONTRIBUTING.md#governance-distinct-from-oasis-tc-process">separate and distinct</a> from the OASIS TC Process and related policies.</p>

<p>All contributions made to this TC Open Repository are subject to open source license terms expressed in the <a href="https://www.oasis-open.org/sites/www.oasis-open.org/files/Apache-LICENSE-2.0.txt">Apache License v 2.0</a>.  That license was selected as the declared <a href="https://www.oasis-open.org/resources/open-repositories/licenses">"Applicable License"</a> when the TC Open Repository was created.</p>

<p>As documented in <a href="https://github.com/oasis-open/openc2-jadn/blob/master/CONTRIBUTING.md#public-participation-invited">"Public Participation Invited</a>", contributions to this OASIS TC Open Repository are invited from all parties, whether affiliated with OASIS or not.  Participants must have a GitHub account, but no fees or OASIS membership obligations are required.  Participation is expected to be consistent with the <a href="https://www.oasis-open.org/policies-guidelines/open-repositories">OASIS TC Open Repository Guidelines and Procedures</a>, the open source <a href="https://github.com/oasis-open/openc2-jadn/blob/master/LICENSE">LICENSE</a> designated for this particular repository, and the requirement for an <a href="https://www.oasis-open.org/resources/open-repositories/cla/individual-cla">Individual Contributor License Agreement</a> that governs intellectual property.</p>

</div>

<div>
<h2><a id="purposeStatement">Statement of Purpose</a></h2>

<p>Statement of Purpose for this OASIS TC Open Repository (openc2-jadn) as <a href="https://drive.google.com/open?id=0B-FunCZrr-vtNF9yanNjTlQtenc">proposed</a> and <a href="https://www.oasis-open.org/committees/ballot.php?id=3115">approved</a> [<a href="https://issues.oasis-open.org/browse/TCADMIN-2745">bis</a>] by the OpenC2 TC:</p>

<p>The purpose of the openc2-jadn GitHub repository is to (a) provide an abstract schema that is independent of serialization, and (b) provision a codebase for unit testing, validation of commands, and conversion of the abstract notation to various serializations.</p>

<p>Unlike concrete schema languages such as XSD and JSON Schema, JADN defines the structure of datatypes independently of the serialization used to communicate and store data objects. An encoder/decoder (codec) validates the structure of data objects against the JADN schema and serializes/deserializes objects using a specified message format.</p>

<p>The initial codebase for this repository is imported from the <a href="https://github.com/OpenC2-org/jadn">OpenC2 Forum's Github repository</a>.</p>

</div>

<div><h2><a id="purposeClarifications">Additions to Statement of Purpose</a></h2>

<p>[Repository Maintainers may include here any clarifications &mdash; any additional sections, subsections, and paragraphs that the Maintainer(s) wish to add as descriptive text, reflecting (sub-) project status, milestones, releases, modifications to statement of purpose, etc.  The project Maintainers will create and maintain this content on behalf of the participants.]</p>
</div>

<div>
<h2><a id="maintainers">Maintainers</a></h2>

<p>TC Open Repository <a href="https://www.oasis-open.org/resources/open-repositories/maintainers-guide">Maintainers</a> are responsible for oversight of this project's community development activities, including evaluation of GitHub <a href="https://github.com/oasis-open/openc2-jadn/blob/master/CONTRIBUTING.md#fork-and-pull-collaboration-model">pull requests</a> and <a href="https://www.oasis-open.org/policies-guidelines/open-repositories#repositoryManagement">preserving</a> open source principles of openness and fairness. Maintainers are recognized and trusted experts who serve to implement community goals and consensus design preferences.</p>

<p>Initially, the associated TC members have designated one or more persons to serve as Maintainer(s); subsequently, participating community members may select additional or substitute Maintainers, per <a href="https://www.oasis-open.org/resources/open-repositories/maintainers-guide#additionalMaintainers">consensus agreements</a>.</p>

<p><b><a id="currentMaintainers">Current Maintainers of this TC Open Repository</a></b></p>

<ul>
<li><a href="mailto:pavel.gutin@g2-inc.com">Pavel Gutin</a>; GitHub ID: <a href="https://github.com/pavel-gutin">https://github.com/pavel-gutin</a>; WWW: <a href="https://www.g2-inc.com/">G2, Inc</a></li>
<li><a href="mailto:dpkemp@radium.ncsc.mil">Dave Kemp</a>; GitHub ID: <a href="https://github.com/davaya">https://github.com/davaya</a>; WWW: <a href="http://www.nsa.gov/">Department of Defense</a></li>
</ul>

</div>

<div><h2><a id="aboutOpenRepos">About OASIS TC Open Repositories</a></h2>

<p><ul>
<li><a href="https://www.oasis-open.org/resources/open-repositories/">TC Open Repositories: Overview and Resources</a></li>
<li><a href="https://www.oasis-open.org/resources/open-repositories/faq">Frequently Asked Questions</a></li>
<li><a href="https://www.oasis-open.org/resources/open-repositories/licenses">Open Source Licenses</a></li>
<li><a href="https://www.oasis-open.org/resources/open-repositories/cla">Contributor License Agreements (CLAs)</a></li>
<li><a href="https://www.oasis-open.org/resources/open-repositories/maintainers-guide">Maintainers' Guidelines and Agreement</a></li>
</ul></p>

</div>

<div><h2><a id="feedback">Feedback</a></h2>

<p>Questions or comments about this TC Open Repository's activities should be composed as GitHub issues or comments. If use of an issue/comment is not possible or appropriate, questions may be directed by email to the Maintainer(s) <a href="#currentMaintainers">listed above</a>.  Please send general questions about TC Open Repository participation to OASIS Staff at <a href="mailto:repository-admin@oasis-open.org">repository-admin@oasis-open.org</a> and any specific CLA-related questions to <a href="mailto:repository-cla@oasis-open.org">repository-cla@oasis-open.org</a>.</p>

</div></div>

>>>>>>> 99aa7223575990d7831b739b0a19a5b4cb41d793
