"""
Translate JADN to HTML property tables
"""

from __future__ import unicode_literals
from ..codec.jadn_defs import *
from ..codec.codec_utils import topts_s2d, fopts_s2d, cardinality
from datetime import datetime

#--------- Markdown ouput -----------------


def doc_begin_m(title):
    text = '## Schema\n'
    return text


def doc_end_m():
    return ''


def sect_m(num, name):
    return len(num)*'#' + '.'.join([str(n) for n in num]) + ' ' + name + '\n'


def meta_begin_m():
    return ' .  | .\n ---:|:---\n'


def meta_item_m(h, val):
    if h == "exports":
        sval = ', '.join(val)
    elif h == 'imports':
        sval = ' '.join(['**' + i[0] + '**:&nbsp;' + i[1] for i in val])
    else:
        sval = val
    return h + ': |' + sval + '\n'


def meta_end_m():
    return ''


def type_begin_m(tname, ttype, topts, headers, cls):
    assert len(headers) == len(cls)
    ch = {'n': '---:', 'h': '---:', 's': ':---'}
    clh = [ch[c] if c in ch else '---' for c in cls]
    tc = '\n**' + (tname + ' (' + ttype) + topts + ')' + '**' if tname else ''
    return tc + '\n\n' + '|'.join(headers) + '\n' + '|'.join(clh) + '\n'


def type_item_m(row, cls):
    assert len(row) == len(cls)
    return '|'.join(row) + '\n'


def type_end_m():
    return ''


# ---------- HTML output ------------------


def doc_begin_h(title):
    text = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n'
    text += '<link rel="stylesheet" type="text/css" href="theme.css">\n'
    text += '<title>' + title + '</title>\n</head>\n'
    text += '<body>\n<h2>Schema</h2>\n'
    return text


def doc_end_h():
    return '</body>\n'


def sect_h(num, name):
    hn = 'h' + str(len(num))
    return '\n<' + hn + '>' + '.'.join([str(n) for n in num]) + ' ' + name + '</' + hn + '>\n'


def meta_begin_h():
    return '<table>\n'


def meta_item_h(h, val):
    if h == "exports":
        sval = ', '.join(val)
    elif h == 'imports':
        sval = ' '.join(['**' + i[0] + '**:&nbsp;' + i[1] for i in val])
    else:
        sval = val
    rc = [[h + ':', 'h'], [sval, 's']]
    return '<tr>' + ''.join(['<td class="' + c[1] + '">' + c[0] + '</td>' for c in rc]) + '</tr>\n'


def meta_imps_h(imports):
    return '<br>\n'.join([i[0] + ': ' + i[1] for i in imports])


def meta_end_h():
    return ''


def type_begin_h(tname, ttype, topts, headers, cls):
    assert len(headers) == len(cls)
    tc = '<caption>' + (tname + ' (' + ttype) + topts + ')' + '</caption>' if tname else ''
    rc = zip(headers, cls)
    return  '<table>' + tc + '<type_begin>' + ''.join(['<th class="' + c[1] + '">' + c[0] + '</th>' for c in rc]) + '</type_begin>\n'


def type_item_h(row, cls):
    assert len(row) == len(cls)
    rc = zip(row, cls)
    return '<tr>' + ''.join(['<td class="' + c[1] + '">' + c[0] + '</td>' for c in rc]) + '</tr>\n'


def type_end_h():
    return  '</table>'


# ---------- JADN Source (JAS) output ------------------


def doc_begin_s(title):
    text = ''
    return text


def doc_end_s():
    return ''


def sect_s(num, name):
    return ''


def meta_begin_s():
    return ''


def meta_item_s(key, val):
    return ''


def meta_end_s():
    return ''


def type_begin_s(tname, ttype, topts, headers, cls):
    assert len(headers) == len(cls)
    return ''


def type_item_s(row, cls):
    assert len(row) == len(cls)
    return ''


def type_end_s():
    return  ''


# ---------- JADN output ------------------


def doc_begin_d(title):
    text = ''
    return text


def doc_end_d():
    return ''


def sect_d(num, name):
    return ''


def meta_begin_d():
    return ''


def meta_item_d(key, val):
    return ''


def meta_end_d():
    return ''


def type_begin_d(tname, ttype, topts, headers, cls):
    assert len(headers) == len(cls)
    return ''


