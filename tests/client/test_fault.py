import pytest

import xmlrpc2.client


def test_repr():
    f = xmlrpc2.client.Fault(42, "Test Fault")

    assert repr(f) == "<Fault 42: 'Test Fault'>"
    assert repr(f) == str(f)


def test_dump_fault():
    f = xmlrpc2.client.Fault(42, "Test Fault")
    s = xmlrpc2.client.dumps((f,))

    (newf,), m = xmlrpc2.client.loads(s)

    assert newf == {'faultCode': 42, 'faultString': 'Test Fault'}
    assert m is None

    s = xmlrpc2.client.Marshaller().dumps(f)

    with pytest.raises(xmlrpc2.client.Fault):
        xmlrpc2.client.loads(s)
