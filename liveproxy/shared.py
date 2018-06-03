# -*- coding: utf-8 -*-
'''
    Python classes that are shared between
      LiveProxy main.py and Kodi service.liveproxy
'''
import logging
import os
import sys

from streamlink import __version__ as streamlink_version

import streamlink.logger as logger

log = logging.getLogger('streamlink.liveproxy-shared')


def check_root():
    if hasattr(os, 'getuid'):
        if os.geteuid() == 0:
            log.info('LiveProxy is running as root! Be careful!')


def check_streamlink_version():
    streamlink_commit = 100
    wrong_version = False
    _v = streamlink_version.split('+')
    if _v[0] < '0.12.1':
        wrong_version = True
    elif _v[0] == '0.12.1':
        try:
            if (int(_v[1].split('.')[0]) >= streamlink_commit):
                wrong_version = False
            else:
                wrong_version = True
        except IndexError:
            wrong_version = True
    else:
        wrong_version = False

    if wrong_version is True:
        log.error('Streamlink version 0.12.1+{0} is required, your version is {1}'.format(
            streamlink_commit, streamlink_version))
        log.info('pip install -U git+https://github.com/streamlink/streamlink.git')
        sys.exit(1)


def setup_logging(stream=sys.stdout, level='info'):
    logger.basicConfig(stream=stream, level=level, format='[{name}][{levelname}] {message}', style='{')


__all__ = [
    'check_root',
    'check_streamlink_version',
    'logger',
    'setup_logging',
]
