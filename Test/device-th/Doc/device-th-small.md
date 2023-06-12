         title: "Threat Hunting Profile"
       package: "https://praxiseng.com/threat-hunter-9001"
       version: "0-wd01"
   description: "Data definitions for Threat Hunting (TH) functions"
       exports: ["OpenC2-Command", "OpenC2-Response", "SCO"]
        config: {"$MaxBinary": 5555, "$MaxString": 5555, "$MaxElements": 555, "$Sys": "$", "$TypeName": "^[A-Za-z][-:_A-Za-z0-9]{0,63}$", "$FieldName": "^[A-Za-z][-:_A-Za-z0-9]{0,63}$", "$NSID": "^[A-Za-z][A-Za-z0-9]{0,7}$"}

The Command defines an Action to be performed on a Target

**Type: OpenC2-Command (Record)**

| ID | Name           | Type       | \#   | Description                                                                |
|----|----------------|------------|------|----------------------------------------------------------------------------|
| 1  | **action**     | Action     | 1    | The task or activity to be performed (i.e., the 'verb').                   |
| 2  | **target**     | Target     | 1    | The object of the Action. The Action is performed on the Target.           |
| 3  | **args**       | Args       | 0..1 | Additional information that applies to the Command.                        |
| 4  | **actuator**   | Actuator   | 0..1 | The subject of the Action. The Actuator executes the Action on the Target. |
| 5  | **command_id** | Command-ID | 0..1 | An identifier of this Command.                                             |

**********

**Type: OpenC2-Response (Map{1..\*})**

| ID | Name            | Type        | \#   | Description                                                                           |
|----|-----------------|-------------|------|---------------------------------------------------------------------------------------|
| 1  | **status**      | Status-Code | 1    | An integer status code                                                                |
| 2  | **status_text** | String      | 0..1 | A free-form human-readable description of the Response status                         |
| 3  | **results**     | Results     | 0..1 | Map of key:value pairs that contain additional results based on the invoking Command. |

**********

**Type: Action (Enumerated)**

| ID | Item            | Description                                                                                            |
|----|-----------------|--------------------------------------------------------------------------------------------------------|
| 3  | **query**       | Initiate a request for information.                                                                    |
| 30 | **investigate** | Task the recipient to aggregate and report information as it pertains to a security event or incident. |

**********

**Type: Target (Choice)**

| ID   | Name         | Type      | \# | Description                                                                        |
|------|--------------|-----------|----|------------------------------------------------------------------------------------|
| 9    | **features** | Features  | 1  | A set of items used with the query Action to determine an Actuator's capabilities. |
| 1036 | **th**       | AP-Target | 1  | Threat Hunting Profile-defined targets                                             |

**********

**Type: Args (Map{1..\*})**

| ID   | Name                   | Type          | \#   | Description |
|------|------------------------|---------------|------|-------------|
| 1    | **start_time**         | Date-Time     | 0..1 |             |
| 2    | **stop_time**          | Date-Time     | 0..1 |             |
| 3    | **duration**           | Duration      | 0..1 |             |
| 4    | **response_requested** | Response-Type | 0..1 |             |
| 1036 | **th**                 | AP-Args       | 0..1 |             |

**********

**Type: Actuator (Enumerated)**

| ID   | Item   | Description |
|------|--------|-------------|
| 1036 | **th** |             |

**********

Response Results

**Type: Results (Map{1..\*})**

| ID   | Name           | Type            | \#    | Description                                                         |
|------|----------------|-----------------|-------|---------------------------------------------------------------------|
| 1    | **versions**   | Version unique  | 0..10 | List of OpenC2 language versions supported by this Actuator         |
| 2    | **profiles**   | Nsid unique     | 0..\* | List of profiles supported by this Actuator                         |
| 3    | **pairs**      | Pairs           | 0..1  | Targets applicable to each supported Action                         |
| 4    | **rate_limit** | Number{0.0..\*} | 0..1  | Maximum number of requests per minute supported by design or policy |
| 1036 | **th**         | AP-Results      | 0..1  | TH-defined results                                                  |

**********

**Type: Pairs (Enumerated)**

| ID | Item                                          | Description |
|----|-----------------------------------------------|-------------|
| 3  | **query: features, /huntbooks, /datasources** |             |
| 30 | **investigate: /hunt**                        |             |

**********

