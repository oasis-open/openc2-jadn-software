"""
Translate JADN to HTML property tables
"""

from __future__ import unicode_literals
from ..codec.jadn_defs import *
from ..codec.codec_utils import topts_s2d, fopts_s2d, cardinality
from datetime import datetime

def thead(headers):
    return '<table><thead><tr><th>' + '</th><th>'.join(headers) + '</th></tr></thead>\n'

# def trow(row, cls):
#    return '<tr><td class="tag">' + str(fd[FTAG]) + '</td><td>' + fd[FNAME] + '</td><td class="desc">' + fd[EDESC] + '</td></tr>\n'

def html_dumps(jadn):
    """
    Produce property tables in Markdown format from JADN structure
    """

    text = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n'
    text += '<title>Title</title>\n'
    text += '<link rel="stylesheet" type="text/css" href="theme.css">\n'
    text += '</head>\n<body>\n'

    hdrs = jadn['meta']
    hdr_list = ['module', 'title', 'version', 'description', 'namespace']
    text += '<!--\n'
    for h in list(set(hdrs) - set(hdr_list)):
        text += h + ': ' + str(hdrs[h]) + '\n'
    text += '-->\n\n'
    if 'title' in hdrs:
        text += '<h1>' + hdrs['title'] + '</h1>\n'
    if 'module' in hdrs:
        text += '<h2>Module ' + hdrs['module']
        if 'version' in hdrs:
            text += ', version ' + hdrs['version']
        text += '</h2>\n'
    if 'description' in hdrs:
        text += '<br>' + hdrs['description'] + '\n'
    if 'namespace' in hdrs:
        text += '<br>Namespace: ' + hdrs['namespace'] + '\n'

    n = 1
    text += '<h2>3.2 Structure Types</h2>\n'
    for td in jadn['types']:
        if td[TTYPE] in STRUCTURE_TYPES:
            text += '<h3>3.2.' + str(n) + ' ' + td[TNAME] + '</h3>\n'
            text += td[TDESC] + '\n'
            text += '<div class="type">Type: ' + td[TTYPE] + '</div>\n'
            to = topts_s2d(td[TOPTS])
            if to:
                text += '<div class="topts">' + str(to) + '</div>\n'  # have a look
        if td[TTYPE] in {k for k in STRUCTURE_TYPES} - {'ArrayOf', 'Choice', 'Enumerated'}:
            text += thead(['ID', 'Name', 'Type', '#', 'Description'])
            for fd in td[FIELDS]:
                text += '<tr><td class="tag">' + str(fd[FTAG]) + '</td><td>' + fd[FNAME] + '</td><td>' + fd[FTYPE] + '</td>\n'
                fo = {'min': 1, 'max': 1}
                fo.update(fopts_s2d(fd[FOPTS]))
                text += '<td>' + cardinality(fo['min'], fo['max'])
                text += '</td><td class="desc">' + fd[FDESC] + '</td></tr>\n'
            n += 1
            text += '</table>\n'
        elif td[TTYPE] == 'Choice':            # same as above but without cardinality column
            text += thead(['ID', 'Name', 'Type', 'Description'])
            for fd in td[FIELDS]:
                text += '<tr><td class="tag">' + str(fd[FTAG]) + '</td><td>' + fd[FNAME] + '</td><td>' + fd[FTYPE]
                text += '</td><td class="desc">' + fd[FDESC] + '</td></tr>\n'
            n += 1
            text += '</table>\n'
        elif td[TTYPE] == 'ArraryOf':
            text += '(arrayof definition)\n'
            n += 1
        elif td[TTYPE] == 'Enumerated':
            if 'compact' in topts_s2d(td[TOPTS]):
                text += thead(['Value', 'Description'])
                for fd in td[FIELDS]:
                    name = fd[FNAME] + ' / ' if fd[FNAME] else ''
                    text += '<tr><td class="tag">' + str(fd[FTAG]) + '</td><td class="desc">' + name + fd[EDESC] + '</td></tr>\n'
            else:
                text += thead(['ID', 'Name', 'Description'])
                for fd in td[FIELDS]:
                    text += '<tr><td class="tag">' + str(fd[FTAG]) + '</td><td>' + fd[FNAME] + '</td><td class="desc">' + fd[EDESC] + '</td></tr>\n'
#                    text += trow([str(fd[FTAG]), fd[FNAME], fd[EDESC]])
            n += 1
            text += '</table>\n'

    text += '<h2>3.3 Primitive Types</h2>\n'
    text += thead(['Name', 'Type', 'Description'])
    text += '<table><thead><tr><th>Name</th><th>Type</th><th>Description</th></tr></thead>\n'
    for td in jadn['types']:                    # 0:type name, 1:base type, 2:type opts, 3:type desc, 4:fields
        if td[TTYPE] in PRIMITIVE_TYPES:
            to = topts_s2d(td[TOPTS])
            rng = ''            # TODO: format min-max into string length or number range
            fmt = ' (' + to['format'] + ')' if 'format' in to else ''
            text += '<tr><td>' + td[TNAME] + '</td><td>' + td[TTYPE] + rng + fmt + '</td><td class="desc">' + td[TDESC] + '</td></tr>\n'
    text += '</table><\body>\n'

    return text


def html_dump(jadn, fname, source=''):
    with open(fname, 'w') as f:
        if source:
            f.write('<!-- Generated from ' + source + ', ' + datetime.ctime(datetime.now()) + '-->\n')
        f.write(html_dumps(jadn))
