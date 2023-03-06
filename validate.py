import fire
import jadn
import json
import os

SCHEMA_DIR = 'Schemas'
DATA_DIR = 'Data'

def validate(file: str = 'container.json', schema: str = 'container.jidl') -> None:
    filename, ext = os.path.splitext(file)
    with open(os.path.join(SCHEMA_DIR, schema), encoding='utf-8') as fp:
        sc = jadn.load_any(fp)
    with open(os.path.join(DATA_DIR, file), encoding='utf-8') as fp:
        data = json.load(fp)
    print(len(sc), len(data))

if __name__ == '__main__':
    try:
        fire.Fire(validate)
    except FileNotFoundError as e:
        print(e)