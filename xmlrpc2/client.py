from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import urllib.parse


class BaseTransport(object):

    @property
    def scheme(self):
        raise NotImplementedError("Transports must have a scheme")


class HTTPTransport(BaseTransport):

    scheme = "http"


class Client(object):

    def __init__(self, uri, transports=None):
        if transports is None:
            transports = [HTTPTransport]

        # Initialize transports
        self._transports = {}
        for transport in transports:
            t = transport()
            self._transports[t.scheme] = t

        parsed = urllib.parse.urlparse(uri)

        if parsed.scheme not in self._transports:
            raise ValueError("Invalid uri scheme {scheme}. Must be one of {available}.".format(scheme=parsed.scheme, available=",".join(self._transports)))

        self._transport = self._transports[parsed.scheme]

        # Default to /RPC2 for path as it is a common endpoint
        if not parsed.path:
            parsed = parsed[:2] + ("/RPC2",) + parsed[3:]

        self._uri = urllib.parse.urlunparse(parsed)
