from .jadn_defs import *

FORMAT_FUNCTIONS = (

# Semantic validation functions from JSON Schema
    'date-time',
    'date',
    'time',
    'email',
    'idn-email',
    'hostname',
    'idn-hostname',
    'ipv4',
    'ipv6',
    'uri',
    'uri-reference',
    'iri',
    'iri-reference',
    'uri-template',
    'json-pointer',
    'relative-json-pointer',
    'regex',

# Additional validation functions
    'duration',         # RFC 3339 Appendix A "duration"
    'ip-addr',          # Either an IPv4 or IPv6 address
    'port',             # Service Name or Transport Protocol Port Number, per IANA registry
    'mac-addr',         # 48 bit Media Access Code address
    'is-even',          # Silly example of a function that applies to integer instances, for testing
    'json',             # A json document
)
