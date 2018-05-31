#!/usr/bin/env python
# -*- coding: utf-8 -*-
import errno
import logging
import sys

from .argparser import parser
from .shared import (
    check_root,
    log_current_versions,
    setup_logging,
)
from .server import (
    HTTPRequest,
    ThreadedHTTPServer,
)

log = logging.getLogger('streamlink.liveproxy-main')


def main():
    error_code = 0

    args = parser.parse_args(sys.argv[1:])

    setup_logging()

    check_root()
    log_current_versions()

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