TH targets defined in this profile.

**Type: AP-Target (Choice)**

| ID | Name            | Type                | \#   | Description                                                                                            |
|----|-----------------|---------------------|------|--------------------------------------------------------------------------------------------------------|
| 1  | **hunt**        | String              | 1    | A procedure to find a set of entities in the monitored environment that associates with a cyberthreat. |
| 2  | **huntbooks**   | Huntbook-Specifiers | 1    | TH Huntbook specifiers.                                                                                |
| 3  | **datasources** | String              | 0..1 |                                                                                                        |

**********

TH command arguments defined in this profile.

**Type: AP-Args (Map)**

| ID | Name         | Type     | \# | Description                                                    |
|----|--------------|----------|----|----------------------------------------------------------------|
| 1  | **huntargs** | Huntargs | 1  | Arguments for use in conjunction with huntbook implementation. |

**********

TH command arguments defined in this profile.

**Type: Huntargs (Record{1..\*})**

| ID | Name             | Type                           | \#   | Description                                                                                       |
|----|------------------|--------------------------------|------|---------------------------------------------------------------------------------------------------|
| 1  | **string_arg**   | String                         | 0..1 | string arguments supplied as huntargs.                                                            |
| 2  | **integer_arg**  | Integer                        | 0..1 | integer arguments supplied as huntargs.                                                           |
| 3  | **stix**         | STIX-Cybersecurity-Observables | 0..1 | STIX arguments supplied as huntargs.                                                              |
| 4  | **timeranges**   | Timeranges                     | 0..1 | Timeranges used in the execution of a hunt.                                                       |
| 5  | **datasources**  | Datasource-Array               | 0..1 | Available data sources for hunting. These may be a host monitor, an EDR, a SIEM, a firewall, etc. |
| 6  | **ipv4_address** | IPv4-Addr                      | 0..1 | IPv4 address as defined in [RFC0791].                                                             |
| 7  | **ipv6_address** | IPv6-Addr                      | 0..1 | IPv6 address as defined in [RFC8200].                                                             |
| 8  | **ipv4_network** | IPv4-Net                       | 0..1 | ipv4 network targeted by hunt activity.                                                           |
| 9  | **ipv6_network** | IPv6-Net                       | 0..1 | ipv6 network targeted by hunt activity.                                                           |

**********

TH Huntbook specifiers.

**Type: Huntbook-Specifiers (Map)**

| ID | Name              | Type                | \#   | Description                                                             |
|----|-------------------|---------------------|------|-------------------------------------------------------------------------|
| 1  | **path**          | String              | 0..1 | Return huntbooks at and below this filesystem location (absolute path). |
| 2  | **tags**          | Tags                | 0..1 | Return huntbooks with these keywords.                                   |
| 3  | **arg_types**     | Specified-Arg-Types | 0..1 | Return huntbooks that take these argument types.                        |
| 4  | **arg_names**     | Specified-Arg-Names | 0..1 | Return huntbooks that take these argument types.                        |
| 5  | **format_types**  | Return-Type         | 0..1 | Return huntbooks that produce these output types.                       |
| 6  | **return_format** | Huntbook-Sections   | 0..1 | For each huntbook returned, include these data items.                   |

**********

| Type Name               | Type Definition   | Description                                      |
|-------------------------|-------------------|--------------------------------------------------|
| **Specified-Arg-Types** | ArrayOf(Arg-Type) | Return huntbooks that take these argument types. |

**********

| Type Name               | Type Definition   | Description                                            |
|-------------------------|-------------------|--------------------------------------------------------|
| **Specified-Arg-Names** | ArrayOf(Arg-Name) | Return huntbooks that take arguments with these names. |

**********

TH results defined in this profile.

**Type: AP-Results (Map{1..\*})**

| ID | Name              | Type                           | \#   | Description                                              |
|----|-------------------|--------------------------------|------|----------------------------------------------------------|
| 1  | **huntbook_info** | ArrayOf(Huntbook-Info)         | 0..1 | Structured data returned by Query: Huntbooks.            |
| 2  | **datasources**   | Datasource-Array               | 0..1 | Datasource names and info returned by Query Datasources. |
| 3  | **stix_returns**  | STIX-Cybersecurity-Observables | 0..1 | STIX SCO object returns                                  |

**********

