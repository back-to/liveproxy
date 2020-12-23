import base64
import errno
import logging
import os
import shlex
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from urllib.parse import parse_qsl, unquote, urlparse

ACCEPTABLE_ERRNO = (
    errno.ECONNABORTED,
    errno.ECONNRESET,
    errno.EINVAL,
    errno.EPIPE,
)
try:
    ACCEPTABLE_ERRNO += (errno.WSAECONNABORTED,)
except AttributeError:
    pass  # Not windows


log = logging.getLogger(__name__.replace('liveproxy.', ''))


def arglist_from_query(path):
    old_data = parse_qsl(urlparse(path).query)
    arglist = []
    for k, v in old_data:
        if k == 'q':
            # backwards compatibility --q
            k = 'default-stream'
        arglist += ['--{0}'.format(unquote(k)), unquote(v)]
    return arglist


class HTTPRequest(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        # log.debug('%s - %s' % (self.address_string(), format % args))
        pass

    def _headers(self, status, content, connection=False):
        self.send_response(status)
        self.send_header('Server', 'LiveProxy')
        self.send_header('Content-type', content)
        if connection:
            self.send_header('Connection', connection)
        self.end_headers()

    def do_HEAD(self):
        '''Respond to a HEAD request.'''
        self._headers(404, 'text/html', connection='close')

    def do_GET(self):
        '''Respond to a GET request.'''
        if self.path.startswith(('/play/', '/streamlink/', '/301/', '/streamlink_301/')):
            # http://127.0.0.1:53422/play/?url=https://foo.bar&q=worst
            arglist = arglist_from_query(self.path)
            main_play(self, arglist)
        elif self.path.startswith(('/base64/')):
            # http://127.0.0.1:53422/base64/STREAMLINK-COMMANDS/
            base64_path = self.path[8:]
            if base64_path.endswith('/'):
                base64_path = base64_path[:-1]
            arglist = shlex.split(base64.urlsafe_b64decode(base64_path).decode('UTF-8'))
            if arglist[0].lower() == 'streamlink':
                arglist = arglist[1:]
            main_play(self, arglist)
        else:
            self._headers(404, 'text/html', connection='close')


class Server(HTTPServer):
    '''HTTPServer class with timeout.'''
    timeout = 5

    def finish_request(self, request, client_address):
        """Finish one request by instantiating RequestHandlerClass."""
        try:
            self.RequestHandlerClass(request, client_address, self)
        except socket.error as err:
            if err.errno not in ACCEPTABLE_ERRNO:
                raise


class ThreadedHTTPServer(ThreadingMixIn, Server):
    '''Handle requests in a separate thread.'''
    allow_reuse_address = True
    daemon_threads = True


__all__ = ('HTTPRequest', 'ThreadedHTTPServer')
