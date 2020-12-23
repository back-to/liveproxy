#!/usr/bin/env python
import errno
import logging
import os
import platform
import sys

import streamlink.logger as logger
from requests import __version__ as requests_version
from streamlink import __version__ as streamlink_version

from liveproxy import __version__ as liveproxy_version
from liveproxy.argparser import parser

log = logging.getLogger('streamlink.liveproxy-main')


def log_current_versions():
    '''Show current installed versions'''

    # MAC OS X
    if sys.platform == 'darwin':
        os_version = 'macOS {0}'.format(platform.mac_ver()[0])
    # Windows
    elif sys.platform.startswith('win'):
        os_version = '{0} {1}'.format(platform.system(), platform.release())
    # linux / other
    else:
        os_version = platform.platform()
from liveproxy.files import create_file
from liveproxy.server import HTTPRequest, ThreadedHTTPServer

    log.info('For LiveProxy support visit https://github.com/back-to/liveproxy')
    log.debug('OS:         {0}'.format(os_version))
    log.debug('Python:     {0}'.format(platform.python_version()))
    log.debug('LiveProxy:  {0}'.format(liveproxy_version))
    log.debug('Streamlink: {0}'.format(streamlink_version))
    log.debug('Requests:   {0}'.format(requests_version))


def setup_logging(stream=sys.stdout, level="info"):
    logger.basicConfig(
        stream=stream,
        level=level,
        style="{",
        format=("[{asctime}]" if level == "trace" else "") + "[{name}][{levelname}] {message}",
        datefmt="%H:%M:%S" + (".%f" if level == "trace" else "")
    )


def main():
    error_code = 0

    args = parser.parse_args(sys.argv[1:])

    setup_logging()

    if hasattr(os, 'getuid'):
        if os.geteuid() == 0:
            log.info('LiveProxy is running as root! Be careful!')

    log_current_versions()

    HOST = args.host
    PORT = int(args.port)

    if args.help:
        parser.print_help()



    if args.file:
        create_file(args)
    else:
        log.info('Starting server: {0} on port {1}'.format(HOST, PORT))

        try:
            httpd = ThreadedHTTPServer((HOST, PORT), HTTPRequest)
        except OSError as err:
            if err.errno == errno.EADDRINUSE:
                log.error('Could not listen on port {0}! Exiting...'.format(PORT))
                sys.exit(errno.EADDRINUSE)
            log.error('Error {0}! Exiting...'.format(err.errno))
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
                    log.info('Closing server {0} on port {1} ...'.format(HOST, PORT))
                    httpd.shutdown()
                    httpd.server_close()
                except KeyboardInterrupt:
                    error_code = 130

        sys.exit(error_code)
