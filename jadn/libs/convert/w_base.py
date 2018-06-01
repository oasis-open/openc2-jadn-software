"""
Translate JADN to HTML property tables
"""

from __future__ import unicode_literals
from ..codec.jadn_defs import *
from ..codec.codec_utils import topts_s2d, fopts_s2d, cardinality
from datetime import datetime

#--------- Markdown ouput -----------------


def begin_doc_m(title):
    text = '## Schema\n'
    return text


def end_doc_m():
    return ''


def sect_m(num, name):
    return len(num)*'#' + '.'.join([str(n) for n in num]) + ' ' + name + '\n'


def begin_type_m(tname, ttype, topts, headers, cls):
    assert len(headers) == len(cls)
    tc = '\n**' + (tname + ' (' + ttype) + topts + ')' + '**' if tname else ''
    return tc + '\n\n' + '|'.join(headers) + '\n' + '|'.join(len(cls)*['---']) + '\n'


def trow_m(row, cls):
    assert len(row) == len(cls)
    return '|'.join(row) + '\n'


def imps_m(imports):
    return ' '.join(['**' + i[0] + '**:&nbsp;' + i[1] for i in imports])


def begin_meta_m(cls):
    return '|'.join(len(cls)*[' . ']) + '\n' + '|'.join(len(cls)*['---']) + '\n'


def end_table_m():
    return ''


# ---------- HTML output ------------------


def begin_doc_h(title):
    text = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n'
    text += '<link rel="stylesheet" type="text/css" href="theme.css">\n'
    text += '<title>' + title + '</title>\n</head>\n'
    text += '<body>\n<h2>Schema</h2>\n'
    return text


def end_doc_h():
    return '</body>\n'


def sect_h(num, name):
    hn = 'h' + str(len(num))
    return '\n<' + hn + '>' + '.'.join([str(n) for n in num]) + ' ' + name + '</' + hn + '>\n'


def begin_type_h(tname, ttype, topts, headers, cls):
    assert len(headers) == len(cls)
    tc = '<caption>' + (tname + ' (' + ttype) + topts + ')' + '</caption>' if tname else ''
    rc = zip(headers, cls)
    return  '<table>' + tc + '<begin_type>' + ''.join(['<th class="' + c[1] + '">' + c[0] + '</th>' for c in rc]) + '</begin_type>\n'


def trow_h(row, cls):
    assert len(row) == len(cls)
    rc = zip(row, cls)
    return '<tr>' + ''.join(['<td class="' + c[1] + '">' + c[0] + '</td>' for c in rc]) + '</tr>\n'


def imps_h(imports):
    return '<br>\n'.join([i[0] + ': ' + i[1] for i in imports])


def begin_meta_h(cls):
    return '<table>\n'


def end_table_h():
    return  '</table>'


# ---------- JADN Source (JAS) output ------------------


def begin_doc_s(title):
    text = ''
    return text


def end_doc_s():
    return ''


def sect_s(num, name):
    return ''


def begin_type_s(tname, ttype, topts, headers, cls):
    assert len(headers) == len(cls)
    return ''


def trow_s(row, cls):
    assert len(row) == len(cls)
    return ''


def imps_s(imports):
    return ''


def begin_meta_s(cls):
    return ''


def end_table_s():
    return  ''


# ---------- JADN output ------------------


def begin_doc_d(title):
    text = ''
    return text


def end_doc_d():
    return ''


def sect_d(num, name):
    return ''


def begin_type_d(tname, ttype, topts, headers, cls):
    assert len(headers) == len(cls)
    return ''


def trow_d(row, cls):
    assert len(row) == len(cls)
    return ''


def imps_d(imports):
    return ''


def begin_meta_d(cls):
    return ''


def end_table_d():
    return  ''


# ---------- CDDL output ------------------


def begin_doc_c(title):
    text = ''
    return text


def end_doc_c():
    return ''


def sect_c(num, name):
    return ''


def begin_type_c(tname, ttype, topts, headers, cls):
    assert len(headers) == len(cls)
    return ''


def trow_c(row, cls):
    assert len(row) == len(cls)
    return ''


def imps_c(imports):
    return ''


def begin_meta_c(cls):
    return ''


def end_table_c():
    return  ''


# ---------- Thrift output ------------------


def begin_doc_t(title):
    text = ''
    return text


def end_doc_t():
    return ''


def sect_t(num, name):
    return ''


def begin_type_t(tname, ttype, topts, headers, cls):
    assert len(headers) == len(cls)
    return ''


def trow_t(row, cls):
    assert len(row) == len(cls)
    return ''


def imps_t(imports):
    return ''


def begin_meta_t(cls):
    return ''


def end_table_t():
    return  ''


# ---------- JSON Schema output ------------------


def begin_doc_j(title):
    text = ''
    return text


def end_doc_j():
    return ''


def sect_j(num, name):
    return ''


def begin_type_j(tname, ttype, topts, headers, cls):
    assert len(headers) == len(cls)
    return ''


def trow_j(row, cls):
    assert len(row) == len(cls)
    return ''


def imps_j(imports):
    return ''


def begin_meta_j(cls):
    return ''


def end_table_j():
    return  ''


#----------------------------------------------

"""
begin_doc - initial content
end_doc - final closing content, if any
sect - section heading for human document formats, nothing for machine-readable schemas
begin_meta - begin meta content
begin_type - begin type definition
trow - add field to type definition or most meta items
imps - special handling for imports meta statement
end_table - close meta section or type definition
"""
# TODO: refactor into base and sub classes to support instance context

