# -*- coding: utf-8 -*-
import re

from textwrap import dedent

from liveproxy import __version__ as liveproxy_version

from .constants import FILE_OUTPUT_LIST
from streamlink_cli.argparser import (
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


def file_output_list(value):
    if not value.endswith(tuple(FILE_OUTPUT_LIST)):
        raise ValueError

    return value


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
      https://liveproxy.github.io/
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

    Can also be used for `--file`

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

    Can also be used for `--file`

    Default is 53422.
    '''
)

url = parser.add_argument_group('URL options')
url.add_argument(
    '--file',
    metavar='FILE',
    help='''
    Read the given file and create a new file with base64
    encoded URLs for LiveProxy.

    It will only encode lines that starts with `streamlink`,
    other lines will be ignored.

    You can use `--file-output` to specify the new file.
    '''
)
url.add_argument(
    '--file-output',
    metavar='FILE',
    type=file_output_list,
    help='''
    Use a custom output file for `--file` instead of a '.new' file.

    Valid files are: {0}
    '''.format(' '.join(FILE_OUTPUT_LIST))
)
url.add_argument(
    '--format',
    default='m3u',
    choices=['m3u', 'e2'],
    help='''
    Some playlists need special settings:

    For E2 Linux Receivers with Userbouquets,
    use `--format e2`

    Default is m3u
    ''',
)

__all__ = ['parser']
