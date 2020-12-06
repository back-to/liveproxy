import os
import sys

is_py2 = (sys.version_info[0] == 2)
is_py3 = (sys.version_info[0] == 3)
is_win32 = os.name == "nt"

try:
    from http.server import BaseHTTPRequestHandler
    from http.server import HTTPServer
except ImportError:
    # Python 2.7
    from BaseHTTPServer import BaseHTTPRequestHandler
    from BaseHTTPServer import HTTPServer

try:
    from socketserver import ThreadingMixIn
except ImportError:
    # Python 2.7
    from SocketServer import ThreadingMixIn

try:
    from urllib.parse import (
        urlparse, urlunparse, urljoin, quote, unquote, unquote_plus, parse_qsl, urlencode, urlsplit, urlunsplit
    )
    import queue
except ImportError:
    from urlparse import urlparse, urlunparse, urljoin, parse_qsl, urlsplit, urlunsplit
    from urllib import quote, unquote, unquote_plus, urlencode
    import Queue as queue

try:
    from shutil import which
except ImportError:
    from backports.shutil_which import which

try:
    from html import unescape as html_unescape
except ImportError:
    from HTMLParser import HTMLParser
    html_unescape = unescape = HTMLParser().unescape

__all__ = (
    'BaseHTTPRequestHandler',
    'HTTPServer',
    'ThreadingMixIn',
    'html_unescape',
    'parse_qsl',
    'queue',
    'quote',
    'unquote',
    'unquote_plus',
    'urlencode',
    'urljoin',
    'urlparse',
    'urlsplit',
    'urlunparse',
    'urlunsplit',
    'which',
)
