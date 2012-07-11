from __future__ import absolute_import
from __future__ import division

import pytest

import xmlrpc2.client

from xmlrpc2.exceptions import UnsupportedScheme


@pytest.mark.parametrize("url", ["http://example.com/", "https://example.com/"])
def test_valid_urls(url):
    xmlrpc2.client.Client(url)


@pytest.mark.parametrize("url", ["foo://example.com/"])
def test_invalid_urls(url):
    with pytest.raises(UnsupportedScheme):
        xmlrpc2.client.Client(url)
