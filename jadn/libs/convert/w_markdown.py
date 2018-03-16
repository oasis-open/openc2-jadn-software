"""
Translate JADN to Markdown property tables
"""

from __future__ import unicode_literals
from ..codec.jadn_defs import *
from ..codec.codec_utils import topts_s2d, fopts_s2d, cardinality
from datetime import datetime


def markdown_dumps(jadn):
    """
    Produce property tables in Markdown format from JADN structure
    """

    hdrs = jadn["meta"]
    hdr_list = ["module", "title", "version", "description", "namespace"]
    mdown = '<!--\n'
    for h in list(set(hdrs) - set(hdr_list)):
        mdown += h + ': ' + str(hdrs[h]) + '\n'
    mdown += '-->\n\n'
    if 'title' in hdrs:
        mdown += '# ' + hdrs['title'] + '\n'
    if 'module' in hdrs:
        mdown += '## Module ' + hdrs['module']
        if 'version' in hdrs:
            mdown += ', version ' + hdrs['version']
        mdown += '\n'
    if 'description' in hdrs:
        mdown += hdrs['description'] + '\n'
    if 'namespace' in hdrs:
        mdown += '\nNamespace: ' + hdrs['namespace'] + '\n'

    n = 1
    mdown += '## 3.2 Structure Types\n'
    for td in jadn['types']:
        if td[TTYPE] in STRUCTURE_TYPES:
            mdown += '### 3.2.' + str(n) + ' ' + td[TNAME] + '\n'
            mdown += td[TDESC] + '\n\n'
            mdown += '**Type: ' + td[TTYPE] + '**\n\n'
            to = topts_s2d(td[TOPTS])
            if to:
                mdown += str(to) + '\n\n'  # have a look
        if td[TTYPE] in {k for k in STRUCTURE_TYPES} - {'ArrayOf', 'Choice', 'Enumerated'}:
            mdown += '|ID|Name|Type|#|Description|\n'
            mdown += '|---:|---|---|---:|---|\n'
            for fd in td[FIELDS]:
                mdown += '|' + str(fd[FTAG]) + '|' + fd[FNAME] + '|' + fd[FTYPE]
                fo = {'min': 1, 'max':1}
                fo.update(fopts_s2d(fd[FOPTS]))
                mdown += '|' + cardinality(fo['min'], fo['max'])
                mdown += '|' + fd[FDESC] + '|\n'
            n += 1
        elif td[TTYPE] == 'Choice':            #same as above but without cardinality column
            mdown += '|ID|Name|Type|Description|\n'
            mdown += '|---:|---|---|---|\n'
            for fd in td[FIELDS]:
                mdown += '|' + str(fd[FTAG]) + '|' + fd[FNAME] + '|' + fd[FTYPE]
                mdown += '|' + fd[FDESC] + '|\n'
            n += 1
        elif td[TTYPE] == 'ArraryOf':
            mdown += '(arrayof definition)\n'
            n += 1
        elif td[TTYPE] == 'Enumerated':
            if 'etag' in topts_s2d(td[TOPTS]):
                mdown += '|Value|Description|\n'
                mdown += '|---|---|\n'
                for fd in td[FIELDS]:
                    name = fd[FNAME] + ' / ' if fd[FNAME] else ''
                    mdown += '|' + str(fd[FTAG]) + '|' + name + fd[EDESC] + '|\n'
            else:
                mdown += '|ID|Name|Description|\n'
                mdown += '|---:|---|---|\n'
                for fd in td[FIELDS]:
                    mdown += '|' + str(fd[FTAG]) + '|' + fd[FNAME] + '|' + fd[EDESC] + '|\n'
            n += 1

    mdown += '## 3.3 Primitive Types\n'
    mdown += '|Name|Type|Description|\n'
    mdown += '|---|---|---|\n'
    for td in jadn["types"]:                    # 0:type name, 1:base type, 2:type opts, 3:type desc, 4:fields
        if td[TTYPE] in PRIMITIVE_TYPES:
            to = topts_s2d(td[TOPTS])
            len = ""        # TODO: format min-max into string length or number range
            fmt = " (" + to["format"] + ")" if "format" in to else ""
            mdown += '|' + td[TNAME] + '|' + td[TTYPE] + len + fmt + '|' + td[TDESC] + '|\n'

    return mdown


def markdown_dump(jadn, fname, source=""):
    with open(fname, "w") as f:
        if source:
            f.write('<!-- Generated from ' + source + ', ' + datetime.ctime(datetime.now()) + '-->\n')
        f.write(markdown_dumps(jadn))