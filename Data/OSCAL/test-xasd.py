"""
Translate each schema file in Source directory to multiple formats in Out directory
"""
import fire
import jadn
import os
import xasd

SCHEMA_DIR = '../../Schemas/JADN'
OUTPUT_DIR = 'Out'


def translate(filename: str, sdir: str, odir: str) -> None:
    if not os.path.isfile(p := os.path.join(sdir, filename)):
        return
    with open(p, encoding='utf8') as fp:
        schema = jadn.load_any(fp)
    print(f'{filename}:\n' + '\n'.join([f'{k:>15}: {v}' for k, v in jadn.analyze(jadn.check(schema)).items()]))

    fn, ext = os.path.splitext(filename)
    xasd.xasd_dump(schema, os.path.join(odir, fn + '.xml'))


def main(schema_dir: str = SCHEMA_DIR, output_dir: str = OUTPUT_DIR) -> None:
    print(f'Installed JADN version: {jadn.__version__}\n')
    os.makedirs(output_dir, exist_ok=True)
    for f in os.listdir(schema_dir):
        if os.path.splitext(f)[1] == '.jadn':
            try:
                translate(f, schema_dir, output_dir)
            except (ValueError, IndexError) as e:
                print(f'### {f}: {e}')
                raise


if __name__ == '__main__':
    fire.Fire(main)