wtab = {
    'jas': (begin_doc_s, end_doc_s, sect_s, begin_type_s, trow_s, imps_s, begin_meta_s, end_table_s),
    'jadn': (begin_doc_d, end_doc_d, sect_d, begin_type_d, trow_d, imps_d, begin_meta_d, end_table_d),
    'cddl': (begin_doc_c, end_doc_c, sect_c, begin_type_c, trow_c, imps_c, begin_meta_c, end_table_c),
    'html': (begin_doc_h, end_doc_h, sect_h, begin_type_h, trow_h, imps_h, begin_meta_h, end_table_h),
    'thrift': (begin_doc_t, end_doc_t, sect_t, begin_type_t, trow_t, imps_t, begin_meta_t, end_table_t),
    'markdown': (begin_doc_m, end_doc_m, sect_m, begin_type_m, trow_m, imps_m, begin_meta_m, end_table_m),
    'jsonschema': (begin_doc_j, end_doc_j, sect_j, begin_type_j, trow_j, imps_j, begin_meta_j, end_table_j)
}

DEFAULT_SECTION = (3, 2)
DEFAULT_FORMAT = 'html'


def base_dumps(jadn, form=DEFAULT_FORMAT, section=DEFAULT_SECTION):
    """
    Translate JADN schema into other formats
    """

    assert form in wtab
    begin_doc, end_doc, sect, begin_type, trow, format_imp, begin_meta, end_table = wtab[form]
    meta = jadn['meta']
    title = meta['module'] + (' v.' + meta['version']) if 'version' in meta else ''
    text = begin_doc(title)
    cls = ['h', 's']
    text += begin_meta(cls)
    meta_list = ['title', 'module', 'version', 'description', 'exports', 'imports', 'bounds']
    for h in meta_list + list(set(meta) - set(meta_list)):
        if h in meta:
            if h == "exports":
                text += trow([h + ': ', ', '.join(meta[h])], cls)
            elif h == 'imports':
                text += trow([h + ': ', format_imp(meta[h])], cls)
            else:
                text += trow([h + ': ', meta[h]], cls)
    text += end_table()

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
                text += begin_type(td[TNAME], td[TTYPE] + rtype, tos, [], [])
                text += end_table()
            elif td[TTYPE] == 'Enumerated':
                tor = set(to) - {'compact',}
                tos = ' ' + str([str(k) for k in tor]) if tor else ''
                if 'rtype' in to:
                    tt = '.Tag' if 'compact' in to else ''
                    rtype = '.*' + to['rtype']
                    text += begin_type(td[TNAME], td[TTYPE] + tt + rtype, tos, [], [])
                    text += end_table()
                else:
                    if 'compact' in to:
                        cls = ['n', 's']
                        text += begin_type(td[TNAME], td[TTYPE] + '.Tag', tos, ['Value', 'Description'], cls)
                        for fd in td[FIELDS]:
                            name = fd[FNAME] + ' -- ' if fd[FNAME] else ''
                            text += trow([str(fd[FTAG]), name + fd[EDESC]], cls)
                    else:
                        cls = ['n', 's', 's']
                        text += begin_type(td[TNAME], td[TTYPE], tos, ['ID', 'Name', 'Description'], cls)
                        for fd in td[FIELDS]:
                            text += trow([str(fd[FTAG]), fd[FNAME], fd[EDESC]], cls)
            elif td[TTYPE] == 'Choice':            # same as above but without cardinality column
                cls = ['n', 's', 's', 's']
                text += begin_type(td[TNAME], td[TTYPE], tos, ['ID', 'Name', 'Type', 'Description'], cls)
                for fd in td[FIELDS]:
                    text += trow([str(fd[FTAG]), fd[FNAME], fd[FTYPE], fd[FDESC]], cls)
            elif td[TTYPE] == 'Array':
                cls = ['n', 's', 'n', 's']
                text += begin_type(td[TNAME], td[TTYPE], tos, ['ID', 'Type', '#', 'Description'], cls)
                for fd in td[FIELDS]:
                    fo = {'min': 1, 'max': 1}
                    fo.update(fopts_s2d(fd[FOPTS]))
                    fn = '"' + fd[FNAME] + '": ' if fd[FNAME] else ''
                    text += trow([str(fd[FTAG]), fd[FTYPE], cardinality(fo['min'], fo['max']), fn + fd[FDESC]], cls)
            else:
                cls = ['n', 's', 's', 'n', 's']
                text += begin_type(td[TNAME], td[TTYPE], tos, ['ID', 'Name', 'Type', '#', 'Description'], cls)
                for fd in td[FIELDS]:
                    fo = {'min': 1, 'max': 1}
                    fo.update(fopts_s2d(fd[FOPTS]))
                    text += trow([str(fd[FTAG]), fd[FNAME], fd[FTYPE], cardinality(fo['min'], fo['max']), fd[FDESC]], cls)
            sub += 1
            text += end_table()

    sec[-1] += 1
    text += sect(sec, 'Primitive Types')
    cls = ['s', 's', 's']
    text += begin_type(None, None, None, ['Name', 'Type', 'Description'], cls)
    for td in jadn['types']:                    # 0:type name, 1:base type, 2:type opts, 3:type desc, 4:fields
        if td[TTYPE] in PRIMITIVE_TYPES:
            to = topts_s2d(td[TOPTS])
            rng = ''            # TODO: format min-max into string length or number range
            fmt = ' (' + to['format'] + ')' if 'format' in to else ''
            text += trow([td[TNAME], td[TTYPE] + rng + fmt, td[TDESC]], cls)
    text += end_table() + end_doc()

    return text


def base_dump(jadn, fname, source='', form=DEFAULT_FORMAT, section=DEFAULT_SECTION):
    with open(fname, 'w') as f:
        if source:
            f.write('<!-- Generated from ' + source + ', ' + datetime.ctime(datetime.now()) + '-->\n')
        f.write(base_dumps(jadn, form, section))
