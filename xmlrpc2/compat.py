from __future__ import absolute_import
from __future__ import division

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

    base64.encodebytes = base64.encodestring
    base64.decodebytes = base64.decodestring

    bytes = str
    str = unicode
    basestring = basestring

    long = long

    class UnicodeMixin(object):
        __str__ = lambda x: unicode(x).encode("utf-8")
elif is_py3:
    str = str
    bytes = bytes
    basestring = (str, bytes)

    long = int

    class UnicodeMixin(object):
        __str__ = lambda x: x.__unicode__()
