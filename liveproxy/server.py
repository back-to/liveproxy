# -*- coding: utf-8 -*-
import logging
log = logging.getLogger('streamlink.liveproxy-server')


class HTTPRequest(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        log.debug('%s - %s\n' % (self.address_string(), format % args))

    def _headers(self, status, content):
        self.send_response(status)
        self.send_header('Server', 'LiveProxy')
        self.send_header('Content-type', content)
        self.end_headers()

    def do_HEAD(self):
        '''Respond to a HEAD request.'''
        self._headers(404, 'text/html')

    def do_GET(self):
        '''Respond to a GET request.'''
        if self.path.startswith('/play/'):
            main_play(self)
        elif self.path.startswith('/301/'):
            main_play(self, redirect=True)
        else:
            self._headers(404, 'text/html')


class Server(HTTPServer):
    '''HTTPServer class with timeout.'''
    timeout = 5


class ThreadedHTTPServer(ThreadingMixIn, Server):
    '''Handle requests in a separate thread.'''
    daemon_threads = True


__all__ = [
    'HTTPRequest',
    'ThreadedHTTPServer',
]
