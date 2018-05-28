#!/usr/bin/env python
# -*- coding: utf-8 -*-
import errno
import logging
import os
import platform
import sys

from liveproxy import __version__ as liveproxy_version
from requests import __version__ as requests_version
from streamlink import __version__ as streamlink_version
from websocket import __version__ as websocket_version

from .argparser import parser
from .server import (
    HTTPRequest,
    ThreadedHTTPServer,
)

import streamlink.logger as logger

log = logging.getLogger('streamlink.server-main')


def check_root():
    if hasattr(os, 'getuid'):
        if os.geteuid() == 0:
            log.info('LiveProxy is running as root! Be careful!')


def log_current_versions(args):
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

    log.debug('OS:            {0}'.format(os_version))
    log.debug('Python:        {0}'.format(platform.python_version()))
    log.debug('LiveProxy:     {0}'.format(liveproxy_version))
    log.debug('Streamlink:    {0}'.format(streamlink_version))
    log.debug('Requests({0}), Websocket({1})'.format(
        requests_version, websocket_version))


def setup_logging(stream=sys.stdout, level='debug'):
    logger.basicConfig(stream=stream, level=level, format='[{name}][{levelname}] {message}', style='{')


def check_streamlink_version(s_version):
    wrong_version = False
    _v = s_version.split('+')
    if _v[0] < '0.12.1':
        wrong_version = True
    elif _v[0] == '0.12.1':
        try:
            if (_v[1].split('.')[0] >= '53'):
                wrong_version = False
            else:
                wrong_version = True
        except IndexError:
            wrong_version = True
    else:
        wrong_version = False

    return wrong_version


def main():
    error_code = 0

    args = parser.parse_args(sys.argv[1:])

    setup_logging()

    check_root()
    log_current_versions(args)

    if check_streamlink_version(streamlink_version):
        log.error('Streamlink version 0.12.1+53.g7ff1ce8 is required, your version is {0}'.format(streamlink_version))
        log.info('pip install -U git+https://github.com/back-to/streamlink.git@logging-refactor')
        return

    if args.help:
        parser.print_help()
    else:
        HOST = args.host
        PORT = int(args.port)

        log.info('Starting server: {0} on port {1}'.format(HOST, PORT))

        server_class = ThreadedHTTPServer
        server_class.allow_reuse_address = True
        try:
            httpd = server_class((HOST, PORT), HTTPRequest)
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
            log.info('Interrupted! Exiting...')
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
