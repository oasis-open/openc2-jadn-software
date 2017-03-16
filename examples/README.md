## OpenC2 Command examples

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