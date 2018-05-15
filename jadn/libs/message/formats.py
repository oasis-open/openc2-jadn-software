from enum import Enum


class OpenC2MessageFormats(Enum):
    __order__ = 'JSON CBOR ProtoBuf XML'
    JSON = 'json'
    CBOR = 'cbor'
    ProtoBuf = 'proto'
    XML = 'xml'

    @staticmethod
    def list(val=False):
        """
        Structure the message format types as a list
        :return: List of types
        :rtype: list
        """
        tmp = []
        for f in dir(OpenC2MessageFormats):
            if not f.startswith(('_', 'dict', 'list')):
                if val:
                   tmp.append(getattr(OpenC2MessageFormats, f))
                else:
                    tmp.append(f)

        return tmp

    @staticmethod
    def dict(valKey=False):
        """
        Structure the message format types names and values as a dictionary
        :param valKey: bool for use of the name or value as hte key
        :return:
        """
        tmp = {}
        for f in dir(OpenC2MessageFormats):
            if not f.startswith(('_', 'dict', 'list')):
                if valKey:
                    tmp[getattr(OpenC2MessageFormats, f)] = f
                else:
                    tmp[f] = getattr(OpenC2MessageFormats, f)

        return tmp