def type_item_d(row, cls):
    assert len(row) == len(cls)
    return ''


def type_end_d():
    return  ''


# ---------- CDDL output ------------------


def doc_begin_c(title):
    text = ''
    return text


def doc_end_c():
    return ''


def sect_c(num, name):
    return ''


def meta_begin_c():
    return ''


def meta_item_c(key, val):
    return ''


def meta_end_c():
    return ''


def type_begin_c(tname, ttype, topts, headers, cls):
    assert len(headers) == len(cls)
    return ''


def type_item_c(row, cls):
    assert len(row) == len(cls)
    return ''


def type_end_c():
    return  ''


# ---------- Thrift output ------------------


def doc_begin_t(title):
    text = ''
    return text


def doc_end_t():
    return ''


def sect_t(num, name):
    return ''


def meta_begin_t():
    return ''


def meta_item_t(key, val):
    return ''


def meta_end_t():
    return ''


def type_begin_t(tname, ttype, topts, headers, cls):
    assert len(headers) == len(cls)
    return ''


def type_item_t(row, cls):
    assert len(row) == len(cls)
    return ''


def type_end_t():
    return  ''


# ---------- JSON Schema output ------------------


def doc_begin_j(title):
    text = ''
    return text


def doc_end_j():
    return ''


def sect_j(num, name):
    return ''


def meta_begin_j():
    return ''


def meta_item_j(key, val):
    return ''


def meta_end_j():
    return ''


def type_begin_j(tname, ttype, topts, headers, cls):
    assert len(headers) == len(cls)
    return ''


def type_item_j(row, cls):
    assert len(row) == len(cls)
    return ''


def type_end_j():
    return  ''


#----------------------------------------------

"""
doc_begin - initial content
doc_end - closing content, if any
sect - section heading for human document formats, nothing for machine-readable schemas
meta_begin - begin meta content
meta_item - most meta items
meta_imps - special handling for imports meta statement
meta_end - close meta content
type_begin - begin type definition
type_item - add field to type definition
type_end - close type definition
"""
# TODO: refactor into base and sub classes to support instance context

wtab = {
    'jas': (doc_begin_s, doc_end_s, sect_s, meta_begin_s, meta_item_s, meta_end_s, type_begin_s, type_item_s, type_end_s),
    'jadn': (doc_begin_d, doc_end_d, sect_d, meta_begin_d, meta_item_d, meta_end_d, type_begin_d, type_item_d, type_end_d),
    'cddl': (doc_begin_c, doc_end_c, sect_c, meta_begin_c, meta_item_c, meta_end_c, type_begin_c, type_item_c, type_end_c),
    'html': (doc_begin_h, doc_end_h, sect_h, meta_begin_h, meta_item_h, meta_end_h, type_begin_h, type_item_h, type_end_h),
    'thrift': (doc_begin_t, doc_end_t, sect_t, meta_begin_t, meta_item_t, meta_end_t, type_begin_t, type_item_t, type_end_t),
    'markdown': (doc_begin_m, doc_end_m, sect_m, meta_begin_m, meta_item_m, meta_end_m, type_begin_m, type_item_m, type_end_m),
    'jsonschema': (doc_begin_j, doc_end_j, sect_j, meta_begin_j, meta_item_j, meta_end_j, type_begin_j, type_item_j, type_end_j)
}

DEFAULT_SECTION = (3, 2)
DEFAULT_FORMAT = 'html'


