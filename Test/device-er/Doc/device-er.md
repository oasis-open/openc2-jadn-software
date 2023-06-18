         title: "OpenC2 device schema for the Endpoint Response service"
       package: "http://acme.com/schemas/device/er/v2.0"
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

| ID | Item        | Description                                                                                                                               |
|----|-------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| 3  | **query**   | Query the ER actuator for a list of available features.                                                                                   |
| 6  | **deny**    | Deny a process or service from being executed on the endpoint.                                                                            |
| 7  | **contain** | Isolate a device from communicating with other devices on a network, quarantine a file.                                                   |
| 8  | **allow**   | Un-isolate a previously isolated device.                                                                                                  |
| 9  | **start**   | Initiate a process, application, system, or activity.                                                                                     |
| 10 | **stop**    | Halt a system or end an activity.                                                                                                         |
| 11 | **restart** | Restart a device, system, or process.                                                                                                     |
| 15 | **set**     | Change a value, configuration, or state of a managed entity (e.g., registry value, account).                                              |
| 16 | **update**  | Instructs the Actuator to retrieve, install, process, and operate in accordance with a software update, reconfiguration, or other update. |
| 19 | **create**  | Add a new entity of a known type (e.g.,  registry entry, file).                                                                           |
| 20 | **delete**  | Remove an entity (e.g., registry entry, file).                                                                                            |

**********

**Type: Target (Choice)**

