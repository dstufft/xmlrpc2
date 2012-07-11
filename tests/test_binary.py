from __future__ import absolute_import
from __future__ import division

import base64

import xmlrpc2.client

from xmlrpc2.compat import str

# @@@ What should str(Binary(b"\xff")) return?  I'm chosing "\xff"
#     for now (i.e. interpreting the binary data as Latin-1-encoded
#     text).  But this feels very unsatisfactory.  Perhaps we should
#     only define repr(), and return r"Binary(b'\xff')" instead?


def test_default():
    t = xmlrpc2.client.Binary()

    assert str(t) == ""


def test_string():
    d = b"\x01\x02\x03abc123\xff\xfe"
    t = xmlrpc2.client.Binary(d)

    assert str(t) == str(d, "latin-1")


def test_decode():
    d = b'\x01\x02\x03abc123\xff\xfe'
    de = base64.encodebytes(d)

    t1 = xmlrpc2.client.Binary()
    t2 = xmlrpc2.client._binary(de)

    t1.decode(de)

    assert str(t1) == str(d, "latin-1")
    assert str(t2) == str(d, "latin-1")
