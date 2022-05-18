         title: "OpenC2 Language Common Types"
       package: "http://oasis-open.org/openc2/oc2ls-types/v1.1"
       version: "0-wd01"
   description: "Common Types from the OpenC2 Language Specification version 1.1.  These definitions are referenced by or copied into Profiles"
       exports: ["Artifact", "Command-ID", "Date-Time", "Device", "Domain-Name", "Duration", "Email-Addr", "Feature", "Features", "File", "IDN-Domain-Name", "IDN-Email-Addr", "IPv4-Net", "IPv4-Connection", "IPv6-Net", "IPv6-Connection", "IRI", "MAC-Addr", "Nsid", "Process", "Properties", "Response-Type", "Status-Code", "URI", "Version"]

**Type: Artifact (Record{1..\*})**

| ID | Name          | Type    | \#   | Description                                                                        |
|----|---------------|---------|------|------------------------------------------------------------------------------------|
| 1  | **mime_type** | String  | 0..1 | Permitted values specified in the IANA Media Types registry, [[RFC6838]](#rfc6838) |
| 2  | **payload**   | Payload | 0..1 | Choice of literal content or URL                                                   |
| 3  | **hashes**    | Hashes  | 0..1 | Hashes of the payload content                                                      |

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

| Type Name      | Type Definition | Description                                         |
|----------------|-----------------|-----------------------------------------------------|
| **Email-Addr** | String /email   | Email address, [[RFC5322]](#rfc5322), Section 3.4.1 |

**********

| Type Name    | Type Definition                | Description                                                                           |
|--------------|--------------------------------|---------------------------------------------------------------------------------------|
| **Features** | ArrayOf(Feature){0..10} unique | An array of zero to ten names used to query a Consume for its supported capabilities. |

**********

**Type: File (Map{1..\*})**

| ID | Name       | Type   | \#   | Description                                                      |
|----|------------|--------|------|------------------------------------------------------------------|
| 1  | **name**   | String | 0..1 | The name of the file as defined in the file system               |
| 2  | **path**   | String | 0..1 | The absolute path to the location of the file in the file system |
| 3  | **hashes** | Hashes | 0..1 | One or more cryptographic hash codes of the file contents        |

**********

| Type Name           | Type Definition      | Description                                                           |
|---------------------|----------------------|-----------------------------------------------------------------------|
| **IDN-Domain-Name** | String /idn-hostname | Internationalized Domain Name, [[RFC5890]](#rfc5890), Section 2.3.2.3 |

**********

| Type Name          | Type Definition   | Description                                            |
|--------------------|-------------------|--------------------------------------------------------|
| **IDN-Email-Addr** | String /idn-email | Internationalized email address, [[RFC6531]](#rfc6531) |

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

| Type Name | Type Definition | Description                                                   |
|-----------|-----------------|---------------------------------------------------------------|
| **IRI**   | String /iri     | Internationalized Resource Identifier, [[RFC3987]](#rfc3987). |

**********

| Type Name    | Type Definition | Description                                                                                            |
|--------------|-----------------|--------------------------------------------------------------------------------------------------------|
| **MAC-Addr** | Binary /eui     | Media Access Control / Extended Unique Identifier address - EUI-48 or EUI-64 as defined in [EUI](#eui) |

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

| Type Name      | Type Definition              | Description                                                                |
|----------------|------------------------------|----------------------------------------------------------------------------|
| **Properties** | ArrayOf(String){1..*} unique | A list of names that uniquely identify properties supported by a Consumer. |

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

**Type: Payload (Choice)**

| ID | Name    | Type   | \# | Description                                                 |
|----|---------|--------|----|-------------------------------------------------------------|
| 1  | **bin** | Binary | 1  | Specifies the data contained in the artifact                |
| 2  | **url** | URI    | 1  | MUST be a valid URL that resolves to the un-encoded content |

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

| Type Name   | Type Definition | Description                |
|-------------|-----------------|----------------------------|
| **Version** | String          | Major.Minor version number |

**********