| Type Name      | Type Definition    | Description                                  |
|----------------|--------------------|----------------------------------------------|
| **Timeranges** | ArrayOf(Timerange) | a timerange used in the execution of a hunt. |

**********

Identification of process to be targeted by Threat Hunting activity.

**Type: Timerange (Choice)**

| ID | Name                   | Type          | \#   | Description                                                             |
|----|------------------------|---------------|------|-------------------------------------------------------------------------|
| 1  | **timerange_absolute** | Timerange-Abs | 0..1 | Absolute timerange, defined by a start and end time in ISO 8601 format. |
| 2  | **timerange_relative** | Timerange-Rel | 0..1 | Relative timerange, example '3, Days' for last 3 days.                  |

**********

Time Unit Keywords.

**Type: Time-Unit (Enumerated)**

| ID | Item        | Description |
|----|-------------|-------------|
| 1  | **Days**    |             |
| 2  | **Hours**   |             |
| 3  | **Minutes** |             |
| 4  | **Seconds** |             |

**********

Absolute timerange, defined by a start and end time in ISO 8601 format.

**Type: Timerange-Abs (Record{2..\*})**

| ID | Name                | Type      | \# | Description                        |
|----|---------------------|-----------|----|------------------------------------|
| 1  | **hunt_start_time** | timestamp | 1  | Start time, as a STIX time string. |
| 2  | **hunt_stop_time**  | timestamp | 1  | Stop time, as a STIX time string.  |

**********

Relative timerange, example '3, Days' for last 3 days.

**Type: Timerange-Rel (Record{2..\*})**

| ID | Name          | Type      | \# | Description                                                |
|----|---------------|-----------|----|------------------------------------------------------------|
| 1  | **number**    | Integer   | 1  | Number of specified Time Units used in Relative Timerange. |
| 2  | **time_unit** | Time-Unit | 1  | Time Unit Keywords.                                        |

**********

| Type Name    | Type Definition | Description                                                                                                                                                                         |
|--------------|-----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Arg-Type** | String          | Argument types used by a Huntbook. Follow STIX naming conventions, with lowercase characters and hyphens replacing spaces. Common types include process, file, and network-traffic. |

**********

| Type Name    | Type Definition | Description                                                                                                                |
|--------------|-----------------|----------------------------------------------------------------------------------------------------------------------------|
| **Arg-Name** | String          | Argument names used by a Huntbook. Follow C variable naming conventions. Examples include name, src_port, and x_unique_id. |

**********

Variable names and types expected as returns when using a Huntbook.

**Type: Return-Type (Record{2..\*})**

| ID | Name         | Type     | \# | Description                                      |
|----|--------------|----------|----|--------------------------------------------------|
| 1  | **var_name** | Arg-Name | 1  | Variable name to be returned by use of Huntbook. |
| 2  | **var_type** | Arg-Type | 1  | Type of data to be returned by use of Huntbook.  |

**********

Datasource names and tags required for use with a particular Huntbook.

**Type: Datasource (Record{1..\*})**

| ID | Name        | Type   | \#   | Description                                                 |
|----|-------------|--------|------|-------------------------------------------------------------|
| 1  | **ds_name** | String | 1    | Name of a Datasource used by a Huntbook in Kestrel runtime. |
| 2  | **ds_tags** | Tags   | 0..1 | Tags applied to a Datasource for search or filter purposes. |

**********

| Type Name             | Type Definition           | Description                                           |
|-----------------------|---------------------------|-------------------------------------------------------|
| **Huntbook-Sections** | ArrayOf(Huntbook-Section) | For each huntbook returned, include these data items. |

**********

Data format to be returned by Query Huntbooks. If none specified, return all.

**Type: Huntbook-Section (Enumerated)**

| ID | Item                 | Description                                                                                           |
|----|----------------------|-------------------------------------------------------------------------------------------------------|
| 1  | **path**             | Specifies the return should include the path to each Huntbook specified by the query conditions.      |
| 2  | **uniqueId**         | Specifies the return should include the ID of each Huntbook specified by the query conditions.        |
| 3  | **version**          | Specifies the return should include the ID of each Huntbook specified by the query conditions.        |
| 4  | **args_required**    | Specifies the returned data should include the required arguments for the available Huntbooks.        |
| 5  | **expected_returns** | Specifies the returned data should include the expected returns for the available Huntbooks.          |
| 6  | **script**           | Specifies the returned data should include the full text of the Huntflow for each available Huntbook. |

