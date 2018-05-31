# -*- coding: utf-8 -*-
'''
    Python classes that are shared between
      LiveProxy main.py and Kodi service.liveproxy
'''
import logging
import os
import platform
import sys

from liveproxy import __version__ as liveproxy_version
from requests import __version__ as requests_version
from streamlink import __version__ as streamlink_version
from websocket import __version__ as websocket_version

import streamlink.logger as logger

log = logging.getLogger('streamlink.liveproxy-shared')


def check_root():
    if hasattr(os, 'getuid'):
        if os.geteuid() == 0:
            log.info('LiveProxy is running as root! Be careful!')


def check_streamlink_version():
    wrong_version = False
    _v = streamlink_version.split('+')
    if _v[0] < '0.12.1':
        wrong_version = True
    elif _v[0] == '0.12.1':
        try:
            if (_v[1].split('.')[0] >= '73'):
                wrong_version = False
            else:
                wrong_version = True
        except IndexError:
            wrong_version = True
    else:
        wrong_version = False

    if wrong_version is True:
        log.error('Streamlink version 0.12.1+73 is required, your version is {0}'.format(streamlink_version))
        log.info('pip install -U git+https://github.com/streamlink/streamlink.git')
        sys.exit(1)


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
    log.debug('OS:            {0}'.format(os_version))
    log.debug('Python:        {0}'.format(platform.python_version()))
    log.debug('LiveProxy:     {0}'.format(liveproxy_version))
    log.debug('Streamlink:    {0}'.format(streamlink_version))
    log.debug('Requests({0}), Websocket({1})'.format(
        requests_version, websocket_version))


def setup_logging(stream=sys.stdout, level='info'):
    logger.basicConfig(stream=stream, level=level, format='[{name}][{levelname}] {message}', style='{')


__all__ = [
    'check_root',
    'check_streamlink_version',
    'log_current_versions',
    'logger',
    'setup_logging',
]
