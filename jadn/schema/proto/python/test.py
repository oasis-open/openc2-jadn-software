import openc2_pb2 as proto

from google.protobuf.json_format import Parse, MessageToDict

msg_json = open('../deny_ip_valid.json', 'r').read()
msg_proto_json = proto.OpenC2Command()
msg_proto_file = proto.OpenC2Command()
msg_proto_str = proto.OpenC2Command()

Parse(msg_json, msg_proto_json)

with open('deny_ip_valid.pb', 'wb') as f:
    f.write(msg_proto_json.SerializeToString())

with open('deny_ip_valid.pb', 'rb') as f:
    msg_proto_file.ParseFromString(f.read())

print("Json:\n{}".format(msg_proto_json))
print("File:\n{}".format(msg_proto_file))
print("String:\n{}".format(msg_proto_str))

msg_proto_str.ParseFromString(msg_proto_file.SerializeToString())

print(MessageToDict(msg_proto_str, preserving_proto_field_name=True))