**********

Structured data returned by Query: Huntbooks with specifiers for specific info.

**Type: Huntbook-Info (Record{1..\*})**

| ID | Name                 | Type            | \#   | Description                                           |
|----|----------------------|-----------------|------|-------------------------------------------------------|
| 1  | **path**             | String          | 0..1 | Path used to identify a Huntbook in place of a name.  |
| 2  | **uniqueId**         | Integer         | 0..1 | Unique ID associated with a specified Huntbook.       |
| 3  | **version**          | String          | 0..1 | Unique ID associated with a specified Huntbook.       |
| 4  | **args_required**    | Typed-Arguments | 0..1 | List of arguments used in the specified Huntflow.     |
| 5  | **expected_returns** | Typed-Arguments | 0..1 | Data returned by the specified Huntbooks.             |
| 6  | **script**           | String          | 0..1 | Text of Hunt logic implemented by specified Huntbook. |

**********

| Type Name            | Type Definition     | Description                                                  |
|----------------------|---------------------|--------------------------------------------------------------|
| **Datasource-Array** | ArrayOf(Datasource) | An Array of Datasources, with multiple uses in Threathunting |

**********

| Type Name | Type Definition | Description                                 |
|-----------|-----------------|---------------------------------------------|
| **Tags**  | ArrayOf(String) | Tags applied for search or filter purposes. |

**********

| Type Name           | Type Definition           | Description                                           |
|---------------------|---------------------------|-------------------------------------------------------|
| **Typed-Arguments** | MapOf(Arg-Name, Arg-Type) | Argument names and types tied to a specific Huntbook. |

**********

| Type Name                          | Type Definition | Description                                              |
|------------------------------------|-----------------|----------------------------------------------------------|
| **STIX-Cybersecurity-Observables** | ArrayOf(SCO)    | An Array of Cybersecurity Observables in STIX formatting |

**********

Availiable Cybersecurity Observables in the STIX language

**Type: SCO (Choice)**

| ID | Name        | Type    | \# | Description |
|----|-------------|---------|----|-------------|
| 1  | **Process** | process | 1  |             |

**********

The Process Object represents common properties of an instance of a computer program as executed on an operating system.

**Type: process (Record)**

| ID | Name                       | Type                         | \#   | Description                                                                                                                                                                         |
|----|----------------------------|------------------------------|------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1  | **type**                   | String{pattern="^process$"}  | 1    |                                                                                                                                                                                     |
| 2  | **id**                     | String{pattern="^process--"} | 1    |                                                                                                                                                                                     |
| 3  | **extensions**             | ArrayOf(String)              | 0..1 |                                                                                                                                                                                     |
| 4  | **is_hidden**              | Boolean                      | 0..1 |                                                                                                                                                                                     |
| 5  | **pid**                    | Integer                      | 0..1 | Specifies the Process ID, or PID, of the process.                                                                                                                                   |
| 6  | **created_time**           | timestamp                    | 0..1 | Specifies the date/time at which the process was created.                                                                                                                           |
| 7  | **cwd**                    | String                       | 0..1 | Specifies the current working directory of the process.                                                                                                                             |
| 8  | **command_line**           | String                       | 0..1 | Specifies the full command line used in executing the process, including the process name (which may be specified individually via the binary_ref.name property) and any arguments. |
| 9  | **environment_variables**  | ArrayOf(String)              | 0..1 | Specifies the list of environment variables associated with the process as a dictionary.                                                                                            |
| 10 | **opened_connection_refs** | String                       | 0..1 | Specifies the list of network connections opened by the process, as a reference to one or more Network Traffic Objects.                                                             |
| 11 | **creator_user_ref**       | ArrayOf(String){1..\*}       | 0..1 | Specifies the user that created the process, as a reference to a User Account Object.                                                                                               |
| 12 | **image_ref**              | String                       | 0..1 | Specifies the executable binary that was executed as the process image, as a reference to a File Object.                                                                            |
| 13 | **parent_ref**             | String                       | 0..1 | Specifies the other process that spawned (i.e. is the parent of) this one, as represented by a Process Object.                                                                      |
| 14 | **child_refs**             | ArrayOf(String){1..\*}       | 0..1 | Specifies the other processes that were spawned by (i.e. children of) this process, as a reference to one or more other Process Objects.                                            |
| 15 | **spec_version**           | spec_version                 | 0..1 |                                                                                                                                                                                     |
| 16 | **object_marking_refs**    | object_marking_refs          | 0..1 |                                                                                                                                                                                     |
| 17 | **granular_markings**      | granular_markings            | 0..1 |                                                                                                                                                                                     |
| 18 | **defanged**               | defanged                     | 0..1 |                                                                                                                                                                                     |

