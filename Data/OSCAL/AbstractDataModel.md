# Metaschema and Data Models

The [Metaschema Information Modeling Framework](https://pages.nist.gov/metaschema/):

> Provides a common, format-agnostic modeling framework supporting schema, code,
> and documentation generation all in one".
>
> Current modeling technologies (i.e. XML Schema, JSON Schema, Schematron) are:
> * Uneven in their modeling expressiveness and validation capability
> * Bound to specific formats (i.e., XML, JSON, YAML)

The Metaschema framework includes a "built-in data model". RFC 3444 distinguishes between:
* **Information Model**: models managed objects in a manner independent of data transport details,
can be specified informally or by using a formal Abstract Data Modeling language such as UML, ASN.1, or JADN
* **Data Model**: models data objects using a Concrete Data Modeling language such as XSD for XML data,
JSON Schema for JSON data, or CDDL for CBOR data.

Figure 1 conceptually divides an information modeling framework into three layers:
1. Concrete schemas and format-specific data (the Data Model)
2. Abstract schemas and format-agnostic application state (the Information Model)
3. Everything else including documentation and transformations (the Framework)

An Abstract Data Model API between the Framework and Information/Data layers would
allow Framework functions to be applied uniformly to all data formats.  RDF defines
[Datatype](https://www.w3.org/TR/rdf12-concepts/#section-Datatypes) as consisting of
a lexical space, a value space, and a lexical-to-value mapping, but is based on XML Schema
definitions of both the lexical space (a set of Unicode strings) and value space (simple
strings, numbers and dates). An Information Model is also defined in terms of lexical
to value mappings, but extends both the lexical space (physical instances can be
Unicode strings or byte sequences) and value space (logical instances can be any primitive
or compound value) to support the full information modeling domain.

Metaschema currently uses XSD-defined elements without a clear separation between
the data and information layers, while JADN uses UML-based elements as the information
layer and formally-defined bindings between logical information instances
and lexical data instances. This is not just a theoretical difference - an
Information Model defines format-agnostic application values, not application values
that are tied to a specific data format.

For example, a logical [IPv4 Subnet](https://www.rfc-editor.org/rfc/rfc4632.html#section-3.1)
address includes a network number (prefix) and individual addresses within that network,
modeled as a 32 bit IPv4 address and an integer prefix length. Applications use any in-memory state
that is convenient to represent IPv4 subnet addresses for processing, with serialization based on
the information type consisting of the two components defined in RFC 4632:
```
IPv4-Net = Record
  1 addr        Binary {4..4}
  2 prefix_len  Integer {0..32}
```
Many lexical values can be mapped to the same logical value, including:
* JSON string: "192.168.72.14/24"
* JSON array: ["c0a8480e",24]
* JSON object: {"addr": "c0a8480e", "prefix_len": 24]
* XML content: \<IPv4-Net\>192.168.72.14/24\</IPv4-Net\>
* XML attributes: \<IPv4-Net addr="c0a8480e" prefix_len="24"/\>
* CBOR array: 82 1a c0a8480e 18 18 (8 bytes = array(2), unsigned(3,232,253,966), unsigned(24))

The data format defines which lexical value is used to serialize from and parse to the same in-memory
logical value. The logical value is unaffected by which lexical value was or will be serialized, and
the information type defines only lexical syntax, not usage constraints or semantics other than
assembly/field names that may appear in lexical data. Framework information is linked to/from all
abstract datatypes using a single namespaced path mechanism, e.g., "net:IPv4-Net/prefix_len".

The topics shown in Figure 1 and discussed below are candidate Framework and API capabilities,
subject to modification as suggested by further research.

![Metaschema Framework Diagram](../../Images/metaschema-framework.jpg)
**<div align="center">Fig 1. Information Modeling Framework Capabilities</div>**

## Documentation

## Includes vs. Imports

## Data Formats and Styles

## Namespaced Type References

## Path-based Field References

## Regex Pattern Anchoring

## Logical Values vs. Lexical Representations

## Syntactic Sugar Extensions

## Logical Datatypes as Framework Templates

## Type Inheritance

## Model References