         title: "OpenC2 base device schema for the SLPF-2000 packet filter"
       package: "http://acme.com/schemas/device-base/slpf2000/v2.4"
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

| ID | Item       | Description                                                                                                                             |
|----|------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| 3  | **query**  | Initiate a request for information.                                                                                                     |
| 6  | **deny**   | Prevent a certain event or action from completion, such as preventing a flow from reaching a destination or preventing access.          |
| 8  | **allow**  | Permit access to or execution of a Target.                                                                                              |
| 16 | **update** | Instruct a component to retrieve, install, process, and operate in accordance with a software update, reconfiguration, or other update. |
| 20 | **delete** | Remove an entity (e.g., data, files, flows).                                                                                            |

**********

**Type: Target (Choice)**

| ID   | Name                | Type            | \# | Description                                                                                          |
|------|---------------------|-----------------|----|------------------------------------------------------------------------------------------------------|
| 9    | **features**        | Features        | 1  | A set of items used with the query Action to determine an Actuator's capabilities.                   |
| 10   | **file**            | File            | 1  | Properties of a file.                                                                                |
| 13   | **ipv4_net**        | IPv4-Net        | 1  | An IPv4 address range including CIDR prefix length.                                                  |
| 14   | **ipv6_net**        | IPv6-Net        | 1  | An IPv6 address range including prefix length.                                                       |
| 15   | **ipv4_connection** | IPv4-Connection | 1  | A 5-tuple of source and destination IPv4 address ranges, source and destination ports, and protocol. |
| 16   | **ipv6_connection** | IPv6-Connection | 1  | A 5-tuple of source and destination IPv6 address ranges, source and destination ports, and protocol. |
| 1024 | **slpf/**           | Target$slpf     | 1  | Profile-defined targets                                                                              |

**********

**Type: Args (Map{1..\*})**

| ID   | Name                   | Type          | \#   | Description                                                                |
|------|------------------------|---------------|------|----------------------------------------------------------------------------|
| 1    | **start_time**         | Date-Time     | 0..1 | The specific date/time to initiate the Command                             |
| 2    | **stop_time**          | Date-Time     | 0..1 | The specific date/time to terminate the Command                            |
| 3    | **duration**           | Duration      | 0..1 | The length of time for an Command to be in effect                          |
| 4    | **response_requested** | Response-Type | 0..1 | The type of Response required for the Command: none, ack, status, complete |
| 1024 | **slpf/**              | Args$slpf     | 0..1 | Profile-defined command arguments                                          |

**********

**Type: Profile (Enumerated)**

| ID   | Item     | Description |
|------|----------|-------------|
| 1024 | **slpf** |             |

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

| ID   | Name           | Type                   | \#    | Description                                                         |
|------|----------------|------------------------|-------|---------------------------------------------------------------------|
| 1    | **versions**   | SemVer unique          | 0..10 | List of OpenC2 language versions supported by this Actuator         |
| 2    | **profiles**   | Nsid unique            | 0..\* | List of profiles supported by this Actuator                         |
| 3    | **pairs**      | Pairs                  | 0..1  | DEPRECATED: targets applicable to each supported Action             |
| 4    | **rate_limit** | Number{0.0..\*}        | 0..1  | Maximum number of requests per minute supported by design or policy |
| 5    | **args**       | Enumerated(Enum[Args]) | 0..\* | List of supported Command Arguments                                 |
| 1024 | **slpf/**      | Results$slpf           | 0..1  | Profile-defined results                                             |

**********

Targets applicable to each action supported by this device

**Type: Pairs (Map{1..\*})**

| ID   | Name      | Type                         | \# | Description                                                     |
|------|-----------|------------------------------|----|-----------------------------------------------------------------|
| 3    | **query** | ArrayOf(QueryTargets) unique | 1  |                                                                 |
| 1024 | **slpf/** | Pairs$slpf                   | 1  | Targets of each Action for Software Bill Of Materials retrieval |

**********

**Type: QueryTargets (Enumerated)**

| ID | Item         | Description |
|----|--------------|-------------|
| 9  | **features** |             |

**********

SLPF targets

**Type: Target$slpf (Choice)**

| ID | Name            | Type         | \# | Description                                                                           |
|----|-----------------|--------------|----|---------------------------------------------------------------------------------------|
| 1  | **rule_number** | Rule-ID$slpf | 1  | Immutable identifier assigned when a rule is created. Identifies a rule to be deleted |

**********

SLPF command arguments

**Type: Args$slpf (Map{1..\*})**

| ID | Name             | Type              | \#   | Description                                                                                                                                                                                                  |
|----|------------------|-------------------|------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1  | **drop_process** | Drop-Process$slpf | 0..1 | Specifies how to handle denied packets                                                                                                                                                                       |
| 2  | **persistent**   | Boolean           | 0..1 | Normal operations assume any changes to a device are to be implemented persistently. Setting the persistent modifier to FALSE results in a change that is not persistent in the event of a reboot or restart |
| 3  | **direction**    | Direction$slpf    | 0..1 | Specifies whether to apply rules to incoming or outgoing traffic. If omitted, rules are applied to both                                                                                                      |
| 4  | **insert_rule**  | Rule-ID$slpf      | 0..1 | Specifies the identifier of the rule within a list, typically used in a top-down rule list                                                                                                                   |

**********

SLPF results defined in this profile

**Type: Results$slpf (Map)**

| ID | Name            | Type         | \#   | Description                                          |
|----|-----------------|--------------|------|------------------------------------------------------|
| 1  | **rule_number** | Rule-ID$slpf | 0..1 | Rule identifier returned from allow or deny Command. |

**********

**Type: Pairs$slpf (Enumerated)**

| ID | Item                                                            | Description |
|----|-----------------------------------------------------------------|-------------|
| 3  | **query: features**                                             |             |
| 6  | **deny: ipv4_net, ipv6_net, ipv4_connection, ipv6_connection**  |             |
| 8  | **allow: ipv4_net, ipv6_net, ipv4_connection, ipv6_connection** |             |
| 16 | **update: file**                                                |             |
| 20 | **delete: /rule_number**                                        |             |

**********

**Type: Drop-Process$slpf (Enumerated)**

| ID | Item          | Description                                                                                   |
|----|---------------|-----------------------------------------------------------------------------------------------|
| 1  | **none**      | Drop the packet and do not send a notification to the source of the packet                    |
| 2  | **reject**    | Drop the packet and send an ICMP host unreachable (or equivalent) to the source of the packet |
| 3  | **false_ack** | Drop the traffic and send a false acknowledgement                                             |

**********

**Type: Direction$slpf (Enumerated)**

| ID | Item        | Description                          |
|----|-------------|--------------------------------------|
| 1  | **both**    | Apply rules to all traffic           |
| 2  | **ingress** | Apply rules to incoming traffic only |
| 3  | **egress**  | Apply rules to outgoing traffic only |

**********

| Type Name        | Type Definition | Description            |
|------------------|-----------------|------------------------|
| **Rule-ID$slpf** | Integer         | Access rule identifier |

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

5-tuple that specifies a tcp/ip connection

**Type: IPv4-Connection (Record{1..\*})**

| ID | Name         | Type        | \#   | Description                                                               |
|----|--------------|-------------|------|---------------------------------------------------------------------------|
| 1  | **src_addr** | IPv4-Net    | 0..1 | IPv4 source address range                                                 |
| 2  | **src_port** | Port        | 0..1 | Source service per [[RFC6335]](#rfc6335)                                  |
| 3  | **dst_addr** | IPv4-Net    | 0..1 | IPv4 destination address range                                            |
| 4  | **dst_port** | Port        | 0..1 | Destination service per [[RFC6335]](#rfc6335)                             |
| 5  | **protocol** | L4-Protocol | 0..1 | Layer 4 protocol (e.g., TCP) - see [Section 3.4.2.10](#34210-l4-protocol) |

**********

IPv6 address and prefix length

**Type: IPv6-Net (Array /ipv6-net)**

| ID | Type      | \#   | Description                                                                    |
|----|-----------|------|--------------------------------------------------------------------------------|
| 1  | IPv6-Addr | 1    | **ipv6_addr** - IPv6 address as defined in [[RFC8200]](#rfc8200)               |
| 2  | Integer   | 0..1 | **prefix_length** - prefix length. If omitted, refers to a single host address |

**********

5-tuple that specifies a tcp/ip connection

**Type: IPv6-Connection (Record{1..\*})**

| ID | Name         | Type        | \#   | Description                                                           |
|----|--------------|-------------|------|-----------------------------------------------------------------------|
| 1  | **src_addr** | IPv6-Net    | 0..1 | IPv6 source address range                                             |
| 2  | **src_port** | Port        | 0..1 | Source service per [[RFC6335]](#rfc6335)                              |
| 3  | **dst_addr** | IPv6-Net    | 0..1 | IPv6 destination address range                                        |
| 4  | **dst_port** | Port        | 0..1 | Destination service per [[RFC6335]](#rfc6335)                         |
| 5  | **protocol** | L4-Protocol | 0..1 | Layer 4 protocol (e.g., TCP) - [Section 3.4.2.10](#34210-l4-protocol) |

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

| Type Name     | Type Definition   | Description                                             |
|---------------|-------------------|---------------------------------------------------------|
| **IPv4-Addr** | Binary /ipv4-addr | 32 bit IPv4 address as defined in [[RFC0791]](#rfc0791) |

**********

| Type Name     | Type Definition   | Description                                              |
|---------------|-------------------|----------------------------------------------------------|
| **IPv6-Addr** | Binary /ipv6-addr | 128 bit IPv6 address as defined in [[RFC8200]](#rfc8200) |

**********

Value of the protocol (IPv4) or next header (IPv6) field in an IP packet. Any IANA value, [[RFC5237]](#rfc5237)

**Type: L4-Protocol (Enumerated)**

| ID  | Item     | Description                                                  |
|-----|----------|--------------------------------------------------------------|
| 1   | **icmp** | Internet Control Message Protocol - [[RFC0792]](#rfc0792)    |
| 6   | **tcp**  | Transmission Control Protocol - [[RFC0793]](#rfc0793)        |
| 17  | **udp**  | User Datagram Protocol - [[RFC0768]](#rfc0768)               |
| 132 | **sctp** | Stream Control Transmission Protocol - [[RFC4960]](#rfc4960) |

**********

| Type Name | Type Definition | Description                                    |
|-----------|-----------------|------------------------------------------------|
| **Nsid**  | String{1..16}   | A short identifier that refers to a namespace. |

**********

| Type Name | Type Definition   | Description                                           |
|-----------|-------------------|-------------------------------------------------------|
| **Port**  | Integer{0..65535} | Transport Protocol Port Number, [[RFC6335]](#rfc6335) |

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
