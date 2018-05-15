import cbor2

from dicttoxml import dicttoxml
from xml.dom.minidom import parseString

from .load import OpenC2MessageLoader

from ..enums import OpenC2MessageFormats


class OpenC2Message(object):
    """
    Translate a JSON Encoded message to other formats
    """
    def __init__(self, msg='', msgType=OpenC2MessageFormats.JSON):
        """
        :param msg: Dictionary representation of the message
        :type msg: dict
        :raise TypeError: Dictionary not given
        """
        if msgType in OpenC2MessageFormats.values():
            self._msg = OpenC2MessageLoader(msg, msgType)
        else:
            raise ValueError("Message Type is not a Valid OpenC2 Message Format")

    def json_dump(self):
        """
        translate the message to json
        :return: json version of message
        :rtype: dict
        """
        return self._msg

    def protobuf_dump(self):
        """
        translate the message to protobuff
        :return: protobuff version of message
        :rtype: ??
        """
        return self._msg

    def xml_dump(self, pretty=False):
        """
        translate the message to xml
        :param pretty: bool for pretty print
        :return: xml version of message
        :rtype: str
        """
        xml = dicttoxml(self._msg, custom_root='message', attr_type=False)
        if pretty:
            return parseString(xml).toprettyxml()
        else:
            return xml

    def cbor_dump(self):
        """
        translate the message to cbor
        :return: cbor version of message
        :rtype: str
        """
        return ''.join(["\\x{}".format(c.encode('hex')) if ord(c) >= 128 else c for c in cbor2.dumps(self._msg)])