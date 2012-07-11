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


## Multicall support
#


class _MultiCallMethod:
    # some lesser magic to store calls made to a MultiCall object
    # for batch execution
    def __init__(self, call_list, name):
        self.__call_list = call_list
        self.__name = name

    def __getattr__(self, name):
        return _MultiCallMethod(self.__call_list, "%s.%s" % (self.__name, name))

    def __call__(self, *args):
        self.__call_list.append((self.__name, args))


class MultiCallIterator:
    """Iterates over the results of a multicall. Exceptions are
    thrown in response to xmlrpc faults."""

    def __init__(self, results):
        self.results = results

    def __getitem__(self, i):
        item = self.results[i]
        if type(item) == type({}):
            raise Fault(item['faultCode'], item['faultString'])
        elif type(item) == type([]):
            return item[0]
        else:
            raise ValueError("unexpected type in multicall result")


class MultiCall:
    """server -> a object used to boxcar method calls

    server should be a ServerProxy object.

    Methods can be added to the MultiCall using normal
    method call syntax e.g.:

    multicall = MultiCall(server_proxy)
    multicall.add(2,3)
    multicall.get_address("Guido")

    To execute the multicall, call the MultiCall object e.g.:

    add_result, address = multicall()
    """

    def __init__(self, server):
        self.__server = server
        self.__call_list = []

    def __repr__(self):
        return "<MultiCall at %x>" % id(self)

    __str__ = __repr__

    def __getattr__(self, name):
        return _MultiCallMethod(self.__call_list, name)

    def __call__(self):
        marshalled_list = []
        for name, args in self.__call_list:
            marshalled_list.append({'methodName': name, 'params': args})

        return MultiCallIterator(self.__server.system.multicall(marshalled_list))


class Method(object):
    # some magic to bind an XML-RPC method to an RPC server.
    # supports "nested" methods (e.g. examples.getStateName)

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
        self._session = requests.session(headers=headers)

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
