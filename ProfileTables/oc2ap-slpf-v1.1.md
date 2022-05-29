         title: "Stateless Packet Filtering Profile"
       package: "http://oasis-open.org/openc2/oc2slpf/v1.1"
       version: "0-wd01"
   description: "Data definitions for Stateless Packet Filtering (SLPF) functions"
    namespaces: {"ls": "http://oasis-open.org/openc2/oc2ls-types/v1.1"}
       exports: ["AP-Target", "AP-Args", "AP-Specifiers", "AP-Results"]

**Type: Action (Enumerated)**

| ID | Item       | Description |
|----|------------|-------------|
| 3  | **query**  |             |
| 6  | **deny**   |             |
| 8  | **allow**  |             |
| 16 | **update** |             |
| 20 | **delete** |             |

**********

**Type: Target (Enumerated)**

| ID | Item                | Description |
|----|---------------------|-------------|
| 9  | **features**        |             |
| 10 | **file**            |             |
| 13 | **ipv4_net**        |             |
| 14 | **ipv6_net**        |             |
| 15 | **ipv4_connection** |             |
| 16 | **ipv6_connection** |             |
| 0  | **ap_name**         |             |

**********

**Type: Args (Enumerated)**

| ID | Item                   | Description |
|----|------------------------|-------------|
| 1  | **start_time**         |             |
| 2  | **stop_time**          |             |
| 3  | **duration**           |             |
| 4  | **response_requested** |             |
| 0  | **ap_name**            |             |

**********

**Type: Actuator (Enumerated)**

| ID | Item        | Description |
|----|-------------|-------------|
| 0  | **ap_name** |             |

**********

**Type: Results (Enumerated)**

| ID | Item           | Description |
|----|----------------|-------------|
| 1  | **versions**   |             |
| 2  | **profiles**   |             |
| 3  | **pairs**      |             |
| 4  | **rate_limit** |             |
| 5  | **args**       |             |
| 0  | **ap_name**    |             |

**********

**Type: Pairs (Enumerated)**

| ID | Item                                                            | Description |
|----|-----------------------------------------------------------------|-------------|
| 3  | **query: features**                                             |             |
| 6  | **deny: ipv4_net, ipv6_net, ipv4_connection, ipv6_connection**  |             |
| 8  | **allow: ipv4_net, ipv6_net, ipv4_connection, ipv6_connection** |             |
| 16 | **update: file**                                                |             |
| 20 | **delete: /rule_number**                                        |             |

**********

SLPF targets

**Type: AP-Target (Choice)**

| ID | Name            | Type    | \# | Description                                                                           |
|----|-----------------|---------|----|---------------------------------------------------------------------------------------|
| 1  | **rule_number** | Rule-ID | 1  | Immutable identifier assigned when a rule is created. Identifies a rule to be deleted |

**********

SLPF command arguments

**Type: AP-Args (Map{1..\*})**

| ID | Name             | Type         | \#   | Description                                                                                                                                                                                                  |
|----|------------------|--------------|------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1  | **drop_process** | Drop-Process | 0..1 | Specifies how to handle denied packets                                                                                                                                                                       |
| 2  | **persistent**   | Boolean      | 0..1 | Normal operations assume any changes to a device are to be implemented persistently. Setting the persistent modifier to FALSE results in a change that is not persistent in the event of a reboot or restart |
| 3  | **direction**    | Direction    | 0..1 | Specifies whether to apply rules to incoming or outgoing traffic. If omitted, rules are applied to both                                                                                                      |
| 4  | **insert_rule**  | Rule-ID      | 0..1 | Specifies the identifier of the rule within a list, typically used in a top-down rule list                                                                                                                   |

**********

SLPF actuator specifiers (may be empty)

**Type: AP-Specifiers (Map)**

| ID | Name            | Type   | \#    | Description                                                                                            |
|----|-----------------|--------|-------|--------------------------------------------------------------------------------------------------------|
| 1  | **hostname**    | String | 0..1  | RFC 1123 hostname (can be a domain name or IP address) for a particular device with SLPF functionality |
| 2  | **named_group** | String | 0..1  | User defined collection of devices with SLPF functionality                                             |
| 3  | **asset_id**    | String | 0..1  | Unique identifier for a particular SLPF                                                                |
| 4  | **asset_tuple** | String | 0..10 | Unique tuple identifier for a particular SLPF consisting of a list of up to 10 strings                 |

**********

SLPF results defined in this profile

**Type: AP-Results (Map)**

| ID | Name            | Type    | \#   | Description                                          |
|----|-----------------|---------|------|------------------------------------------------------|
| 1  | **rule_number** | Rule-ID | 0..1 | Rule identifier returned from allow or deny Command. |

**********

**Type: Drop-Process (Enumerated)**

| ID | Item          | Description                                                                                   |
|----|---------------|-----------------------------------------------------------------------------------------------|
| 1  | **none**      | Drop the packet and do not send a notification to the source of the packet                    |
| 2  | **reject**    | Drop the packet and send an ICMP host unreachable (or equivalent) to the source of the packet |
| 3  | **false_ack** | Drop the traffic and send a false acknowledgement                                             |

**********

**Type: Direction (Enumerated)**

| ID | Item        | Description                          |
|----|-------------|--------------------------------------|
| 1  | **both**    | Apply rules to all traffic           |
| 2  | **ingress** | Apply rules to incoming traffic only |
| 3  | **egress**  | Apply rules to outgoing traffic only |

**********

| Type Name   | Type Definition | Description            |
|-------------|-----------------|------------------------|
| **Rule-ID** | Integer         | Access rule identifier |

**********
