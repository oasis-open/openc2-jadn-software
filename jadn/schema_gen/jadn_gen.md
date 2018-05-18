<!-- Generated from schema\jadn.jadn, Thu May 17 16:23:36 2018-->
<!--
-->

# JADN Schema Syntax
## Module jadn, version 1.0 wd01
Syntax of a JSON Abstract Schema Notation (JADN) module.
## 3.2 Structure Types
### 3.2.1 JADN
Definition of a JADN file

**Type: Record**

|ID|Name|Type|#|Description|
|---:|---|---|---:|---|
|1|meta|SchemaMeta|1|Information about the schema module|
|2|types|SchemaType|1..n|Type definitions|
### 3.2.2 SchemaMeta
Meta-information about this schema

**Type: Map**

|ID|Name|Type|#|Description|
|---:|---|---|---:|---|
|1|module|String|1|Module name|
|2|title|String|0..1||
|3|version|String|0..1|Module version|
|4|description|String|0..1||
|5|imports|Import|0..n|List of imported modules|
### 3.2.3 Import


**Type: Array**

|ID|Name|Type|#|Description|
|---:|---|---|---:|---|
|1|nsid|String|1|Namespace identifier|
|2|name|String|1|Unique name of the defining module|
### 3.2.4 SchemaType


**Type: Array**

|ID|Name|Type|#|Description|
|---:|---|---|---:|---|
|1|name|String|1||
|2|type|JADN-Type|1|TODO: Need * option to  autogenerate enum from choice|
|3|options|String|1..n||
|4|description|String|1||
|5|fields|JADN-Type|1..n||
### 3.2.5 JADN-Type


**Type: Choice**

|ID|Name|Type|Description|
|---:|---|---|---|
|1|Binary|Null|Octet sequence|
|2|Boolean|Null|True or False|
|3|Integer|Null|Whole number|
|4|Number|Null|Real number|
|5|Null|Null|Nothing|
|6|String|Null|Character sequence|
|7|Array|FullField|Ordered list of fields|
|8|ArrayOf|Null|Ordered list of fields of a specified type|
|9|Choice|FullField|One of a set of named fields|
|10|Enumerated|EnumField|One of a set of id:name pairs|
|11|Map|FullField|Unordered set of named fields|
|12|Record|FullField|Ordered list of named fields|
### 3.2.6 EnumField
Field definition for Enumerated types

**Type: Array**

|ID|Name|Type|#|Description|
|---:|---|---|---:|---|
|1|id|Integer|1|Field ID|
|2|name|String|1|Field name|
|3|desc|String|1|Field description|
### 3.2.7 FullField
Field definition for types other than Enumerated

**Type: Array**

|ID|Name|Type|#|Description|
|---:|---|---|---:|---|
|1|id|Integer|1|Field ID or ordinal position|
|2|name|String|1|Field name|
|3|type|String|1|Field type|
|4|opts|String|0..n|Field optiona|
|5|desc|String|1|Field description|
## 3.3 Primitive Types
|Name|Type|Description|
|---|---|---|
