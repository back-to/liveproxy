#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import codecs
import errno
import logging
import os
import platform
import sys

from liveproxy import __version__ as liveproxy_version
from requests import __version__ as requests_version
from streamlink import __version__ as streamlink_version

from .argparser import parser
from .constants import FILE_OUTPUT_LIST
from .shared import (
    check_root,
    setup_logging,
)
from .server import (
    HTTPRequest,
    ThreadedHTTPServer,
)

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

    log.info('For LiveProxy support visit https://github.com/back-to/liveproxy')
    log.debug('OS:         {0}'.format(os_version))
    log.debug('Python:     {0}'.format(platform.python_version()))
    log.debug('LiveProxy:  {0}'.format(liveproxy_version))
    log.debug('Streamlink: {0}'.format(streamlink_version))
    log.debug('Requests:   {0}'.format(requests_version))


def main():
    error_code = 0

    args = parser.parse_args(sys.argv[1:])

    setup_logging()

    check_root()
    log_current_versions()

    HOST = args.host
    PORT = int(args.port)

    if args.help:
        parser.print_help()
    elif args.file:
        if not os.path.isfile(args.file):
            log.error('File does not exist: {0}'.format(args.file))
            return
        elif not os.access(args.file, os.F_OK):
            log.error('Can\'t read file: {0}'.format(args.file))
            return

        if args.format == 'm3u':
            URL_TEMPLATE = 'http://{host}:{port}/base64/{base64}/'
            # %3a
        elif args.format == 'e2':
            URL_TEMPLATE = 'http%3a//{host}%3a{port}/base64/{base64}/'
        else:
            return

        new_lines = []
        log.info('open old file: {0}'.format(args.file))
        with codecs.open(args.file, 'r', 'utf-8') as temp:
            text = temp.read()
            for line in text.splitlines():
                if line.startswith('streamlink'):
                    line = URL_TEMPLATE.format(
                        host=HOST,
                        port=PORT,
                        base64=base64.urlsafe_b64encode(line.encode('utf-8')).decode('utf-8'),
                    )
                new_lines.append(line)

        if args.file_output:
            new_file = args.file_output
        else:
            new_file = args.file + '.new'

        if args.file == new_file:
            log.warning('Don\'t use the same name for the old and the new file.')
            return

        if not new_file.endswith(tuple(FILE_OUTPUT_LIST)):
            log.error('Invalid file type: {0}'.format(new_file))
            return

        log.info('open new file: {0}'.format(new_file))
        with codecs.open(new_file, 'w', 'utf-8') as new_temp:
            for line in new_lines:
                new_temp.write(line + '\n')

        log.info('Done.')
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
