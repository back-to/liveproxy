#!/usr/bin/env python
import errno
import logging
import os
import platform
import sys

from liveproxy import __version__ as liveproxy_version
from liveproxy.argparser import parser
from liveproxy.files import create_file
from liveproxy.server import HTTPRequest, ThreadedHTTPServer

log = logging.getLogger(__name__.replace('liveproxy.', ''))


def main():
    error_code = 0
    args = parser.parse_args(sys.argv[1:])
    if args.help:
        parser.print_help()
        return

    logging.basicConfig(
        stream=sys.stdout,
        level=args.loglevel,
        format='[%(name)s][%(levelname)s] %(message)s',
    )

    if hasattr(os, 'getuid'):
        if os.geteuid() == 0:
            log.info('LiveProxy is running as root! Be careful!')

    # MAC OS X
    if sys.platform == 'darwin':
        os_version = f'macOS {platform.mac_ver()[0]}'
    # Windows
    elif sys.platform.startswith('win'):
        os_version = f'{platform.system()} {platform.release()}'
    # Linux / other
    else:
        os_version = platform.platform()

    log.info('For LiveProxy support visit https://github.com/back-to/liveproxy')
    log.debug(f'OS:         {os_version}')
    log.debug(f'Python:     {platform.python_version()}')
    log.debug(f'LiveProxy:  {liveproxy_version}')

    HOST = str(args.host)
    PORT = int(args.port)

    if args.file:
        create_file(args)
    else:
        log.info(f'Starting server: {HOST} on port {PORT}')

        try:
            httpd = ThreadedHTTPServer((HOST, PORT), HTTPRequest)
        except OSError as err:
            if err.errno == errno.EADDRINUSE:
                log.error(f'Could not listen on port {PORT}! Exiting...')
                sys.exit(errno.EADDRINUSE)
            elif err.errno == errno.EADDRNOTAVAIL:
                log.error(f'Cannot assign requested address {HOST}')
                sys.exit(err.errno)
            log.error(f'Error {err}! Exiting...')
            sys.exit(err.errno)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            # close server
            if httpd:
                httpd.shutdown()
                httpd.server_close()
            log.error('Interrupted! Exiting...')
            error_code = 130
        finally:
            if httpd:
                try:
                    log.info(f'Closing server {HOST} on port {PORT} ...')
                    httpd.shutdown()
                    httpd.server_close()
                except KeyboardInterrupt:
                    error_code = 130

        sys.exit(error_code)
