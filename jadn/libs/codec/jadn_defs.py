"""
 JADN Definitions

A JSON Abstract Data Notation (JADN) file contains a list of datatype definitions.  Each type definition
has a specified format - a list of four or five columns depending on whether the type is primitive or
structure: (name, base type, type options, type description [, fields]).

For the enumerated type each field definition is a list of three items: (tag, name, description).

For other structure types (array, choice, map, record) each field definition is a list of five items:
(tag, name, type, field options, field description).
"""

from __future__ import unicode_literals

# JADN Datatype Definition columns
TNAME = 0       # Datatype name
TTYPE = 1       # Base type - built-in or defined
TOPTS = 2       # Type options
TDESC = 3       # Type description
FIELDS = 4      # List of fields

# JADN Field Definition columns
FTAG = 0        # Element ID
FNAME = 1       # Element name
EDESC = 2       # Enumerated value description
FTYPE = 2       # Datatype of field
FOPTS = 3       # Field options
FDESC = 4       # Field Description


# JADN built-in datatypes

PRIMITIVE_TYPES = (
    'Binary',
    'Boolean',
    'Integer',
    'Number',
    'Null',
    'String',
)

STRUCTURE_TYPES = (
    'Array',
    'ArrayOf',  # Special case: instance is a structure but type definition has no fields
    'Choice',
    'Enumerated',
    'Map',
    'Record',
)

# Option Tags/Keys
#   JADN Type Options (TOPTS) and Field Options (FOPTS) contain a list of strings, each of which is an option.
#   The first character of an option string is the type ID; the remaining characters are the value.
#   The option string is converted into a Name: Value pair before use.
#   The tables list the unicode codepoint of the ID and the corresponding Name.

TYPE_OPTIONS = {        # ID, value type, description
    0x3d: 'etag',       # '=', boolean, enumerated type is serialized as tag (name is ignored if present)
    0x5b: 'min',        # '[', integer, minimum string length, integer value, array length, property count
    0x5d: 'max',        # ']', integer, maximum string length, integer value, array length, property count
    0x23: 'aetype',     # '#', string, ArrayOf element type
    0x24: 'pattern',    # '$', string, regular expression that a string type must match
    0x40: 'format',     # '@', string, name of validation function, e.g., date-time, email, ipaddr, ...
}

FIELD_OPTIONS = {
    0x5b: 'min',        # '[', integer, minimum cardinality of field, default = 1, 0 = field is optional
    0x5d: 'max',        # ']', integer, maximum cardinality of field, default = 1, 0 = inherited max, not 1 = array
    0x26: 'atfield',    # '&', string, name of a field that specifies the type of this field
    0x2f: 'etype',      # '/', string, serializer-specific encoding type, e.g., u8, s16, hex, base64
    0x21: 'default',    # '!', string, default value for this field (coerced to field type)
}