def base_dumps(jadn, form=DEFAULT_FORMAT, section=DEFAULT_SECTION):
    """
    Translate JADN schema into other formats
    """

    doc_begin, doc_end, sect, meta_begin, meta_item, meta_end, type_begin, type_item, type_end = wtab[form]
    meta = jadn['meta']
    title = meta['module'] + (' v.' + meta['version']) if 'version' in meta else ''
    text = doc_begin(title)
    text += meta_begin()
    meta_list = ['title', 'module', 'version', 'description', 'exports', 'imports', 'bounds']
    for h in meta_list + list(set(meta) - set(meta_list)):
        text += meta_item(h, meta[h]) if h in meta else ''
    text += meta_end()

    sub = 1
    sec = list(section)
    text += sect(sec, 'Structure Types')
    for td in jadn['types']:
        if td[TTYPE] in STRUCTURE_TYPES:
            text += sect(sec + [sub], td[TNAME])
            text += td[TDESC] + '\n'
            to = topts_s2d(td[TOPTS])
            tos = ' ' + str(to) if to else ''
            if td[TTYPE] == 'ArrayOf':            # In STRUCTURE_TYPES but with no field definitions
                tor = set(to) - {'rtype',}
                tos = ' ' + str([str(k) for k in tor]) if tor else ''
                rtype = '.' + to['rtype']
                text += type_begin(td[TNAME], td[TTYPE] + rtype, tos, [], [])
                text += type_end()
            elif td[TTYPE] == 'Enumerated':
                tor = set(to) - {'compact',}
                tos = ' ' + str([str(k) for k in tor]) if tor else ''
                if 'rtype' in to:
                    tt = '.Tag' if 'compact' in to else ''
                    rtype = '.*' + to['rtype']
                    text += type_begin(td[TNAME], td[TTYPE] + tt + rtype, tos, [], [])
                    text += type_end()
                else:
                    if 'compact' in to:
                        cls = ['n', 's']
                        text += type_begin(td[TNAME], td[TTYPE] + '.Tag', tos, ['Value', 'Description'], cls)
                        for fd in td[FIELDS]:
                            name = fd[FNAME] + ' -- ' if fd[FNAME] else ''
                            text += type_item([str(fd[FTAG]), name + fd[EDESC]], cls)
                    else:
                        cls = ['n', 's', 's']
                        text += type_begin(td[TNAME], td[TTYPE], tos, ['ID', 'Name', 'Description'], cls)
                        for fd in td[FIELDS]:
                            text += type_item([str(fd[FTAG]), fd[FNAME], fd[EDESC]], cls)
            elif td[TTYPE] == 'Choice':            # same as above but without cardinality column
                cls = ['n', 's', 's', 's']
                text += type_begin(td[TNAME], td[TTYPE], tos, ['ID', 'Name', 'Type', 'Description'], cls)
                for fd in td[FIELDS]:
                    text += type_item([str(fd[FTAG]), fd[FNAME], fd[FTYPE], fd[FDESC]], cls)
            elif td[TTYPE] == 'Array':
                cls = ['n', 's', 'n', 's']
                text += type_begin(td[TNAME], td[TTYPE], tos, ['ID', 'Type', '#', 'Description'], cls)
                for fd in td[FIELDS]:
                    fo = {'min': 1, 'max': 1}
                    fo.update(fopts_s2d(fd[FOPTS]))
                    fn = '"' + fd[FNAME] + '": ' if fd[FNAME] else ''
                    text += type_item([str(fd[FTAG]), fd[FTYPE], cardinality(fo['min'], fo['max']), fn + fd[FDESC]], cls)
            else:
                cls = ['n', 's', 's', 'n', 's']
                text += type_begin(td[TNAME], td[TTYPE], tos, ['ID', 'Name', 'Type', '#', 'Description'], cls)
                for fd in td[FIELDS]:
                    fo = {'min': 1, 'max': 1}
                    fo.update(fopts_s2d(fd[FOPTS]))
                    text += type_item([str(fd[FTAG]), fd[FNAME], fd[FTYPE], cardinality(fo['min'], fo['max']), fd[FDESC]], cls)
            sub += 1
            text += type_end()

    sec[-1] += 1
    text += sect(sec, 'Primitive Types')
    cls = ['s', 's', 's']
    text += type_begin(None, None, None, ['Name', 'Type', 'Description'], cls)
    for td in jadn['types']:                    # 0:type name, 1:base type, 2:type opts, 3:type desc, 4:fields
        if td[TTYPE] in PRIMITIVE_TYPES:
            to = topts_s2d(td[TOPTS])
            rng = ''            # TODO: format min-max into string length or number range
            fmt = ' (' + to['format'] + ')' if 'format' in to else ''
            text += type_item([td[TNAME], td[TTYPE] + rng + fmt, td[TDESC]], cls)
    text += type_end() + doc_end()

    return text


def base_dump(jadn, fname, source='', form=DEFAULT_FORMAT, section=DEFAULT_SECTION):
    with open(fname, 'w') as f:
        if source:
            f.write('<!-- Generated from ' + source + ', ' + datetime.ctime(datetime.now()) + '-->\n')
        f.write(base_dumps(jadn, form, section))
