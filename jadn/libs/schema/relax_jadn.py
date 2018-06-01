import json
import re

from datetime import datetime

from bs4 import BeautifulSoup, Comment

from ..codec.codec_utils import opts_d2s
from ..utils import toStr


class Relax2Jadn(object):
    def __init__(self, relax):
        if type(relax) is str:
            relax = relax.replace('\n', '')
            relax = re.sub(r'>\s*?<', '><', relax)
            self.schema = BeautifulSoup(relax, 'lxml')

        else:
            raise TypeError('Relax-NG improperly formatted')

    def jadn_dump(self):
        jadn = {
            'meta': self.makeMeta(),
            'types': self.makeTypes()
        }

        return json.dumps(jadn, indent=2)

    def makeMeta(self):
        meta = {}

        for m in self.schema .find_all(string=lambda text: isinstance(text, Comment)):
            m = re.sub(r'(^\s|\s$)', '', m)
            if m.startswith('meta:'):
                m = re.sub('meta:\s?', '', m)
                k, v = m.split(' - ')

                try:
                    v = json.loads(v)
                except Exception as e:
                    v = re.sub(r'(^\s?|\s?$)', '', v)
                meta[k] = v

        return meta

    def makeTypes(self):
        types = []

        for t in self.schema.find_all('define'):
            tmp_type = [t['name']]
            f_child = next(t.children)
            if isinstance(f_child, Comment):
                com = re.sub(r'(^\s?|\s?$)', '', f_child.string)
                com = re.sub(r'\s?#jadn_opts:\{.*?\}+', '', com)

                opts = re.sub(r'.*?#jadn_opts:\s?(?P<opts>\{.*?\}+)', '\g<opts>', f_child.string)

                print('-{}- -{}-'.format(com, opts))
            else:
                pass

            types.append(tmp_type)

        return types


def relax2jadn_dumps(relax):
    """
    Produce jadn schema from relax schema
    :arg relax: JADN Schema to convert
    :type relax: str
    :return: jadn schema
    :rtype str
    """
    return Relax2Jadn(relax).jadn_dump()


def relax2jadn_dump(relax, fname, source=""):
    with open(fname, "w") as f:
        if source:
            f.write("-- Generated from " + source + ", " + datetime.ctime(datetime.now()) + "\n\n")
        f.write(relax2jadn_dumps(relax))
