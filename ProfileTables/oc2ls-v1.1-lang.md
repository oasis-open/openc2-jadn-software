         title: "OpenC2 Language and Device Template"
       package: "http://oasis-open.org/openc2/oc2ls/v1.1"
   description: "Template for creating OpenC2 v1.1 device schemas"
    namespaces: {"ls": "http://oasis-open.org/openc2/oc2ls-types/v1.1", "nsid1": "http://example.org/profile1", "slpf": "http://oasis-open.org/openc2/ap-slpf/v1.0", "sfpf": "http://oasis-open.org/openc2/ap-sfpf/v1.0", "sbom": "http://oasis-open.org/openc2/ap-sbom/v1.0", "er": "http://oasis-open.org/openc2/ap-er/v1.0", "hop": "http://oasis-open.org/openc2/ap-hop/v1.0", "av": "http://oasis-open.org/openc2/ap-av/v1.0", "ids": "http://oasis-open.org/openc2/ap-ids/v1.0", "log": "http://oasis-open.org/openc2/ap-log/v1.0", "swup": "http://oasis-open.org/openc2/ap-swup/v1.0", "pf": "http://oasis-open.org/openc2/ap-pf/v1.0", "pac": "http://oasis-open.org/openc2/ap-pac/v1.0"}
       exports: ["Message"]
       comment: "Delete unused Action/Target/Args/Results, update package, and replace example.org/profile1 with actual profile(s)"

**Type: Message (Record)**

| ID | Name          | Type    | \#   | Description |
|----|---------------|---------|------|-------------|
| 1  | **headers**   | Headers | 0..1 |             |
| 2  | **body**      | Body    | 1    |             |
| 3  | **signature** | String  | 0..1 |             |

**********

**Type: Headers (Map{1..\*})**

| ID | Name           | Type         | \#    | Description |
|----|----------------|--------------|-------|-------------|
| 1  | **request_id** | String       | 0..1  |             |
| 2  | **created**    | ls:Date-Time | 0..1  |             |
| 3  | **from**       | String       | 0..1  |             |
| 4  | **to**         | String       | 0..\* |             |

**********

Content Types

**Type: Body (Choice)**

| ID | Name       | Type           | \# | Description                                                             |
|----|------------|----------------|----|-------------------------------------------------------------------------|
| 1  | **openc2** | OpenC2-Content | 1  | Media Type 'application/openc2' -> payload=Message, body=OpenC2-Content |

**********

Content values for each message_type

**Type: OpenC2-Content (Choice)**

| ID | Name             | Type            | \# | Description |
|----|------------------|-----------------|----|-------------|
| 1  | **request**      | OpenC2-Command  | 1  |             |
| 2  | **response**     | OpenC2-Response | 1  |             |
| 3  | **notification** | OpenC2-Event    | 1  |             |

**********

The Command defines an Action to be performed on a Target

**Type: OpenC2-Command (Record)**

| ID | Name           | Type          | \#   | Description                                                       |
|----|----------------|---------------|------|-------------------------------------------------------------------|
| 1  | **action**     | Action        | 1    | The task or activity to be performed (i.e., the 'verb').          |
| 2  | **target**     | Target        | 1    | The object of the Action. The Action is performed on the Target.  |
| 3  | **args**       | Args          | 0..1 | Additional information that applies to the Command.               |
| 4  | **actuator**   | Actuator      | 0..1 | The profile defining the function to be performed by the Command. |
| 5  | **command_id** | ls:Command-ID | 0..1 | An identifier of this Command.                                    |

**********

**Type: Action (Enumerated)**

