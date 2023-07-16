# JADN / Metaschema Comparison

JADN and the NIST [Metaschema Modeling Framework](https://pages.nist.gov/metaschema/) have the identical goal:
"Modeling information Quickly and Easily in Multiple Formats".  The reasons for doing so are identical and
well-documented by NIST.  JADN has a somewhat different focus (emphasising the
[information-theoretic](https://en.wikipedia.org/wiki/Information_theory) aspects
of information modeling to support efficient *and lossless* communication) and different details, but there is
enough in common for the Metaschema documentation to provide the structure for comparison.
Each of the headings and bullets are links to the Metaschema specification, with JADN comparison below.

## [Overview](https://pages.nist.gov/metaschema/specification/overview/)
> The Metaschema framework currently supports XML, JSON, and YAML data formats. Support for YAML is limited
> to the subset of YAML that aligns with JSON representations. 
> This tight binding to supported derivative data formats has many advantages.

JADN defines information elements in a manner that supports a wider range of data formats, for example by
assigning numeric identifiers to all property names for use in concise data formats. The information-
theoretic approach's explicit goal is to isolate information from channel coding (data formats), and serialization
rules are a binding between the information model and one data format, independent of other data formats.

* [Information Model](https://pages.nist.gov/metaschema/specification/glossary/#information-model): 
Although JADN
[acknowledges](https://github.com/oasis-tcs/openc2-jadn-im/blob/working/imjadn-v1.0-cn02.md#22-information-models-and-data-models)
RFC 3444's definition of "describing information elements at a conceptual level", it is driven by
RFC 8477's
[Operational](https://github.com/oasis-tcs/openc2-jadn-im/blob/working/imjadn-v1.0-cn02.md#112-the-information-modeling-gap)
focus - an IM is an abstract but rigorous mechanism for expressing logical data requirements in a way that can be
unambiguously mapped to multiple data-level details.

## [Information Modeling](https://pages.nist.gov/metaschema/specification/information-modeling/)
> * An information model consists of information elements
> * A Metaschema module consists of definitions: Assembly, Flag, Choice, Field

* A JADN information model is a collection of one or more packages (module with namespace)
* A JADN package consists of definitions: simple, complex datatype, complex classtype
* A simple Choice is an enumeration, a complex Choice is a union of definitions

## [Graph Theoretical Basis of Metaschema](https://pages.nist.gov/metaschema/specification/information-modeling/#graph-theoretical-basis-of-metaschema)
> * Information elements are represented as nodes of the graph
> * A metaschema module is a directed graph
> * A metaschema module is a multigraph, since two nodes may be connected by multiple edges
> * A meteschema module is a cyclic graph
> * At least one root node must be defined
> * Nodes involved in a cycle must allow for termination, e.g., with zero minimum cardinality

* JADN definitions are nodes of the graph
* There are only two edge types: contain (copy) and reference, but edge names (field identifiers) can indicate purpose.
* A JADN model is a directed graph
* A JADN model is a multigraph (a node can have multiple incoming edges,
a complex node can have multiple outgoing edges, to the same or different nodes)
* A JADN model is a cyclic graph, but
    * `contain` edges SHOULD form a DAG (nesting is allowed to accommodate bad existing models,
    but at the risk of unbounded recursion)
    * `reference` edges (to complex classtype nodes) can be cyclic without restriction
* A DAG has a topological ordering that determines the root nodes, but converting an undirected cyclic graph to a DAG
means choosing the root nodes which determines the edge directions.
* Container nodes involved in a cycle must be terminated with zero minimum cardinality or converting edge to reference.

## [Object-Oriented Basis of Metaschema](https://pages.nist.gov/metaschema/specification/information-modeling/#object-oriented-basis-of-metaschema)
> * composition approach describes information elements
> * aligns with object-oriented programming, where data objects are instances of a class

* JADN definitions are always Classes, they may be implemented as OOP classes where `logical values` are public class variables
* For Metaschema example, Computer and ComputerPart are Classes, consistsOf and usbConnectionTo are properties of Computer,
and the Type of those properties must be either ComputerPart (copy of instance) or ComputerPart* (id of instance).
Defining edge types as contain or reference is part of designing the JADN model, as is defining the root node(s) when
converting from an undirected to directed graph.
* ComputerPart is a data type (does not have an id) unless the model is designed with pointers to (ids of) its instances.
* ComputerPart has a self reference (a graph cycle) that doesn't need to be broken if consistsOf is an id, not a copy.
(The real world will have both compound and simple (atomic) computer parts, so this example must terminate with atomic leaf nodes.)

## [Instances](https://pages.nist.gov/metaschema/specification/syntax/instances/)
> * An assembly definition may contain flag, field, or assembly instances

* Flag is a JADN simple datatype Class (instances are atomic values with no id and no children)
* JADN makes no distinction between assembly and field definitions - a complex (container) class has fields,
each with an identifier (outgoing edge label) and a destination Class (instances are simple datatype copy,
complex datatype/classtype copy, or classtype reference).

## [Data Types](https://pages.nist.gov/metaschema/specification/datatypes/)

> There are 2 kinds of data types.
> * simple data types
> * markup data types

JADN has three kinds of Classes (nodes):
* simple data types (the same xsd simple types as Metaschema, plus restriction-based model-defined types.)
* complex data types (containers with fields.)
* complex class types (containers with fields including id/key.)

JADN does not yet address structured prose text; it is unknown whether such text can be modeled as logical values
and losslessly round-trip serialized.


## Questions
* **Does Metaschema validate itself?**  It appears that information models can be created for application domains,
but has an information model that validates a Metaschema been created?, Is it possible to create one?
A JADN schema is a data object that can be serialized like any other, and can validate itself.
* **Is it technically possible to merge Metaschema and JADN?** JADN is organized around 'logical values',
format-independent application variables.  It's unclear whether logical values can be defined for markup text,
for example a `table` variable that captures everything of interest about tables and can be serialized in
HTML, Markdown, or ODT.  Is it possible to represent application domains like OSCAL by modeling structured
data values rather than markup prose?
* **Is there mutual interest in discovering whether merging is possible or desirable?**
Despite the identical name (Information Modeling) and goals, the details of modeling structured
prose appear to be significantly different from modeling structured data.