# JADN / Metaschema Comparison

JADN and the NIST [Metaschema Modeling Framework](https://pages.nist.gov/metaschema/) have the identical goal:
"Modeling information Quickly and Easily in Multiple Formats".  The reasons for doing so are identical and
well-documented by NIST.  JADN has a slightly different focus (emphasising the
[information-theoretic](https://en.wikipedia.org/wiki/Information_theory) aspects
of information modeling to support efficient communication) and slightly different details, but there is
enough in common for the Metaschema documentation to provide the structure for comparison. Each of the headinga
and bullets below are links to Metaschema, with JADN comparison in the bullet text.

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