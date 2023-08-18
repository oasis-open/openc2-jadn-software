import jadn
import json
import os

SCHEMA = os.path.join('..', '..', 'Schemas', 'Metaschema', 'oscal-catalog.jadn')

with open(SCHEMA) as fp:
    sc = jadn.load(fp)
    print(f'{SCHEMA}:\n' + '\n'.join([f'{k:>15}: {v}' for k, v in jadn.analyze(jadn.check(sc)).items()]))
codec = jadn.codec.Codec(sc, verbose_rec=True, verbose_str=True)

for f in os.scandir('.'):
    if (fn := f.name) == 'basic-catalog.json':
        print(fn)
        with open(fn, encoding='utf-8') as fd:
            file = json.load(fd)
        try:
            codec.encode('Oscal', file)
        except ValueError as e:
            print(f'  ### {e}')