"""
Translate JADN to HTML property tables
"""

from __future__ import unicode_literals
from ..codec.jadn_defs import *
from ..codec.codec_utils import topts_s2d, fopts_s2d, cardinality
from datetime import datetime

def thead(td, headers, cls):
    assert len(headers) == len(cls)
    tc = '<caption>' + (td[TNAME] + ' (' + td[TTYPE]) + ')</caption>' if td else ''
    rc = zip(headers, cls)
    return  '<table>' + tc + '<thead>' + ''.join(['<th class="' + c[1] + '">' + c[0] + '</th>' for c in rc]) + '</thead>\n'

def trow(row, cls):
    assert len(row) == len(cls)
    rc = zip(row, cls)
    return '<tr>' + ''.join(['<td class="' + c[1] + '">' + c[0] + '</td>' for c in rc]) + '</tr>\n'

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
    sec = '3.2'
    sec2 = '3.3'
    text += '<h2>' + sec + ' Structure Types</h2>\n'
    for td in jadn['types']:
        if td[TTYPE] in STRUCTURE_TYPES:
            text += '<h3>' + sec + '.' + str(n) + ' ' + td[TNAME] + '</h3>\n'
            text += td[TDESC] + '\n'
            to = topts_s2d(td[TOPTS])
            if to:
                text += '<div class="topts">' + str(to) + '</div>\n'  # have a look
            if td[TTYPE] == 'ArraryOf':
                text += '(arrayof definition)\n'
                text += '<table>'       # TODO: fix
            elif td[TTYPE] == 'Enumerated':
                if 'compact' in topts_s2d(td[TOPTS]):
                    cls = ['n', 's']
                    text += thead(td, ['Value', 'Description'], cls)
                    for fd in td[FIELDS]:
                        name = fd[FNAME] + ' / ' if fd[FNAME] else ''
                        text += trow([str(fd[FTAG]), name + fd[EDESC]], cls)
                else:
                    cls = ['n', 's', 's']
                    text += thead(td, ['ID', 'Name', 'Description'], cls)
                    for fd in td[FIELDS]:
                        text += trow([str(fd[FTAG]), fd[FNAME], fd[EDESC]], cls)
            elif td[TTYPE] == 'Choice':            # same as above but without cardinality column
                cls = ['n', 's', 's', 's']
                text += thead(td, ['ID', 'Name', 'Type', 'Description'], cls)
                for fd in td[FIELDS]:
                    text += trow([str(fd[FTAG]), fd[FNAME], fd[FTYPE], fd[FDESC]], cls)
            else:
                cls = ['n', 's', 's', 'n', 's']
                text += thead(td, ['ID', 'Name', 'Type', '#', 'Description'], cls)
                for fd in td[FIELDS]:
                    fo = {'min': 1, 'max': 1}
                    fo.update(fopts_s2d(fd[FOPTS]))
                    text += trow([str(fd[FTAG]), fd[FNAME], fd[FTYPE], cardinality(fo['min'], fo['max']), fd[FDESC]], cls)
            n += 1
            text += '</table>\n'

    text += '<h2>' + sec2 + ' Primitive Types</h2>\n'
    cls = ['s', 's', 's']
    text += thead(None, ['Name', 'Type', 'Description'], cls)
    for td in jadn['types']:                    # 0:type name, 1:base type, 2:type opts, 3:type desc, 4:fields
        if td[TTYPE] in PRIMITIVE_TYPES:
            to = topts_s2d(td[TOPTS])
            rng = ''            # TODO: format min-max into string length or number range
            fmt = ' (' + to['format'] + ')' if 'format' in to else ''
            text += trow([td[TNAME], td[TTYPE] + rng + fmt, td[TDESC]], cls)
    text += '</table></body>\n'

    return text


def html_dump(jadn, fname, source=''):
    with open(fname, 'w') as f:
        if source:
            f.write('<!-- Generated from ' + source + ', ' + datetime.ctime(datetime.now()) + '-->\n')
        f.write(html_dumps(jadn))
