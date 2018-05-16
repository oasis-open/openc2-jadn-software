import collections
import cbor2
import json
import os
import xmltodict

from ..enums import OpenC2MessageFormats
from ..utils import Utils


def OpenC2MessageLoader(msg='', msgType=OpenC2MessageFormats.JSON):
    load = {
        'json': load_json,
        'cbor': load_cbor,
        'proto': load_protobuf,
        'xml': load_xml
    }
    if msgType in OpenC2MessageFormats.values():
        return load.get(msgType, load['json'])(msg)
    else:
        raise ValueError("Message Type is not a Valid OpenC2 Message Format")


def load_json(m):
    """
    :param m: JSON Encoded message
    :type m: str or dict
    :raise SyntaxError: Malformed JSON encoded message
    :raise ValueError: Malformed JSON encoded message
    """
    if os.path.isfile(m):
        try:
            with open(m, 'rb') as f:
                rtn = json.load(f)
        except (SyntaxError, ValueError) as e:
            raise e

    elif type(m) == str:
        try:
            rtn = json.loads(m)
        except (SyntaxError, ValueError) as e:
            raise e

    elif type(m) == dict:
        rtn = m

    else:
        raise Exception('Cannot load json, improperly formatted')

    return rtn


def load_cbor(m):
    """
    :param m: CBOR Encoded message
    :type m: hex encoded string (each character is a two digit hex value)
    :raise SyntaxError: Malformed CBOR encoded message
    :raise ValueError: Malformed CBOR encoded message
    :raise cbor2.decoder.CBORDecodeError: Malformed CBOR encoded message
    """
    if os.path.isfile(m):
        try:
            with open(m, 'rb') as f:
                rtn = cbor2.load(f)
        except (SyntaxError, ValueError, cbor2.decoder.CBORDecodeError) as e:
            raise e

    elif type(m) == str:
        try:
            rtn = cbor2.loads(m)
            if type(rtn) is not dict:
                rtn = cbor2.loads(''.join([m[i:i + 2].decode('hex') for i in range(0, len(m), 2)]))
        except (SyntaxError, ValueError, cbor2.decoder.CBORDecodeError) as e:
            raise e
    else:
        raise Exception('Cannot load cbor, improperly formatted')

    return Utils.defaultEncode(rtn)


def load_protobuf(m):
    """
    :param m: ProtoBuf Encoded message
    :type m: str ??
    """
    if os.path.isfile(m):
        if os.path.isfile(m):
            with open(m, 'rb') as f:
                pass
                # TODO: Convert ProtoBuf data to dict
                # rtn = f.read()
                rtn = {}
    elif type(m) == str:
        rtn = {}

    else:
        raise Exception('Cannot load protobuf, improperly formatted')

    return rtn


def load_xml(m):
    """
    :parammg: XML Encoded message
    :type m: str
    """
    def _xml_to_dict(xml):
        tmp = {}

        for t in xml:
            if type(xml[t]) == collections.OrderedDict:
                tmp[t] = _xml_to_dict(xml[t])
            else:
                tmp[t[1:] if t.startswith("@") else t] = xml[t]

        return tmp

    if os.path.isfile(m):
        with open(m, 'rb') as f:
            return _xml_to_dict(xmltodict.parse(f.read()))['message']

    elif type(m) == str:
        return _xml_to_dict(xmltodict.parse(m))['message']

    else:
        raise Exception('Cannot load xml, improperly formatted')