| ID | Item            | Description                                                                                                                             |
|----|-----------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| 1  | **scan**        | Systematic examination of some aspect of the entity or its environment.                                                                 |
| 2  | **locate**      | Find an object physically, logically, functionally, or by organization.                                                                 |
| 3  | **query**       | Initiate a request for information.                                                                                                     |
| 6  | **deny**        | Prevent a certain event or action from completion, such as preventing a flow from reaching a destination or preventing access.          |
| 7  | **contain**     | Isolate a file, process, or entity so that it cannot modify or access assets or processes.                                              |
| 8  | **allow**       | Permit access to or execution of a Target.                                                                                              |
| 9  | **start**       | Initiate a process, application, system, or activity.                                                                                   |
| 10 | **stop**        | Halt a system or end an activity.                                                                                                       |
| 11 | **restart**     | Stop then start a system or an activity.                                                                                                |
| 14 | **cancel**      | Invalidate a previously issued Action.                                                                                                  |
| 15 | **set**         | Change a value, configuration, or state of a managed entity.                                                                            |
| 16 | **update**      | Instruct a component to retrieve, install, process, and operate in accordance with a software update, reconfiguration, or other update. |
| 18 | **redirect**    | Change the flow of traffic to a destination other than its original destination.                                                        |
| 19 | **create**      | Add a new entity of a known type (e.g., data, files, directories).                                                                      |
| 20 | **delete**      | Remove an entity (e.g., data, files, flows).                                                                                            |
| 22 | **detonate**    | Execute and observe the behavior of a Target (e.g., file, hyperlink) in an isolated environment.                                        |
| 23 | **restore**     | Return a system to a previously known state.                                                                                            |
| 28 | **copy**        | Duplicate an object, file, data flow, or artifact.                                                                                      |
| 30 | **investigate** | Task the recipient to aggregate and report information as it pertains to a security event or incident.                                  |
| 32 | **remediate**   | Task the recipient to eliminate a vulnerability or attack point.                                                                        |

**********

**Type: Target (Choice)**

