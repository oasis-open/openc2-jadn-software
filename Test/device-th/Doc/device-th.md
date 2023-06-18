         title: "Threat Hunting Device"
       package: "https://oca.org/casp/device/threat-hunter-2000"
       version: "0-wd01"
   description: "Data definitions for Threat Hunting (TH) functions"
       exports: ["OpenC2-Command", "OpenC2-Response"]

The Command defines an Action to be performed on a Target

**Type: OpenC2-Command (Record)**

| ID | Name           | Type       | \#   | Description                                                                |
|----|----------------|------------|------|----------------------------------------------------------------------------|
| 1  | **action**     | Action     | 1    | The task or activity to be performed (i.e., the 'verb').                   |
| 2  | **target**     | Target     | 1    | The object of the Action. The Action is performed on the Target.           |
| 3  | **args**       | Args       | 0..1 | Additional information that applies to the Command.                        |
| 4  | **profile**    | Profile    | 0..1 | The actuator profile defining the function to be performed by the Command. |
| 5  | **command_id** | Command-ID | 0..1 | An identifier of this Command.                                             |

**********

**Type: OpenC2-Response (Map{1..\*})**

| ID | Name            | Type        | \#   | Description                                                                           |
|----|-----------------|-------------|------|---------------------------------------------------------------------------------------|
| 1  | **status**      | Status-Code | 1    | An integer status code                                                                |
| 2  | **status_text** | String      | 0..1 | A free-form human-readable description of the Response status                         |
| 3  | **results**     | Results     | 0..1 | Map of key:value pairs that contain additional results based on the invoking Command. |

**********

Actions available to this Profile

**Type: Action (Enumerated)**

| ID | Item            | Description                         |
|----|-----------------|-------------------------------------|
| 3  | **query**       | Initiate a request for information. |
| 30 | **investigate** |                                     |

**********

**Type: Target (Choice)**

