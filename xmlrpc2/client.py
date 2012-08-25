from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import functools

try:
    import urllib.parse as urllib_parse
except ImportError:
    import urlparse as urllib_parse

from . import requests
from .exceptions import Fault
from .serializer import Serializer


__all__ = ["BaseTransport", "HTTPTransport", "HTTPSTransport", "Client"]


class BaseTransport(object):

    @property
    def scheme(self):
        raise NotImplementedError("Transports must have a scheme")

    def request(self, uri, body):
        raise NotImplementedError("Transports must implement request")


class HTTPTransport(BaseTransport):

    scheme = "http"

    def __init__(self, session=None):
        if session is None:
            session = requests.session()

        # text/xml is a mandatory content type
        session.headers.update({"Content-Type": "text/xml"})

        self.session = session

    def request(self, uri, body):
        resp = self.session.post(uri, body)
        resp.raise_for_status()
        return resp.text


class HTTPSTransport(HTTPTransport):

    scheme = "https"


class Client(object):

    def __init__(self, uri, transports=None, serializer=None):
        if transports is None:
            transports = [HTTPTransport(), HTTPSTransport()]

        if serializer is None:
            serializer = Serializer()

        self._transports = dict([(t.scheme, t) for t in transports])

        parsed = urllib_parse.urlparse(uri)

        if parsed.scheme not in self._transports:
            raise ValueError("Invalid uri scheme {scheme}. Must be one of {available}.".format(scheme=parsed.scheme, available=",".join(self._transports)))

        self._transport = self._transports[parsed.scheme]

        # Default to /RPC2 for path as it is a common endpoint
        if not parsed.path:
            parsed = parsed[:2] + ("/RPC2",) + parsed[3:]

        self._uri = urllib_parse.urlunparse(parsed)

        self._serializer = serializer

    def __call__(self, method, *args):
        data = {
            "methodCall": {
                "methodName": method,
                "params": args,
            }
        }

        body = self._serializer.serialize(data)
        resp = self._transport.request(self._uri, body)
        values = self._serializer.deserialize(resp)

        if "methodResponse" in values:
            values = values["methodResponse"]
        else:
            raise TypeError("Unknown return from xmlrpc call")

        if "params" in values:
            if len(values["params"]) == 1:
                return values["params"][0]
            elif len(values["params"]) > 1:
                return values["params"]

        if "fault" in values:
            raise Fault(values["fault"]["faultString"], code=values["fault"]["faultCode"])

    def __getattr__(self, name):
        return functools.partial(self, name)
