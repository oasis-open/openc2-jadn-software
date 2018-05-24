import glob

from lxml import etree

from StringIO import StringIO

convert = False

if convert:
    from libs.convert import cddl_dump, proto_dump, relax_dump

    schema = 'schema/openc2-wd06.jadn'

    with open(schema, 'rb') as r:
        schema_file = r.read()

    proto_dump(schema_file, 'test_openc2-wd06.proto')

    cddl_dump(schema_file, 'test_openc2-wd06.cddl')

    relax_dump(schema_file, 'test_openc2-wd06.rng')

else:
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
            except Exception as e:
                print('Error: {}'.format(e))
        print('')
