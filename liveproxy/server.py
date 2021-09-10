import base64
import errno
import logging
import os
import re
import shlex
import socket
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from select import select
from shutil import which
from socketserver import ThreadingMixIn
from time import time
from urllib.parse import parse_qsl, unquote, urlparse

ACCEPTABLE_ERRNO = (
    errno.ECONNABORTED,
    errno.ECONNRESET,
    errno.EINVAL,
    errno.EPIPE,
)

_re_streamlink = re.compile(r'streamlink$', re.IGNORECASE)
_re_youtube_dl = re.compile(r'(?:youtube|yt)[_-]dl(?:p)?$', re.IGNORECASE)

log = logging.getLogger(__name__.replace('liveproxy.', ''))


def arglist_from_query(path, prog='streamlink'):
    old_data = parse_qsl(urlparse(path).query)
    arglist = [prog]
    for k, v in old_data:
        if k == 'q':
            # backwards compatibility --q
            k = 'default-stream'
        arglist += ['--{0}'.format(unquote(k)), unquote(v)]
    return arglist


class HTTPRequest(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
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
        random_id = hex(int(time()))[5:]
        log = logging.getLogger('{name}.{random_id}'.format(
            name=__name__.replace('liveproxy.', ''),
            random_id=random_id,
        ))

        log.info(f'User-Agent: {self.headers.get("User-Agent", "???")}')
        log.info(f'Client: {self.client_address}')
        log.info(f'Address: {self.address_string()}')

        if self.path.startswith(('/play/', '/streamlink/', '/301/', '/streamlink_301/')):
            # http://127.0.0.1:53422/play/?url=https://foo.bar&q=worst
            arglist = arglist_from_query(self.path)
        elif self.path.startswith(('/base64/')):
            # http://127.0.0.1:53422/base64/STREAMLINK-COMMANDS/
            # http://127.0.0.1:53422/base64/YOUTUBE-DL-COMMANDS/
            # http://127.0.0.1:53422/base64/YT-DLP-COMMANDS/
            try:
                arglist = shlex.split(base64.urlsafe_b64decode(self.path.split('/')[2]).decode('UTF-8'))
            except base64.binascii.Error as err:
                log.error(f'invalid base64 URL: {err}')
                self._headers(404, 'text/html', connection='close')
                return
        else:
            self._headers(404, 'text/html', connection='close')
            return

        prog = which(arglist[0], mode=os.F_OK | os.X_OK)
        if not prog:
            log.error(f'invalid prog, can not find "{arglist[0]}" on your system')
            return

        log.debug(f'Video-Software: {prog}')
        if _re_streamlink.search(prog):
            arglist.extend(['--stdout', '--loglevel', 'none'])
        elif _re_youtube_dl.search(prog):
            arglist.extend(['-o', '-', '--quiet', '--no-playlist', '--no-warnings', '--no-progress'])
        else:
            log.error('Video-Software is not supported.')
            self._headers(404, 'text/html', connection='close')
            return

        log.debug(f'{arglist!r}')
        self._headers(200, 'video/unknown')
        process = subprocess.Popen(arglist,
                                   stderr=subprocess.PIPE,
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   shell=False,
                                   )

        log.info(f'Stream started {random_id}')
        try:
            while True:
                reads, _, _ = select([process.stdout.fileno(), process.stderr.fileno()], [], [])
                for descriptor in reads:
                    # stdout
                    if descriptor == process.stdout.fileno():
                        read = process.stdout.readline()
                        if read:
                            self.wfile.write(read)
                    # stderr
                    if descriptor == process.stderr.fileno():
                        read = process.stderr.readline()
                        if read:
                            log.debug(f'{read[0:-1].decode("utf-8")}')
                    sys.stdout.flush()
                if process.poll() is not None:
                    self.wfile.close()
                    break
        except socket.error as e:
            if isinstance(e.args, tuple):
                if e.errno == errno.EPIPE:
                    # remote peer disconnected
                    log.info('Detected remote disconnect')
                else:
                    log.error(f'E1: {e!r}')
            else:
                log.error(f'E2: {e!r}')

        log.info(f'Stream ended {random_id}')
        process.terminate()
        process.wait()
        process.kill()


class Server(HTTPServer):
    '''HTTPServer class with timeout.'''
    timeout = 5

    def finish_request(self, request, client_address):
        '''Finish one request by instantiating RequestHandlerClass.'''
        try:
            self.RequestHandlerClass(request, client_address, self)
        except ValueError:
            pass
        except socket.error as err:
            if err.errno not in ACCEPTABLE_ERRNO:
                raise


class ThreadedHTTPServer(ThreadingMixIn, Server):
    '''Handle requests in a separate thread.'''
    allow_reuse_address = True
    daemon_threads = True


__all__ = ('HTTPRequest', 'ThreadedHTTPServer')
