import pytest

import xmlrpc2.server


def test_dotted_attribute():
    # this will raise AttributeError because code don't want us to use
    # private methods
    with pytest.raises(AttributeError):
        xmlrpc2.server.resolve_dotted_attribute(str, "__add")

    assert xmlrpc2.server.resolve_dotted_attribute(str, "title")
