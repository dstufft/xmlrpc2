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
    bytes = str
    str = unicode
    basestring = basestring
elif is_py3:
    str = str
    bytes = bytes
    basestring = (str, bytes)
