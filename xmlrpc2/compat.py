# -*- coding: utf-8 -*-
import sys

# -------
# Pythons
# -------

# Syntax sugar.
_ver = sys.version_info

#: Python 2.x?
is_py2 = (_ver[0] == 2)

#: Python 3.x?
is_py3 = (_ver[0] == 3)


if is_py2:
    import base64
    import httplib
    import urllib as urllib_parse

    base64.encodebytes = base64.encodestring
    base64.decodebytes = base64.decodestring

    urllib_parse.unquote_to_bytes = urllib_parse.unquote

    bytes = str
    str = unicode
    basestring = basestring
elif is_py3:
    import http.client as httplib
    import urllib.parse as urllib_parse

    str = str
    bytes = bytes
    basestring = (str, bytes)
