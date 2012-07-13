from __future__ import absolute_import
from __future__ import division

import base64

import requests

from .exceptions import ProtocolError, ResponseError, Fault
from .serializer import Serializer

from .compat import UnicodeMixin, bytes, str


##
# Wrapper for binary data.  This can be used to transport any kind
# of binary data over XML-RPC, using BASE64 encoding.
#
# @param data An 8-bit string containing arbitrary data.


class Binary:
    """Wrapper for binary data."""

    def __init__(self, data=None):
        if data is None:
            data = b""
        else:
            if not isinstance(data, bytes):
                raise TypeError("expected bytes, not %s" %
                                data.__class__.__name__)
            data = bytes(data)  # Make a copy of the bytes!
        self.data = data

    ##
    # Get buffer contents.
    #
    # @return Buffer contents, as an 8-bit string.

    def __str__(self):
        return str(self.data, "latin-1")  # XXX encoding?!

    def __eq__(self, other):
        if isinstance(other, Binary):
            other = other.data
        return self.data == other

    def __ne__(self, other):
        if isinstance(other, Binary):
            other = other.data
        return self.data != other

    def decode(self, data):
        self.data = base64.decodebytes(data)

    def encode(self, out):
        out.write("<value><base64>\n")
        encoded = base64.encodebytes(self.data)
        out.write(encoded.decode('ascii'))
        out.write('\n')
        out.write("</base64></value>\n")


def _binary(data):
    # decode xml element contents into a Binary structure
    value = Binary()
    value.decode(data)
    return value

WRAPPERS = (Binary,)


class Method(object):

    def __init__(self, send, name):
        self._send = send
        self._name = name

    def __getattr__(self, item):
        if item.startswith("_"):
            raise AttributeError(item)

        return Method(self._send, "%s.%s" % (self._name, item))

    def __call__(self, *args):
        return self._send(self._name, args)


class Client(UnicodeMixin, object):

    def __init__(self, uri, session=None, encoding=None, allow_none=False, *args, **kwargs):
        super(Client, self).__init__(*args, **kwargs)

        headers = {"Content-Type": "text/xml", "Accept": "text/xml"}

        self._uri = uri

        if session is None:
            self._session = requests.session(headers=headers)
        else:
            # Merge the sessions together
            attrs = {}

            for attr in requests.Session.__attrs__:
                if attr == "headers":
                    headers.update(getattr(session, attr, {}))

                    attrs[attr] = headers
                else:
                    attrs[attr] = getattr(session, attr)

            self._session = requests.session(**attrs)

        self._allow_none = allow_none
        self._encoding = encoding if encoding is not None else "utf-8"

    def __getattr__(self, item):
        if item.startswith("_"):
            raise AttributeError(item)

        return Method(self._request, item)

    def __unicode__(self):
        return "<Client (%s)>" % self._uri

    def __repr__(self):
        return self.__str__()

    def _request(self, method, params):
        body = self._dumps(method, params).encode(self._encoding)

        response = self._session.post(self._uri, body)
        response.raise_for_status()

        result = self._loads(response.text.encode("utf-8"))

        if len(result) == 1:
            result = result[0]

        return result

    def _dumps(self, method, arguments):
        s = Serializer(encoding=self._encoding, allow_none=self._allow_none)
        return s.dumps(method, arguments)

    def _loads(self, data):
        s = Serializer(encoding=self._encoding, allow_none=self._allow_none)
        return s.loads(data)