| ID   | Name         | Type      | \# | Description                                                                        |
|------|--------------|-----------|----|------------------------------------------------------------------------------------|
| 9    | **features** | Features  | 1  | A set of items used with the query Action to determine an Actuator's capabilities. |
| 1036 | **th/**      | Target$th | 1  | Threat Hunting Profile-defined targets                                             |

**********

**Type: Args (Map{1..\*})**

| ID   | Name                   | Type          | \#   | Description |
|------|------------------------|---------------|------|-------------|
| 1    | **start_time**         | Date-Time     | 0..1 |             |
| 2    | **stop_time**          | Date-Time     | 0..1 |             |
| 3    | **duration**           | Duration      | 0..1 |             |
| 4    | **response_requested** | Response-Type | 0..1 |             |
| 1036 | **th/**                | Args$th       | 0..1 |             |

**********

**Type: Profile (Enumerated)**

| ID   | Item   | Description |
|------|--------|-------------|
| 1036 | **th** |             |

**********

Response Results

**Type: Results (Map{1..\*})**

| ID   | Name           | Type            | \#    | Description                                                         |
|------|----------------|-----------------|-------|---------------------------------------------------------------------|
| 1    | **versions**   | SemVer unique   | 0..10 | List of OpenC2 language versions supported by this Actuator         |
| 2    | **profiles**   | Profile unique  | 0..\* | List of profiles supported by this Actuator                         |
| 3    | **pairs**      | Pairs           | 0..1  | Targets applicable to each supported Action                         |
| 4    | **rate_limit** | Number{0.0..\*} | 0..1  | Maximum number of requests per minute supported by design or policy |
| 1036 | **th/**        | Results$th      | 0..1  | TH-defined results                                                  |

**********

Targets applicable to each action supported by this device

**Type: Pairs (Map{1..\*})**

| ID   | Name      | Type                         | \#   | Description                                                     |
|------|-----------|------------------------------|------|-----------------------------------------------------------------|
| 3    | **query** | ArrayOf(QueryTargets) unique | 1    |                                                                 |
| 1036 | **th/**   | Pairs$th                     | 0..1 | Targets of each Action for Software Bill Of Materials retrieval |

**********

**Type: QueryTargets (Enumerated)**

| ID | Item         | Description |
|----|--------------|-------------|
| 9  | **features** |             |

**********

TH targets defined in this profile.

**Type: Target$th (Choice)**

| ID | Name            | Type                   | \#   | Description                                                                                            |
|----|-----------------|------------------------|------|--------------------------------------------------------------------------------------------------------|
| 1  | **hunt**        | String                 | 1    | A procedure to find a set of entities in the monitored environment that associates with a cyberthreat. |
| 2  | **huntbooks**   | Huntbook-Specifiers$th | 1    | TH Huntbook specifiers.                                                                                |
| 3  | **datasources** | String                 | 0..1 |                                                                                                        |

**********

TH command arguments defined in this profile.

**Type: Args$th (Map)**

| ID | Name         | Type        | \# | Description                                                    |
|----|--------------|-------------|----|----------------------------------------------------------------|
| 1  | **huntargs** | Huntargs$th | 1  | Arguments for use in conjunction with huntbook implementation. |

**********

TH results defined in this profile.

**Type: Results$th (Map{1..\*})**

| ID | Name              | Type                     | \#   | Description                                              |
|----|-------------------|--------------------------|------|----------------------------------------------------------|
| 1  | **huntbook_info** | Huntbook-Info$th         | 0..1 | Structured data returned by Query: Huntbooks.            |
| 2  | **datasources**   | Datasource-Array$th      | 0..1 | Datasource names and info returned by Query Datasources. |
| 3  | **investigation** | Investigation-results$th | 1    |                                                          |

**********

**Type: Pairs$th (Map)**

| ID | Name            | Type                                   | \# | Description |
|----|-----------------|----------------------------------------|----|-------------|
| 3  | **query**       | ArrayOf(Query-Targets$th) unique       | 1  |             |
| 30 | **investigate** | ArrayOf(Investigate-Targets$th) unique | 1  |             |

**********

**Type: Query-Targets$th (Enumerated)**

| ID | Item            | Description |
|----|-----------------|-------------|
| 1  | **huntbooks**   |             |
| 2  | **datasources** |             |

**********

**Type: Investigate-Targets$th (Enumerated)**

| ID | Item     | Description |
|----|----------|-------------|
| 1  | **hunt** |             |

**********

TH Huntbook specifiers.

**Type: Huntbook-Specifiers$th (Map)**

| ID | Name              | Type                   | \#   | Description                                                             |
|----|-------------------|------------------------|------|-------------------------------------------------------------------------|
| 1  | **path**          | String                 | 0..1 | Return huntbooks at and below this filesystem location (absolute path). |
| 2  | **tags**          | Tags$th                | 0..1 | Return huntbooks with these keywords.                                   |
| 3  | **arg_types**     | Specified-Arg-Types$th | 0..1 | Return huntbooks that take these argument types.                        |
| 4  | **arg_names**     | Specified-Arg-Names$th | 0..1 | Return huntbooks that take these argument types.                        |
| 5  | **format_types**  | Return-Type$th         | 0..1 | Return huntbooks that produce these output types.                       |
| 6  | **return_format** | Huntbook-Sections$th   | 0..1 | For each huntbook returned, include these data items.                   |

**********

| Type Name                  | Type Definition      | Description                                      |
|----------------------------|----------------------|--------------------------------------------------|
| **Specified-Arg-Types$th** | ArrayOf(Arg-Type$th) | Return huntbooks that take these argument types. |

**********

| Type Name                  | Type Definition      | Description                                            |
|----------------------------|----------------------|--------------------------------------------------------|
| **Specified-Arg-Names$th** | ArrayOf(Arg-Name$th) | Return huntbooks that take arguments with these names. |

**********

TH command arguments defined in this profile.

**Type: Huntargs$th (Record{1..\*})**

| ID | Name            | Type                | \#   | Description                                                                                                                     |
|----|-----------------|---------------------|------|---------------------------------------------------------------------------------------------------------------------------------|
| 1  | **string_arg**  | String              | 0..1 | string arguments supplied as huntargs.                                                                                          |
| 2  | **integer_arg** | Integer             | 0..1 | integer arguments supplied as huntargs.                                                                                         |
| 3  | **stix/**       | STIX-Array$th       | 0..1 | STIX arguments supplied as huntargs.                                                                                            |
| 4  | **timeranges**  | Timeranges$th       | 0..1 | Timeranges used in the execution of a hunt.                                                                                     |
| 5  | **datasources** | Datasource-Array$th | 0..1 | You must identify one or more available data sources for hunting. These may be a host monitor, an EDR, a SIEM, a firewall, etc. |
| 6  | **ipv4_addr**   | IPv4-Addr           | 0..1 | **ipv4_address** - IPv4 address as defined in [RFC0791]                                                                         |
| 7  | **ipv6_addr**   | IPv6-Addr           | 0..1 | **ipv6_address** - IPv6 address as defined in [RFC8200]                                                                         |
| 8  | **ipv4_net**    | IPv4-Net            | 0..1 | **ipv4_network** - ipv4 network targeted by hunt activity                                                                       |
| 9  | **ipv6_net**    | IPv6-Net            | 0..1 | **ipv6_network** - ipv6 network targeted by hunt activity                                                                       |

**********

**Type: Investigation-results$th (Record)**

| ID | Name        | Type    | \# | Description |
|----|-------------|---------|----|-------------|
| 1  | **names**   | String  | 1  | + ???       |
| 2  | **content** | Integer | 1  | tables      |

**********

| Type Name         | Type Definition       | Description                                  |
|-------------------|-----------------------|----------------------------------------------|
| **Timeranges$th** | ArrayOf(Timerange$th) | a timerange used in the execution of a hunt. |

**********

Identification of process to be targeted by Threat Hunting activity.

**Type: Timerange$th (Choice)**

| ID | Name                   | Type             | \#   | Description                                                             |
|----|------------------------|------------------|------|-------------------------------------------------------------------------|
| 1  | **timerange_absolute** | Timerange-Abs$th | 0..1 | Absolute timerange, defined by a start and end time in ISO 8601 format. |
| 2  | **timerange_relative** | Timerange-Rel$th | 0..1 | Relative timerange, example '3, Days' for last 3 days.                  |

**********

Time Unit Keywords.

**Type: Time-Unit$th (Enumerated)**

| ID | Item        | Description |
|----|-------------|-------------|
| 1  | **Days**    |             |
| 2  | **Hours**   |             |
| 3  | **Minutes** |             |
| 4  | **Seconds** |             |

**********

Absolute timerange, defined by a start and end time in ISO 8601 format.

**Type: Timerange-Abs$th (Record{2..\*})**

| ID | Name                | Type         | \# | Description                        |
|----|---------------------|--------------|----|------------------------------------|
| 1  | **hunt_start_time** | STIX-Time$th | 1  | Start time, as a STIX time string. |
| 2  | **hunt_stop_time**  | STIX-Time$th | 1  | Stop time, as a STIX time string.  |

**********

| Type Name        | Type Definition                                                            | Description                             |
|------------------|----------------------------------------------------------------------------|-----------------------------------------|
| **STIX-Time$th** | String{pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$"} | string representation of ISO 8601 time. |

**********

Relative timerange, example '3, Days' for last 3 days.

**Type: Timerange-Rel$th (Record{2..\*})**

| ID | Name          | Type         | \# | Description                                                |
|----|---------------|--------------|----|------------------------------------------------------------|
| 1  | **number**    | Integer      | 1  | Number of specified Time Units used in Relative Timerange. |
| 2  | **time_unit** | Time-Unit$th | 1  | Time Unit Keywords.                                        |

**********

| Type Name       | Type Definition | Description                                                                                                                                                                         |
|-----------------|-----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Arg-Type$th** | String          | Argument types used by a Huntbook. Follow STIX naming conventions, with lowercase characters and hyphens replacing spaces. Common types include process, file, and network-traffic. |

**********

| Type Name       | Type Definition | Description                                                                                                                |
|-----------------|-----------------|----------------------------------------------------------------------------------------------------------------------------|
| **Arg-Name$th** | String          | Argument names used by a Huntbook. Follow C variable naming conventions. Examples include name, src_port, and x_unique_id. |

**********

Variable names and types expected as returns when using a Huntbook.

**Type: Return-Type$th (Record{2..\*})**

| ID | Name         | Type        | \# | Description                                      |
|----|--------------|-------------|----|--------------------------------------------------|
| 1  | **var_name** | Arg-Name$th | 1  | Variable name to be returned by use of Huntbook. |
| 2  | **var_type** | Arg-Type$th | 1  | Type of data to be returned by use of Huntbook.  |

**********

Datasource names and tags required for use with a particular Huntbook.

**Type: Datasource$th (Record{1..\*})**

| ID | Name        | Type    | \#   | Description                                                 |
|----|-------------|---------|------|-------------------------------------------------------------|
| 1  | **ds_name** | String  | 1    | Name of a Datasource used by a Huntbook in Kestrel runtime. |
| 2  | **ds_tags** | Tags$th | 0..1 | Tags applied to a Datasource for search or filter purposes. |

**********

| Type Name                | Type Definition              | Description                                           |
|--------------------------|------------------------------|-------------------------------------------------------|
| **Huntbook-Sections$th** | ArrayOf(Huntbook-Section$th) | For each huntbook returned, include these data items. |

**********

Data format to be returned by Query Huntbooks. If none specified, return all.

**Type: Huntbook-Section$th (Enumerated)**

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

**Type: Huntbook-Info$th (Record{1..\*})**

| ID | Name                 | Type               | \#   | Description                                          |
|----|----------------------|--------------------|------|------------------------------------------------------|
| 1  | **path**             | String             | 0..1 | Path used to identify a Huntbook in place of a name. |
| 2  | **uniqueId**         | Integer            | 0..1 | Unique ID associated with a specified Huntbook.      |
| 3  | **version**          | String             | 0..1 | Unique ID associated with a specified Huntbook.      |
| 4  | **args_required**    | Typed-Arguments$th | 0..1 | List of arguments used in the specified Huntflow.    |
| 5  | **expected_returns** | Typed-Arguments$th | 0..1 | Data returned by the specified Huntbooks.            |
| 6  | **script**           | String             | 0..1 | Text of Hunt logic imlemented by specified Huntbook. |

**********

| Type Name         | Type Definition         | Description                          |
|-------------------|-------------------------|--------------------------------------|
| **STIX-Array$th** | ArrayOf(STIX-Object$th) | STIX arguments supplied as huntargs. |

**********

| Type Name          | Type Definition | Description                                                             |
|--------------------|-----------------|-------------------------------------------------------------------------|
| **STIX-Object$th** | ArrayOf(String) | STIX cyber observables used in threat hunting. link to STIX table HERE. |

**********

| Type Name               | Type Definition        | Description                                                  |
|-------------------------|------------------------|--------------------------------------------------------------|
| **Datasource-Array$th** | ArrayOf(Datasource$th) | An Array of Datasources, with multiple uses in Threathunting |

**********

| Type Name   | Type Definition | Description                                 |
|-------------|-----------------|---------------------------------------------|
| **Tags$th** | ArrayOf(String) | Tags applied for search or filter purposes. |

**********

| Type Name              | Type Definition                 | Description                                           |
|------------------------|---------------------------------|-------------------------------------------------------|
| **Typed-Arguments$th** | MapOf(Arg-Name$th, Arg-Type$th) | Argument names and types tied to a specific Huntbook. |

**********

| Type Name    | Type Definition         | Description                                                                |
|--------------|-------------------------|----------------------------------------------------------------------------|
| **Features** | ArrayOf(Feature) unique | An array of names used to query a Consumer for its supported capabilities. |

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

| Type Name  | Type Definition                                 | Description                      |
|------------|-------------------------------------------------|----------------------------------|
| **SemVer** | String{pattern="^(\d{1,4})(\.(\d{1,6})){0,2}$"} | Major.Minor.Patch version number |

**********
