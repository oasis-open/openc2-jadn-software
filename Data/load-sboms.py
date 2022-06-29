import fire
import json
import requests

SBOM_SOURCES = 'sbom-examples.json'

with open(SBOM_SOURCES) as fp:
    sbom_uris = json.load(fp)
print(f'Creating {len(sbom_uris)} SBOMs')
for n, fn in enumerate(sbom_uris, start=1):
    response = requests.get(fn)
    data = response.content.decode()
    print(f'{n:>4} data:', fn, len(data))