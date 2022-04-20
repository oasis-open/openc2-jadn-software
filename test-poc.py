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
TEST_ROOT = ROOT_REPO           # Select root of device test tree

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


def list_dir(dirname: str) -> dict:
    """
    Return a dict listing the files and directories in a directory on local filesystem or GitHub repo.

    :param dirname: str - a filesystem path or GitHub API URL
    :return: dict {files: [DirEntry*], dirs: [DirEntry*]}
    Local Filesystem: Each list item is an os.DirEntry structure containing name and path attributes
    GitHub Filesystem: Each list item has name, path, and url (download URL) attributes
    """

    files, dirs = [], []
    if dirname.startswith('https://'):
        with urlopen(Request(dirname, headers=AUTH)) as d:
            for dl in json.loads(d.read().decode()):
                url = 'url' if dl['type'] == 'dir' else 'download_url'
                entry = WebDirEntry(dl['name'], dl[url], dl['url'])
                (dirs if dl['type'] == 'dir' else files).append(entry)
    else:
        with os.scandir(dirname) as dlist:
            for entry in dlist:
                (dirs if os.path.isdir(entry) else files).append(entry)
    return {'files': files, 'dirs': dirs}


def read_file(path: str) -> str:
    if path.startswith('https://'):
        with urlopen(Request(path, headers=AUTH)) as fp:
            doc = fp.read().decode()
    else:
        with open(path) as fp:
            doc = fp.read()
    return doc


def gh_get(url):            # Read contents from GitHub API
    with urlopen(Request(url, headers=auth)) as e:
        entry = json.loads(e.read().decode())
    return entry


def find_tests(dname):    # Search for GitHub folders containing schemas and test data
    def _ft(url, tests):    # Internal recursive search
        dl = list_dir(dname)
        dirs = {d.name: d.url for d in dl['dirs']}
        if 'Good-command' in dirs:      # Directory name indicates test data
            files = {e['name']: e['download_url'] for e in gdir if e['type'] == 'file'}
            json_url = [u for f, u in files.items() if os.path.splitext(f)[1] == '.json']
            if len(json_url) == 1:      # Must have exactly one .json file
                tests.append({'dirs': dirs, 'files': files, 'schema': json_url[0]})
            else:
                print('No json schema in', url)
        else:
            for child in dirs.values():
                _ft(child, tests)

    test_list = []          # Initialize, build test list, and return it
    _ft(dname, test_list)
    return test_list


def run_test(tdir):         # Check correct validation of good and bad commands and responses
    json_schema = gh_get(tdir['schema'])
    print(f'\nSchema: {tdir["schema"]}\nNamespace: {json_schema["$id"]}')
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