import glob
import json
import os
import pprint
import sys
import xmltodict

from lxml import etree

convert = True

if convert:
    from libs.convert import base_dump, cddl_dump, proto_dump, relax_dump, thrift_dump
    from libs.schema import relax2jadn_dump, proto2jadn_dump, thrift2jadn_dump

    schema = 'schema/openc2-wd06_functional.jadn'
    test_dir = 'schema_gen_test'
    if not os.path.isdir(test_dir):
        os.makedirs(test_dir)

    with open(schema, 'rb') as r:
        schema_json = json.loads(r.read())

    proto_dump(schema_json, os.path.join(test_dir, 'openc2-wd06.proto'))
    print('Proto ^')

    proto2jadn_dump(open(os.path.join(test_dir, 'openc2-wd06.proto'), 'rb').read(), os.path.join(test_dir, 'openc2-wd06.proto.jadn'))
    print('Proto2Jadn ^')

    cddl_dump(schema_json, os.path.join(test_dir, 'openc2-wd06.cddl'))
    print('Cddl ^')

    relax_dump(schema_json, os.path.join(test_dir, 'openc2-wd06.rng'))
    print('Relax ^')

    relax2jadn_dump(open(os.path.join(test_dir, 'openc2-wd06.rng'), 'rb').read(), os.path.join(test_dir, 'openc2-wd06.rng.jadn'))
    print('Relax2Jadn ^')

    thrift_dump(schema_json, os.path.join(test_dir, 'openc2-wd06.thrift'))
    #print('Thrift ^')

    thrift2jadn_dump(open(os.path.join(test_dir, 'openc2-wd06.thrift'), 'rb').read(), os.path.join(test_dir, 'openc2-wd06.thrift.jadn'))
    print('Thrift2Jadn^')

    base_dump(schema_json, os.path.join(test_dir, 'openc2-wd06.md'), form='markdown')
    print('MD ^')

    base_dump(schema_json, os.path.join(test_dir, 'openc2-wd06.html'), form='html')
    print('HTMl ^')

else:
    if sys.version_info.major >= 3:
        from io import StringIO
    elif sys.version_info.major >= 2:
        from StringIO import StringIO

    with open('test_openc2-wd06.rng', 'rb') as r:
        relax_schema = StringIO(r.read())
        relaxng = etree.RelaxNG(etree.parse(relax_schema))

    for f in glob.glob('message/*.xml'):
        print(f)
        with open(f, 'rb') as r:
            doc = etree.parse(StringIO(r.read()))

            try:
                print('Validating: {}'.format(f))
                relaxng.assertValid(doc)
                print('Valid Message')
                pprint.pprint(json.loads(json.dumps(xmltodict.parse(etree.tostring(doc)))))
            except Exception as e:
                print('Error: {}'.format(e))
        print('')
