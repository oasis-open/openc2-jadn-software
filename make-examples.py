import fire
import jadn
import json
import os
from jsf import JSF

SCHEMA_DIR = 'Schemas'
OUT_DIR = 'Out'


def make_ex(schema: str = 'resolve.jidl', out: str = 'resolve.json'):
    filename, ext = os.path.splitext(schema)
    with open(os.path.join(SCHEMA_DIR, schema)) as fp:
        sc = jadn.load_any(fp)
    sc2 = jadn.transform.resolve_imports(sc, SCHEMA_DIR, ('acme'))
    sc2_js = json.loads(js := jadn.translate.json_schema_dumps(sc2))
    with open(path := os.path.join(OUT_DIR, out), 'w') as fp:
        json.dump(sc2_js, fp, indent=2)
    faker = JSF.from_json(path)
    ex = faker.generate()
    print(json.dumps(ex, indent=2))


if __name__ == '__main__':
    print(f'Installed JADN version: {jadn.__version__}\n')
    os.makedirs(OUT_DIR, exist_ok=True)
    try:
        fire.Fire(make_ex)
    except FileNotFoundError as e:
        print(e)
