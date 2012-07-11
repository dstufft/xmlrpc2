import xmlrpc2.client


def test_escape():
    assert xmlrpc2.client.escape("a&b") == "a&amp;b"
    assert xmlrpc2.client.escape("a<b") == "a&lt;b"
    assert xmlrpc2.client.escape("a>b") == "a&gt;b"
