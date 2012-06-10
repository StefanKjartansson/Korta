#!/usr/bin/env python
# -*- coding: utf-8 -
# flake8: noqa
"""
korta.compat
~~~~~~~~~~~~

2K-3K compatibility layer.
"""
import sys

v = sys.version_info
is_py2 = (v[0] == 2)
is_py3 = (v[0] == 3)

if is_py2:
    from urllib import quote, unquote, unquote_plus, urlencode
    from urlparse import parse_qsl, urlparse, urlunparse, urljoin, urlsplit
    from StringIO import StringIO
    import ConfigParser as configparser

    bytes = str
    str = unicode
    basestring = basestring

elif is_py3:
    from urllib.parse import parse_qsl, urlparse, urlunparse, urljoin, urlsplit, urlencode, quote, unquote
    from urllib.request import parse_http_list
    from io import StringIO
    import configparser

    str = str
    bytes = bytes
    basestring = (str,bytes)
