# -*- coding: utf-8 -*-
'''
    Python classes that are shared between
      LiveProxy main.py and Kodi service.liveproxy
'''
import logging
import os
import sys

import streamlink.logger as logger

log = logging.getLogger('streamlink.liveproxy-shared')


def check_root():
    if hasattr(os, 'getuid'):
        if os.geteuid() == 0:
            log.info('LiveProxy is running as root! Be careful!')


def setup_logging(stream=sys.stdout, level='debug'):
    fmt = ("[{asctime},{msecs:0.0f}]" if level == "trace" else "") + "[{name}][{levelname}] {message}"
    logger.basicConfig(stream=stream, level=level,
                       format=fmt, style="{",
                       datefmt="%H:%M:%S")


__all__ = [
    'check_root',
    'logger',
    'setup_logging',
]
