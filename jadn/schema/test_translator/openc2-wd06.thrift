/* meta
 * exports - ["OpenC2-Command", "OpenC2-Response", "OpenC2-Message"]
 * description - Datatypes that define the content of OpenC2 commands and responses.
 * title - OpenC2 Language Objects
 * imports - [["slpff", "oasis-open.org/openc2/v1.0/ap-slpff"], ["jadn", "oasis-open.org/openc2/v1.0/jadn"]]
 * module - oasis-open.org/openc2/v1.0/openc2-lang
 * version - wd06
*/


struct OpenC2_Command { // The OpenC2 Command describes an action performed on a target. It can be directive or descriptive depending on the context. #jadn_opts:{"type": "Record"}
    1: required Action action; // The task or activity to be performed (i.e., the 'verb') #jadn_opts:{"type": "Action"}
    2: required Target target; // The object of the action. The action is performed on the target #jadn_opts:{"type": "Target"}
    3: optional Actuator actuator; // The subject of the action. The actuator executes the action on the target #jadn_opts:{"type": "Actuator", "options": {"min": 0}}
    4: optional Args args; // Additional information that applies to the command #jadn_opts:{"type": "Args", "options": {"min": 0}}
    5: optional string id; // Identifier used to link responses to a command #jadn_opts:{"type": "command-id", "options": {"min": 0}}
}

enum Action { // #jadn_opts:{"type": "Enumerated"}
    scan = 1; // Systematic examination of some aspect of the target entity or its environment in order to obtain information.
    locate = 2; // Find the target object physically, logically, functionally, or by organization.
    query = 3; // Initiate a request for information.
    report = 4; // Task an entity to provide information to a designated recipient.
    notify = 5; // Set an entity's alerting preferences.
    deny = 6; // Prevent a certain event or action from completion, such as preventing a flow from reaching a destination or preventing access.
    contain = 7; // Isolate a file, process, or entity so that it cannot modify or access other assets or processes.
    allow = 8; // Permit access to or execution of a target.
    start = 9; // Initiate a process, application, system, or activity.
    stop = 10; // Halt a system or end an activity.
    restart = 11; // Stop then start a system or activity.
    pause = 12; // Cease a system or activity while maintaining state.
    resume = 13; // Start a system or activity from a paused state.
    cancel = 14; // Invalidate a previously issued action.
    set = 15; // Change a value, configuration, or state of a managed entity.
    update = 16; // Instruct a component to retrieve, install, process, and operate in accordance with a software update, reconfiguration, or other update.
    move = 17; // Change the location of a file, subnet, network, or process.
    redirect = 18; // Change the flow of traffic to a destination other than its original destination.
    create = 19; // Add a new entity of a known type (e.g., data, files, directories).
    delete = 20; // Remove an entity (e.g., data, files, flows.
    snapshot = 21; // Record and store the state of a target at an instant in time.
    detonate = 22; // Execute and observe the behavior of a target (e.g., file, hyperlink) in an isolated environment.
    restore = 23; // Return the system to a previously known state.
    save = 24; // Commit data or system state to memory.
    throttle = 25; // Adjust the rate of a process, function, or activity.
    delay = 26; // Stop or hold up an activity or data transmittal.
    substitute = 27; // Replace all or part of the data, content or payload.
    copy = 28; // Duplicate a file or data flow.
    sync = 29; // Synchronize a sensor or actuator with other system components.
    investigate = 30; // Task the recipient to aggregate and report information as it pertains to a security event or incident.
    mitigate = 31; // Task the recipient to circumvent a problem without necessarily eliminating the vulnerability or attack point.
    remediate = 32; // Task the recipient to eliminate a vulnerability or attack point.
}