**********

The version of the STIX specification used to represent the content in this cyber-observable.

**Type: spec_version (Enumerated)**

| ID | Item    | Description |
|----|---------|-------------|
| 1  | **2.0** |             |
| 2  | **2.1** |             |

**********

| Type Name               | Type Definition           | Description                                                          |
|-------------------------|---------------------------|----------------------------------------------------------------------|
| **object_marking_refs** | ArrayOf(identifier){1..*} | The list of marking-definition objects to be applied to this object. |

**********

**Type: granular_marking (Record)**

| ID | Name          | Type       | \# | Description                                                                                            |
|----|---------------|------------|----|--------------------------------------------------------------------------------------------------------|
| 1  | **selectors** | identifier | 1  | A list of selectors for content contained within the STIX object in which this property appears.       |
| 2  | **lang**      | String     | 1  | Identifies the language of the text identified by this marking.                                        |
| 3  | **pattern**   | identifier | 1  | The marking_ref property specifies the ID of the marking-definition object that describes the marking. |

**********

| Type Name             | Type Definition                 | Description                                             |
|-----------------------|---------------------------------|---------------------------------------------------------|
| **granular_markings** | ArrayOf(granular_marking){1..*} | The set of granular markings that apply to this object. |

**********

| Type Name    | Type Definition | Description                                                                    |
|--------------|-----------------|--------------------------------------------------------------------------------|
| **defanged** | Boolean         | Defines whether or not the data contained within the object has been defanged. |

**********

| Type Name      | Type Definition                                                                                                                       | Description                                                                                                                                                                        |
|----------------|---------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **identifier** | String{pattern="^[a-z][a-z0-9-]+[a-z0-9]--[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"} | Represents identifiers across the CTI specifications. The format consists of the name of the top-level object being identified, followed by two dashes (--), followed by a UUIDv4. |

**********

Rules for custom properties

**Type: properties (Array{1..\*})**

| ID | Type                   | \#   | Description                                                                                                                                                                                                                                                                                                                                                          |
|----|------------------------|------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1  | Binary                 | 0..1 | **binary** -                                                                                                                                                                                                                                                                                                                                                         |
| 2  | Hex                    | 0..1 | **hex** - The hex data type encodes an array of octets (8-bit bytes) as hexadecimal. The string MUST consist of an even number of hexadecimal characters, which are the digits '0' through '9' and the letters 'a' through 'f'.  In order to allow pattern matching on custom objects, all properties that use the hex type, the property name MUST end with '_hex'. |
| 3  | ArrayOf(String){1..\*} | 0..1 | **array** -                                                                                                                                                                                                                                                                                                                                                          |
| 4  | String                 | 0..1 | **string** -                                                                                                                                                                                                                                                                                                                                                         |
| 5  | Integer                | 0..1 | **integer** -                                                                                                                                                                                                                                                                                                                                                        |
| 6  | Boolean                | 0..1 | **boolean** -                                                                                                                                                                                                                                                                                                                                                        |
| 7  | Number                 | 0..1 | **number** -                                                                                                                                                                                                                                                                                                                                                         |

**********

| Type Name | Type Definition                       | Description |
|-----------|---------------------------------------|-------------|
| **Hex**   | String{pattern="^([a-fA-F0-9]{2})+$"} |             |

**********

