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

## Abstract Data Model API

The data that defines an Information Model / Abstract Data Model / Abstract Schema is a subset
of the Framework, which allows an ADM to be:
1) completely generated from framework data
2) used as a simple source to generate a template framework that can be fleshed out with additional information

The ADM defines itself, which:
1) limits its capabilities to those which can be expressed as a schema
2) allows it to be converted losslessly between data formats, which in turn means that all processing tools
that apply to a model in one format (e.g., XML) apply to all formats. This is analogous to processing
signals in the time domain or frequency domain, whichever is most convenient. The only constraint is that
tools must transform one valid ADM into another.
3) allows it to be displayed and discussed in a human-oriented format such as JADN Information
Definition Language (JIDL) text, before and after being processed by framework tools using a data format.

The topics shown in Figure 1 and discussed below are candidate Framework and ADM capabilities,
subject to modification as suggested by further research. 

![Metaschema Framework Diagram](../../Images/metaschema-framework.jpg)
**<div align="center">Fig 1. Information Modeling Framework Capabilities</div>**

### Documentation
One of Metaschema's primary purposes is to generate documentation, and it includes a rich and extensible
set of documentation mechanisms including formal names, descriptions, XML comments, remarks, and examples.
An excerpt from the `Group` assembly definition illustrates some types of embedded documentation:
```xml
  <define-assembly name="group">
    <formal-name>Control Group</formal-name>
    <description>A group of controls, or of groups of controls.</description>
    <define-flag name="id" as-type="token">
      <!-- This is an id because the identifier is assigned and managed externally by humans. -->
      <formal-name>Group Identifier</formal-name>
      <!-- Identifier Declaration -->
      <description>Identifies the group for the purpose of cross-linking within the defining instance or from other
        instances that reference the catalog.
      </description>
    </define-flag>

    <!-- ... -->

    <remarks>
      <p>Catalogs can use the catalog <code>group</code> construct to organize related controls into a single
        grouping, such as a family of controls or other logical organizational structure.
      </p>
      <p>A <code>group</code> may have its own properties, statements, parameters, and references, which are
        inherited by all controls of that are a member of the group.
      </p>
    </remarks>
    <example>
      <group xmlns="http://csrc.nist.gov/ns/oscal/1.0" id="xyz">
        <title>My Group</title>
        <prop name="required" value="some value"/>
        <control id="xyz1">
          <title>Control</title>
        </control>
      </group>
    </example>
  </define-assembly>
```
In contrast, the core of an information model defines abstract syntax to enable machine processing of messages.
It can include comments to assist model developers, but is intended as a machine-readable annex to a specification,
not the specification itself.

The IM `Group` definition includes descriptions copied from Metaschema's `<description>` elements, included to
demonstrate correspondence between framework and IM content, and truncated to emphasize that the IM is not the
documentation source.  The JSON or XML IM could include full copies of Metaschema descriptions
or none at all, but any documentation included in the IM does not affect message processing or code generation.

The compact presentation of the Group structure is itself a form of documentation, giving the reader a structural
overview that would be obscured by lengthy descriptions.

-- *Note that the `id` field is optional, a fact not readily apparent from inspecting the Metaschema definition.
That may (or may not) indicate a bug in the release from which it was derived.*
```
Groups = ArrayOf(Group){1..*}
Group = Record                               // A group of controls,
   1 id           TokenDatatype optional     // Identifies the group
   2 class        TokenDatatype optional     // A textual label that
   3 title        String                     // A name given to the 
   4 params       Params optional            // Parameters provide a
   5 props        Props optional             // An attribute, charac
   6 links        Links optional             // A reference to a loc
   7 parts        Parts optional             // An annotated, markup
   8 groups       Groups optional            // A group of controls,
   9 controls     Controls optional          // A structured object 
```

### Data Formats and Styles

### Namespaced Type References

### Path-based Field References

### Regex Pattern Anchoring

### Logical Values vs. Lexical Representations

### Syntactic Sugar Extensions

### Logical Datatypes as Framework Templates

### Type Inheritance

### Model References