struct Target { // OpenC2 Target datatypes #jadn_opts:{"type": "Choice"}
    1: optional artifact artifact; // An array of bytes representing a file-like object or a link to that object. #jadn_opts:{"type": "artifact"}
    2: optional string command; // A reference to a previously issued OpenC2 command #jadn_opts:{"type": "command-id"}
    3: optional device device; // #jadn_opts:{"type": "device"}
    4: optional string directory; // #jadn_opts:{"type": "directory"}
    5: optional string disk; // #jadn_opts:{"type": "disk"}
    6: optional string disk_partition; // #jadn_opts:{"type": "disk-partition"}
    7: optional string domain_name; // #jadn_opts:{"type": "domain-name"}
    8: optional string email_addr; // #jadn_opts:{"type": "email-addr"}
    9: optional string email_message; // #jadn_opts:{"type": "email-message"}
    10: optional file file; // #jadn_opts:{"type": "file"}
    11: optional string ipv4_addr; // #jadn_opts:{"type": "ipv4-addr"}
    12: optional string ipv6_addr; // #jadn_opts:{"type": "ipv6-addr"}
    13: optional string mac_addr; // #jadn_opts:{"type": "mac-addr"}
    14: optional string memory; // #jadn_opts:{"type": "memory"}
    15: optional ip_connection ip_connection; // #jadn_opts:{"type": "ip-connection"}
    16: optional openc2 openc2; // OpenC2 - query actuator for supported capabilities, negotiate connection #jadn_opts:{"type": "openc2"}
    17: optional string process; // #jadn_opts:{"type": "process"}
    18: optional string software; // #jadn_opts:{"type": "software"}
    19: optional string uri; // #jadn_opts:{"type": "uri"}
    20: optional string user_account; // #jadn_opts:{"type": "user-account"}
    21: optional string user_session; // #jadn_opts:{"type": "user-session"}
    22: optional string volume; // #jadn_opts:{"type": "volume"}
    23: optional string windows_registry_key; // #jadn_opts:{"type": "windows-registry-key"}
    24: optional string x509_certificate; // #jadn_opts:{"type": "x509-certificate"}
    1024: optional string slpff; // Targets defined in the Stateless Packet Filter Firewall profile #jadn_opts:{"type": "Slpff-Targets"}
}

struct Actuator { // #jadn_opts:{"type": "Choice"}
    1: optional ActuatorSpecifiers generic; // #jadn_opts:{"type": "ActuatorSpecifiers"}
    1024: optional string slpff; // Specifiers as defined in the Stateless Packet Filtering Firewall profile, oasis-open.org/openc2/v1.0/ap-slpff #jadn_opts:{"type": "slpff:Specifiers"}
}

struct ActuatorSpecifiers { // #jadn_opts:{"type": "Map"}
    1: optional string actuator_id; // #jadn_opts:{"type": "uri", "options": {"min": 0}}
    2: optional string asset_id; // #jadn_opts:{"type": "String", "options": {"min": 0}}
}

struct Args { // #jadn_opts:{"type": "Map"}
    1: optional string start_time; // The specific date/time to initiate the action #jadn_opts:{"type": "date-time", "options": {"min": 0}}
    2: optional string end_time; // The specific date/time to terminate the action #jadn_opts:{"type": "date-time", "options": {"min": 0}}
    3: optional string duration; // The length of time for an action to be in effect #jadn_opts:{"type": "duration", "options": {"min": 0}}
    4: optional Response_Type response_requested; // The type of response required for the action #jadn_opts:{"type": "Response-Type", "options": {"min": 0}}
    1024: optional string slpff; // Command arguments defined in the Stateless Packet Filtering Firewall profile #jadn_opts:{"type": "slpff:Args", "options": {"min": 0}}
}

struct OpenC2_Response { // #jadn_opts:{"type": "Record"}
    1: required string id; // Id of the ommand that induced this response #jadn_opts:{"type": "command-id"}
    2: required Status_Code status; // An integer status code #jadn_opts:{"type": "Status-Code"}
    3: optional string status_text; // A free-form human-readable description of the response status #jadn_opts:{"type": "String", "options": {"min": 0}}
    4: required Results unknown; // Data or extended status information that was requested from an OpenC2 command #jadn_opts:{"type": "Results"}
}

