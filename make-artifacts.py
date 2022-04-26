"""
Translate each schema file in Source directory to multiple formats in Out directory
"""
import fire
import jadn
import os
import shutil
from typing import NoReturn

SCHEMA_DIR = 'Schemas'
OUTPUT_DIR = 'Out'


def translate(filename: str, sdir: str, odir: str) -> NoReturn:
    with open(os.path.join(sdir, filename)) as fp:
        schema = jadn.load_any(fp)
    print(f'{filename}:\n' + '\n'.join([f'{k:>15}: {v}' for k, v in jadn.analyze(jadn.check(schema)).items()]))

    fn, ext = os.path.splitext(filename)
    jadn.dump(schema, os.path.join(odir, fn + '.jadn'))
    jadn.dump(jadn.transform.unfold_extensions(jadn.transform.strip_comments(schema)),
              os.path.join(odir, fn + '-core.jadn'))
    jadn.convert.dot_dump(schema, os.path.join(odir, fn + '.dot'), style={'links': True})
    jadn.convert.plant_dump(schema, os.path.join(odir, fn + '.puml'), style={'links': True, 'detail': 'information'})
    jadn.convert.jidl_dump(schema, os.path.join(odir, fn + '.jidl'), style={'desc': 50})
    jadn.convert.html_dump(schema, os.path.join(odir, fn + '.html'))
    jadn.convert.markdown_dump(schema, os.path.join(odir, fn + '.md'))
    jadn.translate.json_schema_dump(schema, os.path.join(odir, fn + '.json'))


def main(schema_dir: str = SCHEMA_DIR, output_dir: str = OUTPUT_DIR) -> None:
    print(f'Installed JADN version: {jadn.__version__}\n')
    css_dir = os.path.join(output_dir, 'css')
    os.makedirs(css_dir, exist_ok=True)
    shutil.copy(os.path.join(jadn.data_dir(), 'dtheme.css'), css_dir)
    for f in os.listdir(schema_dir):
        translate(f, schema_dir, output_dir)


if __name__ == '__main__':
    fire.Fire(main)
