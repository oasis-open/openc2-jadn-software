from collections import defaultdict
from urllib.request import urlopen, Request
import json
from jsonschema import validate, draft7_format_checker
from jsonschema.exceptions import ValidationError
import os

"""
Validate OpenC2 commands and responses for profiles stored on GitHub under "base"
Environment variable "GitHubToken" must have a Personal Access Token to prevent rate limiting

/base
|-- profile-A
|   |-- schema-A.json
|   |-- Good-command
|   |   |-- command.json
|   |   |-- command.json
|   |-- Bad-command
|   |   |-- command.json
|   |-- Good-response
|   |   |-- response.json
|   |-- Bad-response
|   |   |-- response.json
|-- profile-B
|   |-- schema-B.json
     ...
"""

ROOT_DIR = 'Test'
ROOT_REPO = 'https://api.github.com/repos/oasis-tcs/openc2-usecases/contents/Actuator-Profile-Schemas/'
TEST_ROOT = ROOT_DIR           # Select root of device test tree

AUTH = {'Authorization': f'token {os.environ["GitHubToken"]}'}
# auth = {}


class WebDirEntry:
    """
    Fake os.DirEntry type for GitHub filesystem
    """
    def __init__(self, name, path, url):
        self.name = name
        self.path = path
        self.url = url


def list_dir(dirpath: str) -> dict:
    """
    Return a dict listing the files and directories in a directory on local filesystem or GitHub repo.

    :param dirpath: str - a filesystem path or GitHub API URL
    :return: dict {files: [DirEntry*], dirs: [DirEntry*]}
    Local Filesystem: Each list item is an os.DirEntry structure containing name and path attributes
    GitHub Filesystem: Each list item has name, path, and url (download URL) attributes
    """

    files, dirs = [], []
    if dirpath.startswith('https://'):
        with urlopen(Request(dirpath, headers=AUTH)) as d:
            for dl in json.loads(d.read().decode()):
                url = 'url' if dl['type'] == 'dir' else 'download_url'
                entry = WebDirEntry(dl['name'], dl[url], dl['url'])
                (dirs if dl['type'] == 'dir' else files).append(entry)
    else:
        with os.scandir(dirpath) as dlist:
            for entry in dlist:
                (dirs if os.path.isdir(entry) else files).append(entry)
    return {'files': files, 'dirs': dirs}


def read_file(filepath: str) -> str:
    if filepath.startswith('https://'):
        with urlopen(Request(filepath, headers=AUTH)) as fp:
            doc = fp.read().decode()
    else:
        with open(filepath) as fp:
            doc = fp.read()
    return doc

"""
def gh_get(url):            # Read contents from GitHub API
    with urlopen(Request(url, headers=auth)) as e:
        entry = json.loads(e.read().decode())
    return entry
"""


def find_tests(dirpath):    # Search for GitHub folders containing schemas and test data
    def _ft(dpath, tests):    # Internal recursive search
        dl = list_dir(dpath)
        if 'Good-command' in {d.name for d in dl['dirs']}:      # Directory name indicates test data
            tests.append(dpath)
        else:
            for dp in dl['dirs']:
                _ft(dp.path, tests)

    test_list = []          # Initialize, build test list, and return it
    _ft(dirpath, test_list)
    return test_list


def run_test(dpath):         # Check correct validation of good and bad commands and responses
    dl = list_dir(dpath)
    json_files = [f for f in dl['files'] if os.path.splitext(f.name)[1] == '.json']
    if len(json_files) != 1:  # Must have exactly one .json file
        print(f'Err: {len(json_files)} .json files in', dpath)
        return

    json_schema = json.loads(read_file(json_files[0].path))
    # json_schema = gh_get(tdir['schema'])
    print(f'\nSchema: {json_files[0].path}\nNamespace: {json_schema["$id"]}')
    tcount = defaultdict(int)       # Total instances tested
    ecount = defaultdict(int)       # Error instances
    for cr in ('command', 'response'):
        for gb in ('Good', 'Bad'):
            pdir = f'{gb}-{cr}'
            if pdir in tdir['dirs']:
                print(pdir)
                fdir = gh_get(tdir['dirs'][pdir])
                files = {e['name']: e['download_url'] for e in fdir if e['type'] == 'file'}
                for n, (fn, url) in enumerate(files.items(), start=1):
                    print(f'{n:>4} {fn:<50}', end='')
                    try:
                        instance = {'openc2_' + cr: gh_get(url)}  # Read message, wrap it as command or response
                        validate(instance, json_schema, format_checker=draft7_format_checker)
                        tcount[pdir] += 1
                        ecount[pdir] += 1 if gb == 'Bad' else 0
                        print()
                    except ValidationError as e:
                        tcount[pdir] += 1
                        ecount[pdir] += 1 if gb == 'Good' else 0
                        print(f' Fail: {e.message}')
                    except json.decoder.JSONDecodeError as e:
                        print(f' Bad JSON: {e.msg} "{e.doc}"')
            else:
                print(pdir, 'No tests')
    print('\nValidation Errors:', {k: str(dict(ecount)[k]) + '/' + str(dict(tcount)[k]) for k in tcount})


print(f'Test Data: {TEST_ROOT}, Auth: {AUTH["Authorization"][-4:]}')
for test in find_tests(TEST_ROOT):
    run_test(test)