| ID   | Name         | Type      | \# | Description                                                                                                                                                                                  |
|------|--------------|-----------|----|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 3    | **device**   | Device    | 1  | The properties of a device.                                                                                                                                                                  |
| 9    | **features** | Features  | 1  | A set of items such as Action/Target pairs, profiles versions, options that are supported by the Actuator. The Target is used with the query Action to determine an Actuator's capabilities. |
| 10   | **file**     | File      | 1  | The properties of a file.                                                                                                                                                                    |
| 13   | **ipv4_net** | IPv4-Net  | 1  | An IPv4 address range including CIDR prefix length.                                                                                                                                          |
| 14   | **ipv6_net** | IPv6-Net  | 1  | An IPv6 address range including prefix length.                                                                                                                                               |
| 18   | **process**  | Process   | 1  | Common properties of an instance of a computer program as executed on an operating system.                                                                                                   |
| 1027 | **er/**      | Target$er | 1  | Targets defined in the Endpoint Response actuator profile                                                                                                                                    |

**********

**Type: Profile (Enumerated)**

| ID   | Item   | Description |
|------|--------|-------------|
| 1027 | **er** |             |

**********

**Type: Args (Map{1..\*})**

| ID   | Name                   | Type          | \#   | Description                                                                        |
|------|------------------------|---------------|------|------------------------------------------------------------------------------------|
| 1    | **start_time**         | Date-Time     | 0..1 | The specific date/time to initiate the Command                                     |
| 2    | **stop_time**          | Date-Time     | 0..1 | The specific date/time to terminate the Command                                    |
| 3    | **duration**           | Duration      | 0..1 | The length of time for an Command to be in effect                                  |
| 4    | **response_requested** | Response-Type | 0..1 | The type of Response required for the Command: `none`, `ack`, `status`, `complete` |
| 1027 | **er/**                | Args$er       | 0..1 | Command Arguments for Endpoint Response                                            |

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
| 1027 | **er/**        | Results$er      | 0..1  | Results for Endpoint Response                                       |

**********

Targets applicable to each action supported by this device

**Type: Pairs (Map{1..\*})**

| ID   | Name      | Type                         | \#   | Description |
|------|-----------|------------------------------|------|-------------|
| 3    | **query** | ArrayOf(QueryTargets) unique | 1    |             |
| 1027 | **er/**   | Pairs$er                     | 0..1 |             |

**********

**Type: QueryTargets (Enumerated)**

| ID | Item         | Description |
|----|--------------|-------------|
| 9  | **features** |             |

**********

Profile-defined targets

**Type: Target$er (Choice)**

| ID | Name               | Type              | \# | Description                                                                                                                     |
|----|--------------------|-------------------|----|---------------------------------------------------------------------------------------------------------------------------------|
| 1  | **registry_entry** | Registry-Entry$er | 1  | A registry entry applicable to Windows Operating Systems.                                                                       |
| 2  | **account**        | Account$er        | 1  | A user account on an endpoint.                                                                                                  |
| 3  | **service**        | Service$er        | 1  | A program which is managed and executed by a service host process, where several services may be sharing the same service host. |

**********

Profile-defined command arguments

**Type: Args$er (Map{1..\*})**

| ID | Name                    | Type                   | \#   | Description                                                                                                                                                       |
|----|-------------------------|------------------------|------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1  | **account_status**      | Account-Status$er      | 0..1 | Specifies whether an account shall be enabled or disabled.                                                                                                        |
| 2  | **device_containment**  | Device-Containment$er  | 0..1 | Specifies which type of isolation an endpoint shall be subjected to (e.g., port isolation, application restriction).                                              |
| 3  | **permitted_addresses** | Permitted-Addresses$er | 0..1 | Specifies which IP or domain name addresses shall remain accessible when a device is contained with the 'device_containment' Argument set to 'network_isolation'. |

**********

| Type Name      | Type Definition | Description |
|----------------|-----------------|-------------|
| **Results$er** | Map{1..*}       |             |

**********

**Type: Pairs$er (Map)**

| ID | Name        | Type                               | \# | Description |
|----|-------------|------------------------------------|----|-------------|
| 6  | **deny**    | ArrayOf(Deny-Targets$er) unique    | 1  |             |
| 7  | **contain** | ArrayOf(Contain-Targets$er) unique | 1  |             |
| 8  | **allow**   | ArrayOf(Allow-Targets$er) unique   | 1  |             |
| 9  | **start**   | ArrayOf(Start-Targets$er) unique   | 1  |             |
| 10 | **stop**    | ArrayOf(Stop-Targets$er) unique    | 1  |             |
| 11 | **restart** | ArrayOf(Restart-Targets$er) unique | 1  |             |
| 15 | **set**     | ArrayOf(Set-Targets$er) unique     | 1  |             |
| 16 | **update**  | ArrayOf(Update-Targets$er) unique  | 1  |             |
| 19 | **create**  | ArrayOf(Create-Targets$er) unique  | 1  |             |
| 20 | **delete**  | ArrayOf(Delete-Targets$er) unique  | 1  |             |

**********

**Type: Deny-Targets$er (Enumerated)**

| ID | Item         | Description |
|----|--------------|-------------|
| 1  | **file**     |             |
| 2  | **ipv4_net** |             |
| 3  | **ipv6_net** |             |

**********

**Type: Contain-Targets$er (Enumerated)**

| ID | Item         | Description |
|----|--------------|-------------|
| 1  | **file**     |             |
| 2  | **ipv4_net** |             |
| 3  | **ipv6_net** |             |

**********

**Type: Allow-Targets$er (Enumerated)**

| ID | Item         | Description |
|----|--------------|-------------|
| 1  | **file**     |             |
| 2  | **ipv4_net** |             |
| 3  | **ipv6_net** |             |

**********

**Type: Start-Targets$er (Enumerated)**

| ID | Item     | Description |
|----|----------|-------------|
| 1  | **file** |             |

**********

**Type: Stop-Targets$er (Enumerated)**

| ID | Item        | Description |
|----|-------------|-------------|
| 1  | **device**  |             |
| 2  | **process** |             |
| 3  | **service** |             |

**********

**Type: Restart-Targets$er (Enumerated)**

| ID | Item        | Description |
|----|-------------|-------------|
| 1  | **device**  |             |
| 2  | **process** |             |

**********

**Type: Set-Targets$er (Enumerated)**

| ID | Item               | Description |
|----|--------------------|-------------|
| 1  | **ipv4_net**       |             |
| 2  | **ipv6_net**       |             |
| 3  | **registry_entry** |             |
| 4  | **account**        |             |

**********

**Type: Update-Targets$er (Enumerated)**

| ID | Item     | Description |
|----|----------|-------------|
| 1  | **file** |             |

**********

**Type: Create-Targets$er (Enumerated)**

| ID | Item               | Description |
|----|--------------------|-------------|
| 1  | **registry_entry** |             |

**********

**Type: Delete-Targets$er (Enumerated)**

| ID | Item               | Description |
|----|--------------------|-------------|
| 1  | **file**           |             |
| 2  | **registry_entry** |             |
| 3  | **service**        |             |

**********

**Type: Registry-Entry$er (Record)**

| ID | Name      | Type   | \#   | Description                                                                                                         |
|----|-----------|--------|------|---------------------------------------------------------------------------------------------------------------------|
| 1  | **key**   | String | 0..1 | Specifies the full registry key including the hive.                                                                 |
| 2  | **type**  | String | 1    | The registry value type as defined in the [[Winnt.h header]](#winnth-registry-types).                               |
| 3  | **value** | String | 0..1 | The value of the registry key. The Actuator is responsible to format the value in accordance with the defined type. |

**********

**Type: Account$er (Map{1..\*})**

| ID | Name             | Type   | \#   | Description                               |
|----|------------------|--------|------|-------------------------------------------|
| 1  | **uid**          | String | 0..1 | The unique identifier of the account.     |
| 2  | **account_name** | String | 0..1 | The chosen display name of the account.   |
| 3  | **directory**    | String | 0..1 | The path to the account's home directory. |

**********

**Type: Service$er (Map{1..\*})**

| ID | Name             | Type   | \#   | Description                      |
|----|------------------|--------|------|----------------------------------|
| 1  | **name**         | String | 0..1 | The unique name of the service.  |
| 2  | **display_name** | String | 0..1 | The display name of the service. |

**********

**Type: Account-Status$er (Enumerated)**

| ID | Item         | Description                                                    |
|----|--------------|----------------------------------------------------------------|
| 1  | **enabled**  | Enable the account and render it available on the endpoint.    |
| 2  | **disabled** | Disable the account and render it unavailable on the endpoint. |

**********

**Type: Device-Containment$er (Enumerated)**

| ID | Item                  | Description                                                                                                                                                                                                                                                                  |
|----|-----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1  | **network_isolation** | Isolate the endpoint from communicating with other networked entities, typically through relegation to a private VLAN segment and/or port isolation. MAY be combined with the 'permitted_addresses' Argument to allow communication with select IP or domain name addresses. |
| 2  | **app_restriction**   | Restrict the execution of applications to only those that are signed by a trusted party (e.g., Microsoft only).                                                                                                                                                              |
| 3  | **disable_nic**       | Disable the Network Interface Controller(s) on the endpoint.                                                                                                                                                                                                                 |

**********

**Type: Permitted-Addresses$er (Map{1..\*})**

| ID | Name            | Type                 | \#   | Description                                                                          |
|----|-----------------|----------------------|------|--------------------------------------------------------------------------------------|
| 1  | **domain_name** | ArrayOf(Domain-Name) | 0..1 | The domain name address(es) the contained device(s) can still communicate with.      |
| 2  | **ipv4_net**    | ArrayOf(IPv4-Net)    | 0..1 | The IPv4 address(es) or range(s) the contained device(s) can still communicate with. |
| 3  | **ipv6_net**    | ArrayOf(IPv6-Net)    | 0..1 | The IPv6 address(es) or range(s) the contained device(s) can still communicate with. |

**********

**Type: Device (Map{1..\*})**

| ID | Name             | Type         | \#   | Description                                                                             |
|----|------------------|--------------|------|-----------------------------------------------------------------------------------------|
| 1  | **hostname**     | Hostname     | 0..1 | A hostname that can be used to connect to this device over a network                    |
| 2  | **idn_hostname** | IDN-Hostname | 0..1 | An internationalized hostname that can be used to connect to this device over a network |
| 3  | **device_id**    | String       | 0..1 | An identifier that refers to this device within an inventory or management system       |

**********

| Type Name       | Type Definition  | Description                        |
|-----------------|------------------|------------------------------------|
| **Domain-Name** | String /hostname | [[RFC1034]](#rfc1034), Section 3.5 |

**********

| Type Name    | Type Definition         | Description                                                                |
|--------------|-------------------------|----------------------------------------------------------------------------|
| **Features** | ArrayOf(Feature) unique | An array of names used to query a Consumer for its supported capabilities. |

**********

**Type: File (Map{1..\*})**

| ID | Name       | Type   | \#   | Description                                                      |
|----|------------|--------|------|------------------------------------------------------------------|
| 1  | **name**   | String | 0..1 | The name of the file as defined in the file system               |
| 2  | **path**   | String | 0..1 | The absolute path to the location of the file in the file system |
| 3  | **hashes** | Hashes | 0..1 | One or more cryptographic hash codes of the file contents        |

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

**Type: Process (Map{1..\*})**

| ID | Name             | Type           | \#   | Description                                                                          |
|----|------------------|----------------|------|--------------------------------------------------------------------------------------|
| 1  | **pid**          | Integer{0..\*} | 0..1 | Process ID of the process                                                            |
| 2  | **name**         | String         | 0..1 | Name of the process                                                                  |
| 3  | **cwd**          | String         | 0..1 | Current working directory of the process                                             |
| 4  | **executable**   | File           | 0..1 | Executable that was executed to start the process                                    |
| 5  | **parent**       | Process        | 0..1 | Process that spawned this one                                                        |
| 6  | **command_line** | String         | 0..1 | The full command line invocation used to start this process, including all arguments |

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

Cryptographic hash values

**Type: Hashes (Map{1..\*})**

| ID | Name       | Type              | \#   | Description                                     |
|----|------------|-------------------|------|-------------------------------------------------|
| 1  | **md5**    | Binary{16..16} /x | 0..1 | MD5 hash as defined in [[RFC1321]](#rfc1321)    |
| 2  | **sha1**   | Binary{20..20} /x | 0..1 | SHA1 hash as defined in [[RFC6234]](#rfc6234)   |
| 3  | **sha256** | Binary{32..32} /x | 0..1 | SHA256 hash as defined in [[RFC6234]](#rfc6234) |

**********

| Type Name    | Type Definition  | Description                                              |
|--------------|------------------|----------------------------------------------------------|
| **Hostname** | String /hostname | Internet host name as specified in [[RFC1123]](#rfc1123) |

**********

| Type Name        | Type Definition      | Description                                                                                  |
|------------------|----------------------|----------------------------------------------------------------------------------------------|
| **IDN-Hostname** | String /idn-hostname | Internationalized Internet host name as specified in [[RFC5890]](#rfc5890), Section 2.3.2.3. |

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
