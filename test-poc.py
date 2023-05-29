import jadn
import json
import os
from collections import defaultdict
from io import TextIOWrapper
from typing import TextIO
from urllib.request import urlopen, Request
from urllib.parse import urlparse
from jsonschema import validate, Draft202012Validator
from jsonschema.exceptions import ValidationError

"""
Validate OpenC2 commands and responses for profiles stored in local ROOT_DIR or GitHub under ROOT_REPO
Environment variable "GitHubToken" must have a Personal Access Token to prevent rate limiting

/
|-- device-A
|   |-- device-A-schema.jadn
|   |-- device-A-schema.json
|   |-- Good-command
|   |   |-- command.json
|   |   |-- command.json
|   |-- Bad-command
|   |   |-- command.json
|   |-- Good-response
|   |   |-- response.json
|   |-- Bad-response
|   |   |-- response.json
|-- device-B
|   |-- device-B-schema.jadn
|   |-- device-B-schema.json
     ...
"""

VALIDATE_JADN = True    # Use JAON schema if True, JSON schema if False

ROOT_DIR = 'Test'
ROOT_REPO = 'https://api.github.com/repos/oasis-open/openc2-jadn-software/contents/Test'
TEST_ROOT = ROOT_REPO          # Select local directory or GitHub root of test tree

AUTH = {'Authorization': f'token {os.environ["GitHubToken"] if TEST_ROOT == ROOT_REPO else "None"}'}


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
    u = urlparse(dirpath)
    if all([u.scheme, u.netloc]):
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


def open_file(fileentry: os.DirEntry) -> TextIO:
    u = urlparse(fileentry.path)
    if all([u.scheme, u.netloc]):
        return TextIOWrapper(urlopen(Request(fileentry.path, headers=AUTH)), encoding='utf8')
    return open(fileentry.path, 'r', encoding='utf8')


def find_tests(dirpath):        # Search for folders containing schemas and test data
    def _ft(dpath, tests):      # Internal recursive search
        dl = list_dir(dpath)    # Get local or web directory listing
        if 'Good-command' in {d.name for d in dl['dirs']}:      # Test data directory found
            tests.append(dpath)
        else:
            for dp in dl['dirs']:
                _ft(dp.path, tests)

    test_list = []          # Initialize, build test list, and return it
    _ft(dirpath, test_list)
    return test_list


def run_test(dpath):         # Check correct validation of good and bad commands and responses
    print(f'\n{dpath}:')
    dl = list_dir(dpath)
    try:
        if VALIDATE_JADN:
            schemas = [f for f in dl['files'] if os.path.splitext(f.name)[1] in ('.jadn', '.jidl')]
            with open_file(schemas[0]) as fp:
                codec = jadn.codec.Codec(jadn.load_any(fp), verbose_rec=True, verbose_str=True)
        else:
            schemas = [f for f in dl['files'] if os.path.splitext(f.name)[1] == '.json']
            with open_file(schemas[0]) as fp:
                json_schema = json.load(fp)
    except IndexError:
        print(f'No schemas found in {dpath}')
        return
    except ValueError as e:
        print(e)
        return
    tcount = defaultdict(int)       # Total instances tested
    ecount = defaultdict(int)       # Error instances
    tdirs = {d.name: d for d in dl['dirs']}
    for cr in ('command', 'response'):
        for gb in ('Good', 'Bad'):
            pdir = f'{gb}-{cr}'
            if pdir in tdirs:
                print(f'  {pdir}')
                dl2 = list_dir(tdirs[pdir].path)
                for n, f in enumerate(dl2['files'], start=1):
                    print(f'{n:>6} {f.name:<50}', end='')
                    try:
                        if VALIDATE_JADN:
                            crtype = 'OpenC2-Command' if cr == 'command' else 'OpenC2-Response'
                            codec.decode(crtype, json.load(open_file(f)))
                        else:
                            validate({'openc2_' + cr: json.load(open_file(f))}, json_schema,
                                     format_checker=Draft202012Validator.FORMAT_CHECKER)
                        tcount[pdir] += 1
                        ecount[pdir] += 1 if gb == 'Bad' else 0
                        print()
                    except ValidationError as e:    # JSON Schema validation error
                        tcount[pdir] += 1
                        ecount[pdir] += 1 if gb == 'Good' else 0
                        print(f' Fail: {e.message}')
                    except ValueError as e:         # JADN validation error
                        tcount[pdir] += 1
                        ecount[pdir] += 1 if gb == 'Good' else 0
                        print(f' Fail: {e}')
                    except json.decoder.JSONDecodeError as e:
                        print(f' Bad JSON: {e.msg} "{e.doc}"')
            else:
                print(pdir, 'No tests')
    print(f'Validation Errors: {sum(k for k in ecount.values())}', {k: str(dict(ecount)[k]) + '/' + str(dict(tcount)[k]) for k in tcount})


if __name__ == '__main__':
    print(f'JADN Version: {jadn.__version__}, Test Data: {TEST_ROOT}, Access Token: ..{AUTH["Authorization"][-4:]}')
    for test in find_tests(TEST_ROOT):
        run_test(test)