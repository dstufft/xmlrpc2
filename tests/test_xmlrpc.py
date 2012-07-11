from __future__ import absolute_import
from __future__ import division

import datetime
import socket
import sys

import pytest

import xmlrpc2.client

from xmlrpc2.compat import str
from xmlrpc2.utils import iso8601


DUMMY_DATA = [
    {
        "astring": "foo@bar.baz.spam",
        "afloat": 7283.43,
        "anint": 2 ** 20,
        "ashortlong": 2,
        "anotherlist": [".zyx.41"],
        "abase64": xmlrpc2.client.Binary(b"my dog has fleas"),
        "boolean": False,
        "unicode": str("\u4000\u6000\u8000"),
        str("ukey\u4000"): "regular value",
        "datetime1": iso8601.parse("20050210T11:41:23"),
        "datetime2": datetime.datetime(2005, 2, 10, 11, 41, 23, tzinfo=iso8601.utc),
    },
]


def test_dump_load():
    dump = xmlrpc2.client.dumps((DUMMY_DATA,))
    load = xmlrpc2.client.loads(dump)

    assert DUMMY_DATA == load[0][0]


def test_dump_bare_datetime():
    # This checks that an unwrapped datetime.date object can be handled
    # by the marshalling code.  This can't be done via test_dump_load()
    # since with use_datetime set to 1 the unmarshaller would create
    # datetime objects for the 'datetime[123]' keys as well
    dt = datetime.datetime(2005, 2, 10, 11, 41, 23, tzinfo=iso8601.utc)
    s = xmlrpc2.client.dumps((dt,))
    (newdt,), m = xmlrpc2.client.loads(s, use_datetime=1)

    assert newdt == dt
    assert m is None

    (newdt,), m = xmlrpc2.client.loads(s, use_datetime=0)

    assert newdt == xmlrpc2.client.DateTime("20050210T11:41:23")


def test_datetime_before_1900():
    # same as before but with a date before 1900
    dt = datetime.datetime(1,  2, 10, 11, 41, 23, tzinfo=iso8601.utc)
    s = xmlrpc2.client.dumps((dt,))
    (newdt,), m = xmlrpc2.client.loads(s, use_datetime=1)

    assert newdt == dt
    assert m is None

    (newdt,), m = xmlrpc2.client.loads(s, use_datetime=0)

    assert newdt == xmlrpc2.client.DateTime("00010210T11:41:23")


def test_bug_1164912():
    d = xmlrpc2.client.DateTime()
    ((new_d,), dummy) = xmlrpc2.client.loads(xmlrpc2.client.dumps((d,), methodresponse=True))

    assert isinstance(new_d.value, str)

    # Check that the output of dumps() is still an 8-bit string
    s = xmlrpc2.client.dumps((new_d,), methodresponse=True)
    assert isinstance(s, str)


def test_newstyle_class():
    class T(object):
        pass

    t = T()
    t.x = 100
    t.y = "Hello"

    ((t2,), dummy) = xmlrpc2.client.loads(xmlrpc2.client.dumps((t,)))

    assert t2 == t.__dict__


def test_dump_big_long():
    with pytest.raises(OverflowError):
        xmlrpc2.client.dumps((2 ** 99,))


def test_dump_bad_dict():
    with pytest.raises(TypeError):
        xmlrpc2.client.dumps(({(1, 2, 3): 1},))


def test_dump_recursive_seq():
    l = [1, 2, 3]
    t = [3, 4, 5, l]

    l.append(t)

    with pytest.raises(TypeError):
        xmlrpc2.client.dumps((l,))


def test_dump_recursive_dict():
    d = {"1": 1, "2": 1}
    t = {"3": 3, "d": d}

    d["t"] = t

    with pytest.raises(TypeError):
        xmlrpc2.client.dumps((d,))


def test_dump_big_int():
    def _dummy_write(s):
        pass

    if sys.maxsize > 2 ** 31 - 1:
        with pytest.raises(OverflowError):
            xmlrpc2.client.dumps((int(2 ** 34),))

    xmlrpc2.client.dumps((xmlrpc2.client.MAXINT, xmlrpc2.client.MININT))

    with pytest.raises(OverflowError):
        xmlrpc2.client.dumps((xmlrpc2.client.MAXINT + 1,))

    with pytest.raises(OverflowError):
        xmlrpc2.client.dumps((xmlrpc2.client.MININT - 1,))

    m = xmlrpc2.client.Marshaller()
    m.dump_int(xmlrpc2.client.MAXINT, _dummy_write)
    m.dump_int(xmlrpc2.client.MININT, _dummy_write)

    with pytest.raises(OverflowError):
        m.dump_int(xmlrpc2.client.MAXINT + 1, _dummy_write)

    with pytest.raises(OverflowError):
        m.dump_int(xmlrpc2.client.MININT - 1, _dummy_write)


def test_dump_none():
    value = DUMMY_DATA + [None]
    arg1 = (DUMMY_DATA + [None],)

    strg = xmlrpc2.client.dumps(arg1, allow_none=True)

    assert value == xmlrpc2.client.loads(strg)[0][0]

    with pytest.raises(TypeError):
        xmlrpc2.client.dumps((arg1,))


@pytest.mark.skipif("sys.version_info < (3,0)")
def test_dump_bytes():
    with pytest.raises(TypeError):
        xmlrpc2.client.dumps((b"my dog has fleas",))


@pytest.mark.xfail(reason="Failing test from massive refactor")
def test_ssl_presence():
    try:
        import ssl
    except ImportError:
        has_ssl = False
    else:
        has_ssl = True

    try:
        xmlrpc2.client.Client("https://localhost:9999").bad_function()
    except NotImplementedError:
        assert not has_ssl, "xmlrpc2 client's error with SSL support"
    except socket.error:
        assert has_ssl
