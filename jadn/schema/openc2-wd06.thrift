/*
* Module: openC2
* Title: OpenC2 Command Definitions
* Version: wd06
* Description: Datatypes that define the content of OpenC2 commands and responses.
*/

struct OpenC2_Command {
    1: required Action action;
    2: required Target target;
    3: optional Actuator actuator;
    4: optional Args args;
    5: required string id;
}

enum Action {
    scan = 1,
    locate = 2,
    query = 3,
    report = 4,
    notify = 5,
    deny = 6,
    contain = 7,
    allow = 8,
    start = 9,
    stop = 10,
    restart = 11,
    pause = 12,
    resume = 13,
    cancel = 14,
    set = 15, // Not sure if this is ok
    update = 16,
    move = 17,
    redirect = 18,
    create = 19,
    delete = 20,
    snapshot = 21,
    detonate = 22,
    restore = 23,
    save = 24,
    throttle = 25,
    delay = 26,
    substitute = 27,
    copy = 28,
    sync = 29,
    investigate = 30,
    mitigate = 31,
    remediate = 32,
}

struct Target {  // Cannot find a 'choice' option for thrift, using all optional tags for time being.
    1: optional string artifact;
    2: optional string command;
    3: optional Device device;
    4: optional string disk;
    5: optional string disk_partition;
    6: optional string domain_name;
    7: optional string email_addr;
    8: optional string email_message;
    9: optional File file;
    10: optional string ipv4_addr;
    11: optional string ipv6_addr;
    12: optional string mac_addr;
    13: optional string memory;
    14: optional Ip_Connection ip_connection;
    15: optional Openc2 openc2;
    16: optional Process process;
    17: optional string software;
    18: optional string uri;
    19: optional string user_account;
    20: optional string user_session;
    21: optional string volume;
    22: optional string windows_registry_key;
    23: optional string x509_certificate;
    24: optional string slpff;
}

struct Actuator {  // This is a 'choice'
    1: optional string spff;
}

struct Args {  // Not sure how to create a map using thrift, using struct for now.
    1: optional string start_time;
    2: optional string end_time;
    3: optional string duration;
    4: optional string response_requested;
    5: optional string spff;
}

struct OpenC2_Response {
    1: required string id;
    2: required Status_Code status;
    3: optional string status_text;
    4: required string results;
}

enum Status_Code {  // enumerated boolean? (how its shown on original jadn. Left as normal enum here.
    processing = 102,
    ok = 200,
    moved = 301,
    bad_request = 400,
    unauthorized = 401,
    forbidden = 403,
    server_error = 500,
    not_implemented = 501,
}

struct Artifact {
    1: optional string mime_type;
    2: optional Payload payload;
    3: optional Hashes hashes;
}

struct Payload {  // This is a 'choice'
    1: optional binary payload_bin;
    2: optional string uri;
}

struct Openc2 {  //  Listed as 'arrayof' not sure.
    1: optional list<Query_Item> item;
}

enum Query_Item {
    versions = 1,
    profiles = 2,
    schema = 3,
}

struct Ip_Connection {
    1: optional string src_addr;
    2: optional string src_port;
    3: optional string dst_addr;
    4: optional string dst_port;
    5: optional Layer4_Protocol layer4_protocol;
}

enum Layer4_Protocol {
    icmp = 1,
    tcp = 2,
    udp = 3,
    sctp = 4,
}

struct File {  // This is a map
    1: optional string name;
    2: optional string path;
    3: optional Hashes hash;
}

enum Response_Type {
    none = 1,
    ack = 2,
    complete = 3,
}

struct Process {  // This is a map
    1: optional i64 pid;
    2: optional string name;
    3: optional string cwd;
    4: optional File executable;
    5: optional Process parent;
    6: optional string command_line;
}

struct Hashes {  // This is a map
    1: optional binary md5;
    2: optional binary sha1;
    3: optional binary  sha256;
}

struct Device {  // This is a map
    1: optional string description;
    2: optional string device_type;
    3: optional string manufacturer;
    4: optional string  model;
    5: optional string serial_number;
    6: optional string firmware_version;
    7: optional string system_details;
}