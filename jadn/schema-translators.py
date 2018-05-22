from libs.convert import cddl_dump, proto_dump

schema = 'schema/openc2-wd06.jadn'

with open(schema, 'rb') as r:
    schema_file = r.read()

proto_dump(schema_file, 'test_openc2-wd06.proto')

# cddl_dump(schema_file, 'test_openc2-wd06.cddl')