| ID   | Name                | Type               | \# | Description                                                                                          |
|------|---------------------|--------------------|----|------------------------------------------------------------------------------------------------------|
| 1    | **artifact**        | ls:Artifact        | 1  | An array of bytes representing a file-like object or a link to that object.                          |
| 2    | **command**         | ls:Command-ID      | 1  | A reference to a previously issued Command.                                                          |
| 3    | **device**          | ls:Device          | 1  | The properties of a hardware device.                                                                 |
| 7    | **domain_name**     | ls:Domain-Name     | 1  | A network domain name.                                                                               |
| 8    | **email_addr**      | ls:Email-Addr      | 1  | A single email address.                                                                              |
| 9    | **features**        | ls:Features        | 1  | A set of items used with the query Action to determine an Actuator's capabilities.                   |
| 10   | **file**            | ls:File            | 1  | Properties of a file.                                                                                |
| 11   | **idn_domain_name** | ls:IDN-Domain-Name | 1  | An internationalized domain name.                                                                    |
| 12   | **idn_email_addr**  | ls:IDN-Email-Addr  | 1  | A single internationalized email address.                                                            |
| 13   | **ipv4_net**        | ls:IPv4-Net        | 1  | An IPv4 address range including CIDR prefix length.                                                  |
| 14   | **ipv6_net**        | ls:IPv6-Net        | 1  | An IPv6 address range including prefix length.                                                       |
| 15   | **ipv4_connection** | ls:IPv4-Connection | 1  | A 5-tuple of source and destination IPv4 address ranges, source and destination ports, and protocol. |
| 16   | **ipv6_connection** | ls:IPv6-Connection | 1  | A 5-tuple of source and destination IPv6 address ranges, source and destination ports, and protocol. |
| 20   | **iri**             | ls:IRI             | 1  | An internationalized resource identifier (IRI).                                                      |
| 17   | **mac_addr**        | ls:MAC-Addr        | 1  | A Media Access Control (MAC) address - EUI-48 or EUI-64 as defined in [[EUI]](#eui).                 |
| 18   | **process**         | ls:Process         | 1  | Common properties of an instance of a computer program as executed on an operating system.           |
| 25   | **properties**      | ls:Properties      | 1  | Data attribute associated with an Actuator.                                                          |
| 19   | **uri**             | ls:URI             | 1  | A uniform resource identifier (URI).                                                                 |
| 1001 | **ap_name1/**       | nsid1:AP-Target    | 1  | Example: Profile-defined targets                                                                     |

**********

Table 3.3.1.4 lists the properties (ID/Name) and NSIDs assigned to specific Actuator Profiles. The OpenC2 Namespace Registry is the most current list of active and proposed Actuator Profiles.

**Type: Actuator (Choice)**

| ID   | Name      | Type               | \# | Description                                                                |
|------|-----------|--------------------|----|----------------------------------------------------------------------------|
| 1024 | **slpf/** | slpf:AP-Specifiers | 1  | Actuator function and specifiers for Stateless Packet Filtering            |
| 1025 | **sfpf/** | sfpf:AP-Specifiers | 1  | Actuator function and specifiers for Stateful Packet Filtering             |
| 1026 | **sbom/** | sbom:AP-Specifiers | 1  | Actuator function and specifiers for Software Bill Of Materoals retrieval  |
| 1027 | **er/**   | er:AP-Specifiers   | 1  | Actuator function and specifiers for Endpoint Response                     |
| 1028 | **hop/**  | hop:AP-Specifiers  | 1  | Actuator function and specifiers for Honeypot Operations                   |
| 1029 | **av/**   | av:AP-Specifiers   | 1  | Actuator function and specifiers for Anti-Virus Actions                    |
| 1030 | **ids/**  | ids:AP-Specifiers  | 1  | Actuator function and specifiers for Intrusion Detection                   |
| 1031 | **log/**  | log:AP-Specifiers  | 1  | Actuator function and specifiers for Logging Control                       |
| 1032 | **swup/** | swup:AP-Specifiers | 1  | Actuator function and specifiers for Software Updating                     |
| 1034 | **pf/**   | pf:AP-Specifiers   | 1  | Actuator function and specifiers for Packet Filtering                      |
| 1035 | **pac/**  | pac:AP-Specifiers  | 1  | Actuator function and specifiers for Security Posture Attribute Collection |

**********

**Type: Args (Map{1..\*})**

| ID   | Name                   | Type             | \#   | Description                                                                        |
|------|------------------------|------------------|------|------------------------------------------------------------------------------------|
| 1    | **start_time**         | ls:Date-Time     | 0..1 | The specific date/time to initiate the Command                                     |
| 2    | **stop_time**          | ls:Date-Time     | 0..1 | The specific date/time to terminate the Command                                    |
| 3    | **duration**           | ls:Duration      | 0..1 | The length of time for an Command to be in effect                                  |
| 4    | **response_requested** | ls:Response-Type | 0..1 | The type of Response required for the Command: `none`, `ack`, `status`, `complete` |
| 1001 | **ap_name1/**          | nsid1:AP-Args    | 0..1 | Example: Profile-defined command arguments                                         |

**********

OpenC2-Response defines the structure of a response to OpenC2-Command.

**Type: OpenC2-Response (Record)**

| ID | Name            | Type           | \#   | Description                                                                           |
|----|-----------------|----------------|------|---------------------------------------------------------------------------------------|
| 1  | **status**      | ls:Status-Code | 1    | An integer status code.                                                               |
| 2  | **status_text** | String         | 0..1 | A free-form human-readable description of the Response status.                        |
| 3  | **results**     | Results        | 0..1 | Map of key:value pairs that contain additional results based on the invoking Command. |

**********

Response Results

**Type: Results (Map{1..\*})**

| ID   | Name           | Type              | \#    | Description                                                         |
|------|----------------|-------------------|-------|---------------------------------------------------------------------|
| 1    | **versions**   | ls:Version unique | 0..\* | List of OpenC2 language versions supported by this Consumer         |
| 2    | **profiles**   | ls:Nsid unique    | 0..\* | List of profiles supported by this Consumer                         |
| 3    | **pairs**      | Action-Targets    | 0..1  | List of targets applicable to each supported Action                 |
| 4    | **rate_limit** | Number{0.0..\*}   | 0..1  | Maximum number of requests per minute supported by design or policy |
| 1001 | **ap_name1/**  | nsid1:AP-Results  | 0..1  | Example: Profile-defined results                                    |

**********

Content of a one-way notification

**Type: OpenC2-Event (Map{1..\*})**

| ID   | Name          | Type           | \#   | Description                                  |
|------|---------------|----------------|------|----------------------------------------------|
| 1001 | **ap_name1/** | nsid1:AP-Event | 0..1 | Example: Profile-defined event notifications |

**********

| Type Name          | Type Definition              | Description                                                |
|--------------------|------------------------------|------------------------------------------------------------|
| **Action-Targets** | MapOf(Action, Targets){1..*} | Targets applicable to each action supported by this device |

**********

| Type Name   | Type Definition                       | Description     |
|-------------|---------------------------------------|-----------------|
| **Targets** | ArrayOf(Pointer[Target]){1..*} unique | Target pointers |

**********