struct Results { // #jadn_opts:{"type": "Choice"}
    1: optional string string; // List of strings #jadn_opts:{"type": "String", "options": {"max": 0, "min": 0}}
    2: optional string media; // Media type and data #jadn_opts:{"type": "Media"}
}

enum Status_Code { // #jadn_opts:{"type": "Enumerated", "options": {"compact": true}}
    Processing = 102; // An interim response used to inform the client that the server has accepted the request but not yet completed it.
    OK = 200; // The request has succeeded.
    Moved_Permanently = 301; // The target resource has been assigned a new permanent URI
    Bad_Request = 400; // The server cannot process the request due to something that is perceived to be a client error (e.g., malformed request syntax.)
    Unauthorized = 401; // The request lacks valid authentication credentials for the target resources or authorization has been refused for the submitted credentials.
    Forbidden = 403; // The server understood the request but refuses to authorize it.
    Server_Error = 500; // The server encountered an unexpected condition that prevented it from fulfilling the request.
    Not_Implemented = 501; // The server does not support the functionality required to fulfill the request.
}

struct artifact { // #jadn_opts:{"type": "Record"}
    1: optional string mime_type; // Permitted values specified in the IANA Media Types registry #jadn_opts:{"type": "String", "options": {"min": 0}}
    2: optional payload unknown; // choice of literal content or URL to obtain content #jadn_opts:{"type": "payload", "options": {"min": 0}}
    3: optional hashes hashes; // Specifies a dictionary of hashes for the contents of the payload #jadn_opts:{"type": "hashes", "options": {"min": 0}}
}

struct payload { // #jadn_opts:{"type": "Choice"}
    1: optional binary payload_bin; // Specifies the data contained in the artifact. #jadn_opts:{"type": "Binary"}
    2: optional string url; // MUST be a valid URL that resolves to the un-encoded content #jadn_opts:{"type": "uri"}
}

struct openc2 {
    1: optional list<Query_Item> item;  // A target used to query Actuator for its supported capabilities #jadn_opts:{"type": "ArrayOf", "options": {"max": 3, "min": 0, "rtype": "Query-Item"}}
}

enum Query_Item { // Results to be included in response to query openc2 command #jadn_opts:{"type": "Enumerated"}
    versions = 1; // OpenC2 language versions supported by this actuator
    profiles = 2; // List of profiles supported by this actuator
    schema = 3; // Definition of the command syntax supported by this actuator
}

struct ip_connection { // 5-tuple that specifies a tcp/ip connection #jadn_opts:{"type": "Record"}
    1: optional string src_addr; // source address #jadn_opts:{"type": "ip-addr", "options": {"min": 0}}
    2: optional string src_port; // source TCP/UDP port number #jadn_opts:{"type": "port", "options": {"min": 0}}
    3: optional string dst_addr; // destination address #jadn_opts:{"type": "ip-addr", "options": {"min": 0}}
    4: optional string dst_port; // destination TCP/UDP port number #jadn_opts:{"type": "port", "options": {"min": 0}}
    5: optional layer4_protocol layer4_protocol; // Protocol (IPv4) / Next Header (IPv6) #jadn_opts:{"type": "layer4-protocol", "options": {"min": 0}}
}

enum layer4_protocol { // protocol (IPv4) or next header (IPv6) field - any IANA value, RFC 5237 #jadn_opts:{"type": "Enumerated"}
    icmp = 1; // Internet Control Message Protocol - RFC 792
    tcp = 6; // Transmission Control Protocol - RFC 793
    udp = 17; // User Datagram Protocol - RFC 768
    sctp = 132; // Stream Control Transmission Protocol - RFC 4960
}

