import pytest

import xmlrpc2.transport


@pytest.mark.parametrize("transport", [xmlrpc2.transport.BaseTransport])
def test_initalization(transport):
    transport("example.com", 80, "/RPC2")

    with pytest.raises(TypeError):
        transport("example.com")

    with pytest.raises(TypeError):
        transport("example.com", 80)

    with pytest.raises(TypeError):
        transport("example.com", 80, "/RPC2", None)


def test_base_request():
    t = xmlrpc2.transport.BaseTransport("example.com", 80, "/RPC2")

    with pytest.raises(NotImplementedError):
        t.request(None)
