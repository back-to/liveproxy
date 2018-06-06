#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os

from setuptools import setup

import liveproxy

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

setup(
    name=liveproxy.__title__,
    version=liveproxy.__version__,
    description=liveproxy.__summary__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    license=liveproxy.__license__,
    url=liveproxy.__uri__,
    project_urls={
        'Documentation': 'https://liveproxy.github.io/',
        'Source': 'https://github.com/back-to/liveproxy/',
        'Tracker': 'https://github.com/back-to/liveproxy/issues',
    },
    author=liveproxy.__author__,
    author_email=liveproxy.__email__,
    packages=['liveproxy'],
    entry_points={
        'console_scripts': [
            'liveproxy=liveproxy.main:main'
        ],
    },
    install_requires=[
        'streamlink>=0.13.0, <1',
    ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Multimedia :: Video',
        'Topic :: Utilities',
    ],
    keywords='LiveProxy Streamlink Livecli Livestreamer IPTV TV',
)
