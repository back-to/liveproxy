import sys

is_py2 = (sys.version_info[0] == 2)
is_py3 = (sys.version_info[0] == 3)

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

__all__ = (
    'BaseHTTPRequestHandler',
    'HTTPServer',
    'ThreadingMixIn',
)