struct file { // #jadn_opts:{"type": "Map"}
    1: optional string name; // The name of the file as defined in the file system #jadn_opts:{"type": "String", "options": {"min": 0}}
    2: optional string path; // The absolute path to the location of the file in the file system #jadn_opts:{"type": "String", "options": {"min": 0}}
    3: optional hashes hashes; // One or more cryptographic hash codes of the file contents #jadn_opts:{"type": "hashes", "options": {"min": 0}}
}

enum Response_Type { // #jadn_opts:{"type": "Enumerated"}
    None = 0; // No response
    Ack = 1; // Respond when command received
    Complete = 2; // Respond when all aspects of command completed
}

struct Process { // #jadn_opts:{"type": "Map"}
    1: optional i64 pid; // Process ID of the process #jadn_opts:{"type": "Integer", "options": {"min": 0}}
    2: optional string name; // Name of the process #jadn_opts:{"type": "String", "options": {"min": 0}}
    3: optional string cwd; // Current working directory of the process #jadn_opts:{"type": "String", "options": {"min": 0}}
    4: optional file executable; // Executable that was executed to start the process #jadn_opts:{"type": "file", "options": {"min": 0}}
    5: optional Process parent; // Process that spawned this one #jadn_opts:{"type": "Process", "options": {"min": 0}}
    6: optional string command_line; // The full command line invocation used to start this process, including all arguments #jadn_opts:{"type": "String", "options": {"min": 0}}
}

struct hashes { // Cryptographic Hash values #jadn_opts:{"type": "Map"}
    1: optional binary md5; // Hex-encoded MD5 hash as defined in RFC3121 #jadn_opts:{"type": "Binary", "options": {"min": 0}}
    4: optional binary sha1; // Hex-encoded SHA1 hash as defined in RFC3174 #jadn_opts:{"type": "Binary", "options": {"min": 0}}
    6: optional binary sha256; // Hex-encoded SHA256 as defined in RFC6234 #jadn_opts:{"type": "Binary", "options": {"min": 0}}
}

struct device { // TODO: Add inventory device-id? #jadn_opts:{"type": "Map"}
    1: optional string description; // #jadn_opts:{"type": "String", "options": {"min": 0}}
    2: optional string device_type; // #jadn_opts:{"type": "String", "options": {"min": 0}}
    3: optional string manufacturer; // #jadn_opts:{"type": "String", "options": {"min": 0}}
    4: optional string model; // #jadn_opts:{"type": "String", "options": {"min": 0}}
    5: optional string serial_number; // #jadn_opts:{"type": "String", "options": {"min": 0}}
    6: optional string firmware_version; // #jadn_opts:{"type": "String", "options": {"min": 0}}
    7: optional string system_details; // #jadn_opts:{"type": "String", "options": {"min": 0}}
}

/* JADN Custom Fields
[
    ['command-id', 'String', [], 'Uniquely identifies a particular command - TBD syntax'],
    ['date-time', 'String', ['@date-time'], 'RFC 3339 date-time'],
    ['duration', 'String', ['@duration'], 'RFC 3339 / ISO 8601 duration'],
    ['domain-name', 'String', ['@hostname'], 'Domain name, RFC 1034, section 3.5'],
    ['email-addr', 'String', ['@email'], 'Email address, RFC 5322, section 3.4.1'],
    ['ip-addr', 'String', ['@ip'], 'IPv4 or IPv6 address'],
    ['ipv4-addr', 'String', ['@ipv4'], 'IPv4 address or range in CIDR notation, RFC 2673, section 3.2'],
    ['ipv6-addr', 'String', ['@ipv6'], 'IPv6 address or range, RFC 4291, section 2.2'],
    ['mac-addr', 'String', ['@mac'], '48 bit Media Access Code address'],
    ['port', 'String', ['@port'], 'Service Name or Transport Protocol Port Number, RFC 6335'],
    ['version', 'String', [], 'Version string - TBD syntax'],
    ['uri', 'String', ['@uri'], 'Uniform Resource Identifier']
]
*/