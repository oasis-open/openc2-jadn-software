"""
Create an SPDXv3 TransferUnit (document) from a set of element files
"""
import fire
import jadn
import json
import os

SCHEMA = 'Schemas/spdx-v3.jidl'
DATA_DIR = 'Data/SPDX-3.0/TransferUnit'
OUTPUT_DIR = 'Out'


def load_element(fn: str, codec: jadn.codec.Codec) -> dict:
    with os.open(fn) as fp:
        return codec.decode('Element', json.load(fp))


class TransferUnit():
    def __init__(self,
                 schema: str = SCHEMA,
                 data_dir: str = DATA_DIR,
                 output_dir: str = OUTPUT_DIR,
                 namespace: str = ''):

        with open(schema) as fp:
            schema = jadn.load_any(fp)
        self.codec = jadn.codec.Codec(schema, verbose_rec=True, verbose_str=True)
        os.makedirs(output_dir, exist_ok=True)

        self.elements = {}
        for path in os.scandir(data_dir):
            if path.is_file() and os.path.splitext(path)[1] == '.json':
                print(path)
                with open(path) as fp:
                    element = self.codec.decode('Element', json.load(fp))
                self.elements.update(element)


if __name__ == '__main__':
    print(f'Installed JADN version: {jadn.__version__}\n')

    tu = TransferUnit()
    fire.Fire(tu)
