<!-- Generated from schema\jadn.jadn, Fri May 25 14:09:23 2018-->
## Schema
 . | . 
---|---
title: |JADN Syntax
module: |oasis-open.org/openc2/v1.0/jadn
version: |wd01
description: |Syntax of a JSON Abstract Data Notation (JADN) module.
exports: |Schema
##3.2 Structure Types
###3.2.1 Schema
Definition of a JADN file

**Schema (Record)**

ID|Name|Type|#|Description
---|---|---|---|---
1|meta|Meta|1|Information about the schema module
2|types|Type|1..n|Type definitions
###3.2.2 Meta
Meta-information about this schema

**Meta (Map)**

ID|Name|Type|#|Description
---|---|---|---|---
1|module|Uname|1|Module unique name
2|title|String|0..1|Title
3|version|String|0..1|Module version
4|description|String|0..1|Description
5|imports|Import|0..n|Imported modules
6|exports|String|0..n|Exported datatype names
###3.2.3 Import
Imported module id and unique name

**Import (Array)**

ID|Type|#|Description
---|---|---|---
1|Nsid|1|Local ID used within this module to refer to the imported module
2|Uname|1|Unique name of imported module
###3.2.4 Type


**Type (Array)**

ID|Type|#|Description
---|---|---|---
1|Identifier|1|Name of this datatype
2|JADN-Type|1|Base type
3|Option|1..n|Type options
4|String|1|Type description
5|JADN-Type|1..n|List of fields (for compound types)
###3.2.5 JADN-Type


**JADN-Type (Choice)**

ID|Name|Type|Description
---|---|---|---
1|Binary|Null|Octet sequence
2|Boolean|Null|True or False
3|Integer|Null|Whole number
4|Number|Null|Real number
5|Null|Null|Nothing
6|String|Null|Character sequence
7|Array|FullField|Ordered list of fields
8|ArrayOf|Null|Ordered list of fields of a specified type
9|Choice|FullField|One of a set of named fields
10|Enumerated|EnumField|One of a set of id:name pairs
11|Map|FullField|Unordered set of named fields
12|Record|FullField|Ordered list of named fields
###3.2.6 EnumField
Item definition for Enumerated types

**EnumField (Array)**

ID|Type|#|Description
---|---|---|---
1|Integer|1|Item ID
2|String|1|Item name
3|String|1|Item description
###3.2.7 FullField
Field definition for other compound types

**FullField (Array)**

ID|Type|#|Description
---|---|---|---
1|Integer|1|Field ID or ordinal position
2|Identifier|1|Field name
3|Identifier|1|Field type
4|Option|0..n|Field options
5|String|1|Field description
##3.3 Primitive Types


Name|Type|Description
---|---|---
Identifier|String|A string starting with an alpha char followed by zero or more alphanumeric / underscore / dash chars
Nsid|String|Namespace ID - a short identifier
Uname|String|Unique name of imported module
Option|String|Option string: 1st char = option id
