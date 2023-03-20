import fire
import jadn
import json
import os

SCHEMA_DIR = 'Schemas'
DATA_DIR = 'Data'

"""
Validate a file against a JADN schema
"""
def validate(file: str = 'container.json', schema: str = 'container.jidl') -> None:
    filename, ext = os.path.splitext(file)
    with open(os.path.join(SCHEMA_DIR, schema), encoding='utf-8') as fp:
        sc = jadn.load_any(fp)
    codec = jadn.codec.Codec(sc, verbose_rec=True, verbose_str=True)
    item_type = sc['info']['exports'][0]
    with open(os.path.join(DATA_DIR, file), encoding='utf-8') as fp:
        data = json.load(fp)
    print(f'{item_type}: {len(data)}')
    try:
        codec.decode(item_type, data)
    except ValueError as e:
        print(f' Error: {e}')

if __name__ == '__main__':
    try:
        fire.Fire(validate)
    except FileNotFoundError as e:
        print(e)