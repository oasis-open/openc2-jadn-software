"""
Import namespaced type definitions into a base package.

Search all packages in SCHEMA_DIR for referenced definitions, put resolved base file in OUTPUT_DIR.
"""

import fire
import jadn
import os

SCHEMA_DIR = 'Schemas'
OUTPUT_DIR = 'Out'


def resolve(schema: str = 'device-pac-slpf-base.jadn', reference_dir: str = SCHEMA_DIR, output_dir: str = OUTPUT_DIR) -> None:
    print(f'Installed JADN version: {jadn.__version__}\n')
    print(f'{reference_dir}/{schema} -> {output_dir}')
    os.makedirs(output_dir, exist_ok=True)
    filename, ext = os.path.splitext(schema)
    with open(os.path.join(reference_dir, schema), encoding='utf-8') as fp:
        sc = jadn.load_any(fp)                 # Load base package
    sc2 = jadn.transform.resolve_imports(sc, reference_dir, ('ls',))        # Resolve referenced definitions
    jadn.dump(sc2, os.path.join(output_dir, filename + '-resolved.jadn'))   # Save resolved base package
    print(f'{schema}:\n' + '\n'.join([f'{k:>14}: {v}' for k, v in jadn.analyze(jadn.check(sc2)).items()]))


if __name__ == '__main__':
    try:
        fire.Fire(resolve)
    except FileNotFoundError as e:
        print(e)