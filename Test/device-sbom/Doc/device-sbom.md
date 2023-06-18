         title: "Device schema that supports only SBOM retrieval"
       package: "http://acme.com/device/sbomdevice/v1"
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

**Type: Action (Enumerated)**

| ID | Item      | Description                         |
|----|-----------|-------------------------------------|
| 3  | **query** | Initiate a request for information. |

**********

**Type: Target (Choice)**

| ID   | Name         | Type        | \# | Description                                                                        |
|------|--------------|-------------|----|------------------------------------------------------------------------------------|
| 9    | **features** | Features    | 1  | A set of items used with the query Action to determine an Actuator's capabilities. |
| 1026 | **sbom/**    | Target$sbom | 1  | Targets defined in the Software Bill Of Materials AP                               |

**********

Table 3.3.1.4 lists the properties (ID/Name) and NSIDs assigned to specific Actuator Profiles. The OpenC2 Namespace Registry is the most current list of active and proposed Actuator Profiles.

**Type: Profile (Enumerated)**

| ID   | Item     | Description |
|------|----------|-------------|
| 1026 | **sbom** |             |

**********

**Type: Args (Map{1..\*})**

| ID   | Name                   | Type          | \#   | Description                                                                        |
|------|------------------------|---------------|------|------------------------------------------------------------------------------------|
| 1    | **start_time**         | Date-Time     | 0..1 | The specific date/time to initiate the Command                                     |
| 2    | **stop_time**          | Date-Time     | 0..1 | The specific date/time to terminate the Command                                    |
| 3    | **duration**           | Duration      | 0..1 | The length of time for an Command to be in effect                                  |
| 4    | **response_requested** | Response-Type | 0..1 | The type of Response required for the Command: `none`, `ack`, `status`, `complete` |
| 1026 | **sbom/**              | Args$sbom     | 0..1 | Command arguments for the SBOM actuator profile                                    |

**********

OpenC2-Response defines the structure of a response to OpenC2-Command.

**Type: OpenC2-Response (Record)**

| ID | Name            | Type        | \#   | Description                                                                           |
|----|-----------------|-------------|------|---------------------------------------------------------------------------------------|
| 1  | **status**      | Status-Code | 1    | An integer status code.                                                               |
| 2  | **status_text** | String      | 0..1 | A free-form human-readable description of the Response status.                        |
| 3  | **results**     | Results     | 0..1 | Map of key:value pairs that contain additional results based on the invoking Command. |

**********

Response Results

**Type: Results (Map{1..\*})**

| ID   | Name           | Type            | \#    | Description                                                         |
|------|----------------|-----------------|-------|---------------------------------------------------------------------|
| 1    | **versions**   | SemVer unique   | 0..\* | List of OpenC2 language versions supported by this Consumer         |
| 2    | **profiles**   | Profile unique  | 0..\* | List of profiles supported by this Consumer                         |
| 3    | **pairs**      | Pairs           | 0..1  | List of targets applicable to each supported Action                 |
| 4    | **rate_limit** | Number{0.0..\*} | 0..1  | Maximum number of requests per minute supported by design or policy |
| 1026 | **sbom/**      | Results$sbom    | 0..1  | Results defined in the Sofware Bill Of Materials AP                 |

**********

Targets applicable to each action supported by this device

**Type: Pairs (Map{1..\*})**

| ID   | Name      | Type                         | \#   | Description                                                     |
|------|-----------|------------------------------|------|-----------------------------------------------------------------|
| 3    | **query** | ArrayOf(QueryTargets) unique | 1    |                                                                 |
| 1026 | **sbom/** | Pairs$sbom                   | 0..1 | Targets of each Action for Software Bill Of Materials retrieval |

**********

**Type: QueryTargets (Enumerated)**

| ID | Item         | Description |
|----|--------------|-------------|
| 9  | **features** |             |

**********

Profile-defined targets

**Type: Target$sbom (Choice)**

| ID | Name          | Type                 | \# | Description                                  |
|----|---------------|----------------------|----|----------------------------------------------|
| 1  | **sbom**      | SBOM-Specifiers$sbom | 1  | Return URI IDs for all or specified SBOMs    |
| 2  | **sbom_list** | SBOM-List$sbom       | 1  | Return requested SBOM info for specified IDs |

**********

| Type Name     | Type Definition | Description                       |
|---------------|-----------------|-----------------------------------|
| **Args$sbom** | Map             | Profile-defined command arguments |

**********

Profile-defined response results

**Type: Results$sbom (Map{1..\*})**

| ID | Name          | Type           | \#    | Description                              |
|----|---------------|----------------|-------|------------------------------------------|
| 1  | **sbom**      | ArrayOf(URI)   | 0..1  | IDs of all SBOMs matching query criteria |
| 2  | **sbom_list** | SBOM-Info$sbom | 0..\* | SBOM Info for each ID in sbom_list       |

**********

**Type: Pairs$sbom (Map)**

| ID | Name      | Type                               | \# | Description |
|----|-----------|------------------------------------|----|-------------|
| 3  | **query** | ArrayOf(Query-Targets$sbom) unique | 1  |             |

**********

**Type: Query-Targets$sbom (Enumerated)**

| ID | Item          | Description |
|----|---------------|-------------|
| 1  | **sbom**      |             |
| 2  | **sbom_list** |             |

**********

If none specified, return IDs for all SBOMs

**Type: SBOM-Specifiers$sbom (Map)**

| ID | Name       | Type                                    | \#   | Description                 |
|----|------------|-----------------------------------------|------|-----------------------------|
| 1  | **type**   | ArrayOf(Enum[SBOM-Content$sbom]) unique | 0..1 | SBOM type                   |
| 2  | **format** | ArrayOf(DataFormat$sbom) unique         | 0..1 | Data format                 |
| 3  | **info**   | ArrayOf(Info$sbom){1..\*} unique        | 0..1 | Type of SBOM info to return |

**********

**Type: SBOM-List$sbom (Map)**

| ID | Name     | Type                             | \#    | Description                 |
|----|----------|----------------------------------|-------|-----------------------------|
| 1  | **sids** | URI                              | 1..\* | SBOM IDs to return          |
| 2  | **info** | ArrayOf(Info$sbom){1..\*} unique | 1     | Type of SBOM info to return |

**********

SBOM-Info fields to return

**Type: Info$sbom (Enumerated)**

| ID | Item        | Description                        |
|----|-------------|------------------------------------|
| 1  | **summary** | NTIA Minimumum Elements of an SBOM |
| 2  | **content** | SBOM structured data               |
| 3  | **blob**    | Uninterpreted SBOM bytes           |

**********

**Type: SBOM-Info$sbom (Map)**

| ID | Name        | Type                                | \#   | Description                              |
|----|-------------|-------------------------------------|------|------------------------------------------|
| 1  | **type**    | Enumerated(Enum[SBOM-Content$sbom]) | 1    | SBOM type (name of standard)             |
| 2  | **format**  | DataFormat$sbom                     | 1    | Data (serialization) format              |
| 3  | **sid**     | URI                                 | 1    | Unique identifier or locator of the SBOM |
| 4  | **summary** | SBOM-Elements$sbom                  | 0..1 | NTIA Minimumum Elements of an SBOM       |
| 5  | **content** | SBOM-Content$sbom                   | 0..1 | SBOM structured data                     |
| 6  | **blob**    | Binary                              | 0..1 | Uninterpreted SBOM bytes                 |

**********

**Type: SBOM-Elements$sbom (Record)**

| ID | Name              | Type          | \#    | Description                                                                          |
|----|-------------------|---------------|-------|--------------------------------------------------------------------------------------|
| 1  | **supplier**      | String        | 1..\* | Name of entity that creates, defines, and identifies components                      |
| 2  | **component**     | String        | 1..\* | Designation(s) assigned to a unit of software defined by the original supplier       |
| 3  | **version**       | String        | 1     | Identifier used by supplier to specify a change from a previously identified version |
| 4  | **component_ids** | String        | 1..\* | Other identifiers used to identify a component, or serve as a look-yp key            |
| 5  | **dependencies**  | String        | 1..\* | Upstream component(s)                                                                |
| 6  | **author**        | String        | 1     | Name of the entity that creates SBOM data for this component                         |
| 7  | **timestamp**     | DateTime$sbom | 1     | Record of the date and time of the SBOM data assembly                                |

**********

**Type: SBOM-Content$sbom (Choice)**

| ID | Name          | Type   | \# | Description                          |
|----|---------------|--------|----|--------------------------------------|
| 1  | **cyclonedx** | String | 1  | Placeholder for CycloneDX data model |
| 2  | **spdx2**     | String | 1  | Placeholder for SPDX v2.x data model |
| 3  | **spdx3**     | String | 1  | Placeholder for SPDX v3 data model   |

**********

Serialization Data Formats

**Type: DataFormat$sbom (Enumerated)**

| ID | Item         | Description                        |
|----|--------------|------------------------------------|
| 1  | **ttv**      | Text Tag-Value                     |
| 2  | **json**     | JSON verbose                       |
| 3  | **json-m**   | JSON concise/minimized             |
| 4  | **json-ld**  | JSON linked data                   |
| 5  | **cbor**     | CBOR binary                        |
| 6  | **protobuf** | Protocol Buffers binary            |
| 7  | **xml**      | XML                                |
| 8  | **ss-csv**   | Spreadsheet comma separated values |

**********

| Type Name         | Type Definition | Description |
|-------------------|-----------------|-------------|
| **DateTime$sbom** | Integer{0..*}   |             |

**********

| Type Name    | Type Definition         | Description                                                                |
|--------------|-------------------------|----------------------------------------------------------------------------|
| **Features** | ArrayOf(Feature) unique | An array of names used to query a Consumer for its supported capabilities. |

**********

| Type Name | Type Definition | Description                                         |
|-----------|-----------------|-----------------------------------------------------|
| **URI**   | String /uri     | Uniform Resource Identifier, [[RFC3986]](#rfc3986). |

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
