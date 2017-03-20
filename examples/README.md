## OpenC2 Command examples

This folder contains example OpenC2 commands in two Application Programming Interface (API) formats
and three JSON-based message formats.  **API** values are the structured data objects used by a program, e.g.,
Dictionary and List values for Python applications, Map/WeakMap and Array values for Javascript
applications, or Hash and Array values for Ruby applications.  **Message** values are data objects
that have been serialized (encoded) for transmission between applications or for storage.  The current examples
use JSON serializations, but XML and binary serializations are also possible.  These messages
are encoding alternatives derived from the same abstract syntax; they are not alternative syntax
specifications requiring separate development and maintenance.

**API / Verbose:** Structured data object as used by a Python application, and the direct JSON
serialization of that object as produced by `json.dumps`.  Python literal notation is similar but
not identical to JSON, so the JSON examples shown here would need to be slightly edited for use
as Python literals if they contain boolean or null values.

**API Flat:** Some developers may find it more convenient to work with flattened data values, e.g.
a dictionary containing only primitive data values instead of a dictionary containing nested complex data.
The JAEN package includes routines `flatten` and `fluff` to convert between structured and flat Python dicts.

**JSON-concise:** A message format shown primarily to illustrate how positional encoding eliminates
the need to transmit dictionary keys with every message.  This format produces messages intermediate
in size between verbose and minified encodings.

**JSON-minified:** A message format optimized for minimum bandwidth and storage space, using both
positional encoding and by replacing enumerated strings with integer tags.  This format produces minimum
bandwidth messages for a text-based encoding, although binary encodings would be smaller.


### -- MITIGATE --
#### API / Verbose
```
{   "action": "mitigate",
    "target": {
        "domain_name": {"value": "cdn.badco.org"}}}
```
#### API Flat
```
{   "action": "mitigate",
    "target.domain_name.value": "cdn.badco.org"
}
```
#### Concise
```
["mitigate",{"domain_name":["cdn.badco.org"]}]
```
#### Minified
```
[32,{"7":["cdn.badco.org"]}]
```
### -- CONTAIN --
#### API / Verbose
```
{   "action": "contain",
    "target": {
        "user_account":{
            "user_id": "21942",
            "account_login": "jsmith",
            "is_disabled": true,
            "account_last_login": "1997"}}}
```
#### API Flat
```
{   "action": "contain",
    "target.user_account.user_id": "21942",
    "target.user_account.account_login": "jsmith",
    "target.user_account.is_disabled": true,
    "target.user_account.account_last_login": "2017-03-16T07:38:12-04:00"
}
```
#### Concise
```
[   "contain",{
        "user_account":{
            "user_id": "21942",
            "account_login": "jsmith",
            "is_disabled": true,
            "account_last_login": "1997"}}]
```
#### Minified
```
[7,{"19":{"1":"21942","2":"jsmith","8": true,"13":"1997"}}]
```
### -- DENY --
#### API / Verbose
```
{   "action": "deny",
    "target": {
        "ip_connection": {
            "src_addr": {"name": {"value": "www.badco.com"}},
            "src_port": {"protocol": "https"},
            "dst_addr": {"ipv4": {"value": "192.168.1.1"}},
            "layer4_protocol": "TCP"
        }},
    "actuator": {
        "network_firewall": {"asset_id": "30"}},
    "modifiers": {
        "command_ref": "pf17_8675309",
        "context": "91",
        "datetime": "2016-11-25T08:10:31-04:00",
        "duration": "PT2M30S"}}
```
#### API Flat
```
{   "action": "deny",
    "target.ip_connection.src_addr.name.value": "www.badco.com",
    "target.ip_connection.src_port.protocol": "https",
    "target.ip_connection.dst_addr.ipv4.value": "192.168.1.1",
    "target.ip_connection.layer4_protocol": "TCP",
    "actuator.network_firewall.asset_id": "30",
    "modifiers.command_ref": "pf17_8675309",
    "modifiers.context": "91",
    "modifiers.datetime": "2016-11-25T08:10:31-04:00",
    "modifiers.duration": "PT2M30S"
}
```
#### Concise
```
[   "deny",
    {"ip_connection": [
        {"name": ["www.badco.com"]},
        {"protocol": "https"},
        {"ipv4": ["192.168.1.1"]},
        null,
        null,
        "TCP"]},
    {"network_firewall": [null, "30"]},
    {"context": "91",
    "datetime": "2016-11-25T08:10:31-04:00",
    "duration": "PT2M30S",
    "command_ref": "pf17_8675309"}]
```
#### Minified
```
[6,{"15":[{"3":["www.badco.com"]},{"2":443},
{"1":["192.168.1.1"]},null,null,6]},{"14":[null,"30"]},
{"1":"91","2":"2016-11-25T08:10:31-04:00","4":"PT2M30S",
"6":"pf17_8675309"}]
```
### -- Scan --
#### API / Verbose
```
{   "action": "scan",
    "target": {
        "domain_name": {
            "value": "www.example.com",
            "resolves_to": [
                {"ipv4": {"value": "198.51.100.2"}},
                {"name": {"value": "ms34.example.com"}}]}}}
```
#### API Flat
```
{   "action": "scan",
    "target.domain_name.value": "www.example.com",
    "target.domain_name.resolves_to.0.ipv4.value": "198.51.100.2",
    "target.domain_name.resolves_to.1.name.value": "ms34.example.com"
}
```
#### Concise
```
[   "scan", {
        "domain_name": [
            "www.example.com", [
                {"ipv4": ["198.51.100.2"]},
                {"name": ["ms34.example.com"]}]]}]
```
#### Minified
```
[1,{"7":["www.example.com",[{"1":["198.51.100.2"]},{"3":["ms34.example.com"]}]]}]
```