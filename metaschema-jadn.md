# JADN / Metaschema Comparison

JADN and the NIST [Metaschema Modeling Framework](https://pages.nist.gov/metaschema/) have the identical goal:
"Modeling information Quickly and Easily in Multiple Formats".  The reasons for doing so are identical and
well-documented by NIST.  JADN has a slightly different focus (emphasising the
[information-theoretic](https://en.wikipedia.org/wiki/Information_theory) aspects
of information modeling to support efficient communication) and different details, but there is
enough in common for the Metaschema documentation to provide the structure for comparison.
Each of the headinga and bullets are links to Metaschema, with JADN comparison below.

## [Overview](https://pages.nist.gov/metaschema/specification/overview/)
> The Metaschema framework currently supports XML, JSON, and YAML data formats. Support for YAML is limited
> to the subset of YAML that aligns with JSON representations. 
> This tight binding to supported derivative data formats has many advantages.

JADN defines information elements in a manner that supports a wider range of data formats, for example by
assigning numeric identifiers to all property names for use in concise data formats.

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

* JADN definitions are nodes of the graph
* There are only two edge types: contain (copy) and reference.
* A JADN model is a directed graph
* A JADN model is a multigraph (a node can have multiple incoming edges,
a complex node can have multiple outgoing edges, to the same or different nodes)
* A JADN model is a cyclic graph, but
    * `contain` edges SHOULD form a DAG (nesting is allowed to accommodate bad existing models,
    but at the risk of unbounded recursion)
    * `reference` edges (to complex classtype nodes) can be cyclic without restriction

## [Data Types](https://pages.nist.gov/metaschema/specification/datatypes/)

> There are 2 kinds of data types.
> * simple data types
> * markup data types

JADN has three kinds of types oriented toward structured data:
* simple data types (the same xsd simple types as Metaschema)
* complex data types (containers with fields)
* complex class types (containers with fields that include id/key)

JADN does not address structured prose text (by lines, paragraphs, etc. 


## Questions
* **Does Metaschema validate itself?**  It appears that information models can be created for application domains,
but has an information model that validates a Metaschema been created?, Is it possible to create one?
* **Is it technically possible to merge Metaschema and JADN?**
* **Is there mutual interest in working to discover whether merging is possible or desirable?**