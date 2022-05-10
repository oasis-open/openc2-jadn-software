         title: "OpenC2 device schema for the PACMaster PACE collection service"
       package: "http://acme.com/schemas/device/pac/v1.0"
       exports: ["OpenC2-Command", "OpenC2-Response"]

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

**Type: Action (Enumerated)**

| ID | Item      | Description                         |
|----|-----------|-------------------------------------|
| 3  | **query** | Initiate a request for information. |

**********

**Type: Target (Choice)**

| ID   | Name         | Type          | \# | Description                                                                        |
|------|--------------|---------------|----|------------------------------------------------------------------------------------|
| 9    | **features** | Features      | 1  | A set of items used with the query Action to determine an Actuator's capabilities. |
| 1035 | **pac/**     | AP-Target$pac | 1  | PAC-defined targets                                                                |

**********

**Type: Args (Map{1..\*})**

| ID   | Name                   | Type          | \#   | Description                                                                |
|------|------------------------|---------------|------|----------------------------------------------------------------------------|
| 1    | **start_time**         | Date-Time     | 0..1 | The specific date/time to initiate the Command                             |
| 2    | **stop_time**          | Date-Time     | 0..1 | The specific date/time to terminate the Command                            |
| 3    | **duration**           | Duration      | 0..1 | The length of time for an Command to be in effect                          |
| 4    | **response_requested** | Response-Type | 0..1 | The type of Response required for the Command: none, ack, status, complete |
| 1035 | **pac/**               | AP-Args$pac   | 0..1 | PAC-defined command arguments                                              |

**********

**Type: Actuator (Choice)**

| ID   | Name     | Type              | \# | Description                     |
|------|----------|-------------------|----|---------------------------------|
| 1035 | **pac/** | AP-Specifiers$pac | 1  | PAC-defined actuator specifiers |

**********

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
| 1    | **versions**   | Version unique  | 0..10 | List of OpenC2 language versions supported by this Actuator         |
| 2    | **profiles**   | Nsid unique     | 0..\* | List of profiles supported by this Actuator                         |
| 3    | **pairs**      | Action-Targets  | 0..1  | DEPRECATED: targets applicable to each supported Action             |
| 4    | **rate_limit** | Number{0.0..\*} | 0..1  | Maximum number of requests per minute supported by design or policy |
| 1035 | **pac/**       | AP-Results$pac  | 0..1  | PAC-defined results                                                 |

**********

| Type Name          | Type Definition              | Description                                                |
|--------------------|------------------------------|------------------------------------------------------------|
| **Action-Targets** | MapOf(Action, Targets){1..*} | Targets applicable to each action supported by this device |

**********

| Type Name   | Type Definition                       | Description     |
|-------------|---------------------------------------|-----------------|
| **Targets** | ArrayOf(Pointer[Target]){1..*} unique | Target pointers |

**********

| Type Name    | Type Definition                | Description                                                                           |
|--------------|--------------------------------|---------------------------------------------------------------------------------------|
| **Features** | ArrayOf(Feature){0..10} unique | An array of zero to ten names used to query a Consume for its supported capabilities. |

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

| Type Name   | Type Definition | Description                |
|-------------|-----------------|----------------------------|
| **Version** | String          | Major.Minor version number |

**********

| Type Name         | Type Definition                          | Description             |
|-------------------|------------------------------------------|-------------------------|
| **AP-Target$pac** | ArrayOf(PostureAttributeName$pac) unique | Profile-defined targets |

**********

Profile-defined command arguments

**Type: AP-Args$pac (Map{1..\*})**

| ID | Name    | Type   | \#   | Description              |
|----|---------|--------|------|--------------------------|
| 1  | **foo** | String | 0..1 | Delete from Args if none |

**********

Profile-defined actuator specifiers

**Type: AP-Specifiers$pac (Map)**

| ID | Name    | Type   | \#   | Description                  |
|----|---------|--------|------|------------------------------|
| 1  | **foo** | String | 0..1 | Delete from Actuator if none |

**********

Profile-defined response results

**Type: AP-Results$pac (Map{1..\*})**

| ID | Name           | Type           | \#   | Description |
|----|----------------|----------------|------|-------------|
| 1  | **os_version** | OS-Version$pac | 0..1 |             |
| 2  | **sbom**       | SBOM$pac       | 0..1 |             |

**********

**Type: PostureAttributeName$pac (Enumerated)**

| ID | Item           | Description               |
|----|----------------|---------------------------|
| 1  | **os_version** | Return OS-Version results |
| 2  | **sbom**       | Return SBOM               |

**********

**Type: OS-Version$pac (Record)**

| ID | Name              | Type         | \#    | Description                          |
|----|-------------------|--------------|-------|--------------------------------------|
| 1  | **name**          | String       | 1     | Distribution or product name         |
| 2  | **version**       | String       | 1     | Suitable for presentation OS version |
| 3  | **major**         | Integer      | 0..1  | Major release version                |
| 4  | **minor**         | Integer      | 0..1  |                                      |
| 5  | **patch**         | Integer      | 0..1  | Patch release                        |
| 6  | **build**         | String       | 0..1  | Build-specific or variant string     |
| 7  | **platform**      | String       | 0..1  | OS Platform or ID                    |
| 8  | **platform_like** | String       | 0..\* | Closely-related platforms            |
| 9  | **codename**      | String       | 0..1  | OS Release codename                  |
| 10 | **arch**          | OS-Arch$pac  | 0..1  | OS Architecture                      |
| 11 | **install_date**  | DateTime$pac | 0..1  | Install date of the OS               |

**********

Win: wmic os get osarchitecture, or Unix: uname -m

**Type: OS-Arch$pac (Enumerated)**

| ID | Item       | Description |
|----|------------|-------------|
| 1  | **32-bit** |             |
| 2  | **64-bit** |             |
| 3  | **x86_32** |             |
| 4  | **x86_64** |             |

**********

**Type: SBOM$pac (Choice)**

| ID | Name        | Type              | \# | Description                              |
|----|-------------|-------------------|----|------------------------------------------|
| 1  | **uri**     | URI               | 1  | Unique identifier or locator of the SBOM |
| 2  | **summary** | SBOM-Elements$pac | 1  | NTIA Minimumum Elements of an SBOM       |
| 3  | **content** | SBOM-Content$pac  | 1  | SBOM structured data                     |
| 4  | **blob**    | SBOM-Blob$pac     | 1  | Uninterpreted SBOM bytes                 |

**********

**Type: SBOM-Elements$pac (Record)**

| ID | Name              | Type         | \#    | Description                                                                          |
|----|-------------------|--------------|-------|--------------------------------------------------------------------------------------|
| 1  | **supplier**      | String       | 1..\* | Name of entity that creates, defines, and identifies components                      |
| 2  | **component**     | String       | 1..\* | Designation(s) assigned to a unit of software defined by the original supplier       |
| 3  | **version**       | String       | 1     | Identifier used by supplier to specify a change from a previously identified version |
| 4  | **component_ids** | String       | 0..\* | Other identifiers used to identify a component, or serve as a look-yp key            |
| 5  | **dependencies**  | String       | 0..\* | Upstream component(s)                                                                |
| 6  | **author**        | String       | 1     | Name of the entity that creates SBOM data for this component                         |
| 7  | **timestamp**     | DateTime$pac | 1     | Record of the date and time of the SBOM data assembly                                |

**********

**Type: SBOM-Content$pac (Choice)**

| ID | Name          | Type   | \# | Description                          |
|----|---------------|--------|----|--------------------------------------|
| 1  | **cyclonedx** | String | 1  | Placeholder for CycloneDX data model |
| 2  | **spdx2**     | String | 1  | Placeholder for SPDX v2.x data model |
| 3  | **spdx3**     | String | 1  | Placeholder for SPDX v3 data model   |

**********

**Type: SBOM-Blob$pac (Record)**

| ID | Name       | Type                               | \# | Description |
|----|------------|------------------------------------|----|-------------|
| 1  | **format** | Enumerated(Enum[SBOM-Content$pac]) | 1  |             |
| 2  | **data**   | Binary                             | 1  |             |

**********

| Type Name        | Type Definition                                                                                  | Description     |
|------------------|--------------------------------------------------------------------------------------------------|-----------------|
| **DateTime$pac** | String{pattern="^((?:(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2}(?:\.\d+)?))(Z|[\+-]\d{2}:\d{2})?)$"} | RFC-3339 format |

**********
