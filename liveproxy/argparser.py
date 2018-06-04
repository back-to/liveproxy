# -*- coding: utf-8 -*-
import re

from textwrap import dedent

from liveproxy import __version__ as liveproxy_version

from .mirror_argparser import (
    ArgumentParser,
    HelpFormatter,
    num,
)

_ip_address_re = re.compile(r'^((\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])$')


def ip_address(value):
    match = _ip_address_re.match(value)
    if not match:
        raise ValueError

    return match.group(0)


parser = ArgumentParser(
    fromfile_prefix_chars='@',
    formatter_class=HelpFormatter,
    add_help=False,
    usage='%(prog)s --host [HOST] --port [PORT]',
    description=dedent('''
    LiveProxy is a local URL Proxy for Streamlink
    '''),
    epilog=dedent('''
    For more in-depth documentation see:
      https://github.com/back-to/liveproxy
    ''')
)

general = parser.add_argument_group('General options')
general.add_argument(
    '-h', '--help',
    action='store_true',
    help='''
    Show this help message and exit.
    '''
)
general.add_argument(
    '-V', '--version',
    action='version',
    version='%(prog)s {0}'.format(liveproxy_version),
    help='''
    Show version number and exit.
    '''
)

server = parser.add_argument_group('Server options')
server.add_argument(
    '--host',
    metavar='HOST',
    type=ip_address,
    default='127.0.0.1',
    help='''
    A fixed IP to use as a HOST.

    Default is 127.0.0.1.
    '''
)
server.add_argument(
    '--port',
    metavar='PORT',
    type=num(int, min=0, max=65535),
    default=53422,
    help='''
    A fixed PORT to use for the HOST.

    Default is 53422.
    '''
)

__all__ = ['parser']
