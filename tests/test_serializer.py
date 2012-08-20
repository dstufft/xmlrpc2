from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import datetime

import pytest

from xmlrpc2.serializer import Serializer

from lxml import etree


def test_empty_method_call():
    s = Serializer()
    serialized = s.serialize({
        "methodCall": {
            "methodName": "test"
        }
    })
    assert serialized == b"<methodCall><methodName>test</methodName></methodCall>"


def test_empty_params_method_call():
    s = Serializer()
    serialized = s.serialize({
        "methodCall": {
            "methodName": "test",
            "params": [],
        }
    })
    assert serialized == b"<methodCall><methodName>test</methodName><params/></methodCall>"


def test_all_data_types_method_call():
    s = Serializer()
    serialized = s.serialize({
        "methodCall": {
            "methodName": "test",
            "params": [
                True,
                False,
                1,
                0,
                -1,
                10.5,
                datetime.datetime(year=2012, month=8, day=20, hour=5, minute=32, second=5),
                b"binary data!",
                {
                    "wat": "ok",
                    "winful": True,
                },
                [
                    "one",
                    "two",
                    "three",
                    "and",
                    "a",
                    "four",
                ],
            ],
        }
    })
    assert serialized == b"<methodCall><methodName>test</methodName><params><param><value><boolean>1</boolean></value></param><param><value><boolean>0</boolean></value></param><param><value><int>1</int></value></param><param><value><int>0</int></value></param><param><value><int>-1</int></value></param><param><value><double>10.5</double></value></param><param><value><dateTime.iso8601>2012-08-20T05:32:05</dateTime.iso8601></value></param><param><value><base64>YmluYXJ5IGRhdGEh</base64></value></param><param><value><struct><member><name>wat</name><value><string>ok</string></value></member><member><name>winful</name><value><boolean>1</boolean></value></member></struct></value></param><param><value><array><data><value><string>one</string></value><value><string>two</string></value><value><string>three</string></value><value><string>and</string></value><value><string>a</string></value><value><string>four</string></value></data></array></value></param></params></methodCall>"


@pytest.mark.parametrize(("inp", "expected"), [
    ("one two", b"<value><string>one two</string></value>"),
    ("\x80abc", b"<value><string>&#128;abc</string></value>"),
    (True, b"<value><boolean>1</boolean></value>"),
    (False, b"<value><boolean>0</boolean></value>"),
    (50, b"<value><int>50</int></value>"),
    (101.9, b"<value><double>101.9</double></value>"),
    (datetime.datetime(year=2012, month=8, day=20, hour=5, minute=32, second=5), b"<value><dateTime.iso8601>2012-08-20T05:32:05</dateTime.iso8601></value>"),
    (b"what up dawg", b"<value><base64>d2hhdCB1cCBkYXdn</base64></value>"),
    ({"superman": "clark kent", "batman": "bruce wayne"}, b"<value><struct><member><name>batman</name><value><string>bruce wayne</string></value></member><member><name>superman</name><value><string>clark kent</string></value></member></struct></value>"),
    (["one", "two", "buckle my shoe", "three", "four", "shut the door"], b"<value><array><data><value><string>one</string></value><value><string>two</string></value><value><string>buckle my shoe</string></value><value><string>three</string></value><value><string>four</string></value><value><string>shut the door</string></value></data></array></value>"),
])
def test_to_xml(inp, expected):
    s = Serializer()
    value = etree.tostring(s.to_xml(inp))
    assert value == expected


@pytest.mark.parametrize(("expected", "inp"), [
    ("one two", b"<value><string>one two</string></value>"),
    ("\x80abc", b"<value><string>&#128;abc</string></value>"),
    (True, b"<value><boolean>1</boolean></value>"),
    (False, b"<value><boolean>0</boolean></value>"),
    (50, b"<value><int>50</int></value>"),
    (101.9, b"<value><double>101.9</double></value>"),
    (datetime.datetime(year=2012, month=8, day=20, hour=5, minute=32, second=5), b"<value><dateTime.iso8601>2012-08-20T05:32:05</dateTime.iso8601></value>"),
    (b"what up dawg", b"<value><base64>d2hhdCB1cCBkYXdn</base64></value>"),
    ({"superman": "clark kent", "batman": "bruce wayne"}, b"<value><struct><member><name>batman</name><value><string>bruce wayne</string></value></member><member><name>superman</name><value><string>clark kent</string></value></member></struct></value>"),
    (["one", "two", "buckle my shoe", "three", "four", "shut the door"], b"<value><array><data><value><string>one</string></value><value><string>two</string></value><value><string>buckle my shoe</string></value><value><string>three</string></value><value><string>four</string></value><value><string>shut the door</string></value></data></array></value>"),
])
def test_from_xml(inp, expected):
    s = Serializer()

    value = s.from_xml(etree.fromstring(inp))
    assert value == expected