| Type Name     | Type Definition                                                            | Description |
|---------------|----------------------------------------------------------------------------|-------------|
| **timestamp** | String{pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$"} |             |

**********

| Type Name    | Type Definition                | Description                                                                           |
|--------------|--------------------------------|---------------------------------------------------------------------------------------|
| **Features** | ArrayOf(Feature){0..10} unique | An array of zero to ten names used to query a Consume for its supported capabilities. |

**********

IPv4 address and prefix length

**Type: IPv4-Net (Array /ipv4-net)**

| ID | Type      | \#   | Description                                                                          |
|----|-----------|------|--------------------------------------------------------------------------------------|
| 1  | IPv4-Addr | 1    | **ipv4_addr** - IPv4 address as defined in [[RFC0791]](#rfc0791)                     |
| 2  | Integer   | 0..1 | **prefix_length** - CIDR prefix-length. If omitted, refers to a single host address. |

**********

IPv6 address and prefix length

**Type: IPv6-Net (Array /ipv6-net)**

| ID | Type      | \#   | Description                                                                    |
|----|-----------|------|--------------------------------------------------------------------------------|
| 1  | IPv6-Addr | 1    | **ipv6_addr** - IPv6 address as defined in [[RFC8200]](#rfc8200)               |
| 2  | Integer   | 0..1 | **prefix_length** - prefix length. If omitted, refers to a single host address |

**********

| Type Name     | Type Definition | Description   |
|---------------|-----------------|---------------|
| **Date-Time** | Integer{0..*}   | Date and Time |

**********

| Type Name    | Type Definition | Description      |
|--------------|-----------------|------------------|
| **Duration** | Integer{0..*}   | A length of time |

**********

Specifies the results to be returned from a query features Command

**Type: Feature (Enumerated)**

| ID | Item           | Description                                                         |
|----|----------------|---------------------------------------------------------------------|
| 1  | **versions**   | List of OpenC2 Language versions supported by this Consumer         |
| 2  | **profiles**   | List of profiles supported by this Consumer                         |
| 3  | **pairs**      | List of supported Actions and applicable Targets                    |
| 4  | **rate_limit** | Maximum number of Commands per minute supported by design or policy |

**********

| Type Name     | Type Definition   | Description                                             |
|---------------|-------------------|---------------------------------------------------------|
| **IPv4-Addr** | Binary /ipv4-addr | 32 bit IPv4 address as defined in [[RFC0791]](#rfc0791) |

**********

| Type Name     | Type Definition   | Description                                              |
|---------------|-------------------|----------------------------------------------------------|
| **IPv6-Addr** | Binary /ipv6-addr | 128 bit IPv6 address as defined in [[RFC8200]](#rfc8200) |

**********

| Type Name | Type Definition | Description                                    |
|-----------|-----------------|------------------------------------------------|
| **Nsid**  | String{1..16}   | A short identifier that refers to a namespace. |

**********

**Type: Response-Type (Enumerated)**

| ID | Item         | Description                                     |
|----|--------------|-------------------------------------------------|
| 0  | **none**     | No response                                     |
| 1  | **ack**      | Respond when Command received                   |
| 2  | **status**   | Respond with progress toward Command completion |
| 3  | **complete** | Respond when all aspects of Command completed   |

**********

**Type: Status-Code (Enumerated.ID)**

| ID  | Description                                                                                                                                                           |
|-----|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 102 | **Processing** - an interim Response used to inform the Producer that the Consumer has accepted the Command but has not yet completed it                              |
| 200 | **OK** - the Command has succeeded                                                                                                                                    |
| 201 | **Created** - the Command has succeeded and a new resource has been created as a result of it                                                                         |
| 400 | **Bad Request** - the Consumer cannot process the Command due to something that is perceived to be a Producer error (e.g., malformed Command syntax)                  |
| 401 | **Unauthorized** - the Command Message lacks valid authentication credentials for the target resource or authorization has been refused for the submitted credentials |
| 403 | **Forbidden** - the Consumer understood the Command but refuses to authorize it                                                                                       |
| 404 | **Not Found** - the Consumer has not found anything matching the Command                                                                                              |
| 500 | **Internal Error** - the Consumer encountered an unexpected condition that prevented it from performing the Command                                                   |
| 501 | **Not Implemented** - the Consumer does not support the functionality required to perform the Command                                                                 |
| 503 | **Service Unavailable** - the Consumer is currently unable to perform the Command due to a temporary overloading or maintenance of the Consumer                       |

**********

| Type Name      | Type Definition              | Description        |
|----------------|------------------------------|--------------------|
| **Command-ID** | String{pattern="^\S{0,36}$"} | Command Identifier |

**********

| Type Name   | Type Definition                                 | Description                      |
|-------------|-------------------------------------------------|----------------------------------|
| **Version** | String{pattern="^(\d{1,4})(\.(\d{1,6})){0,2}$"} | Major.Minor.Patch version number |

**********
