from libs.schema import JADNtoProto3, Proto3toJADN

schema = 'schema/openc2-wd05.jadn'

with open(schema, 'rb') as r:
    schema_file = r.read()

schema_proto = JADNtoProto3(schema_file).proto_dump()
schema_jadn = Proto3toJADN(schema_proto).jadn_dump()

with open('test_openc2-wd05.proto', 'wb') as w:
    w.write(schema_proto)

with open('test_openc2-wd05.jadn', 'wb') as w:
    w.write(schema_jadn)
