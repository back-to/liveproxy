#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os
import re

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(
        r'''^__version__ = ['"]([^'"]*)['"]''',
        version_file,
        re.M,
    )
    if version_match:
        return version_match.group(1)

    raise RuntimeError('Unable to find version string.')


long_description = read('README.md')

setup(
    name='liveproxy',
    version=find_version('liveproxy', '__init__.py'),
    description='LiveProxy is a local Proxyserver between Streamlink and an URL.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='BSD 2-Clause "Simplified" License',
    url='https://github.com/back-to/liveproxy',
    project_urls={
        'Documentation': 'https://liveproxy.github.io/',
        'Source': 'https://github.com/back-to/liveproxy/',
        'Tracker': 'https://github.com/back-to/liveproxy/issues',
    },
    author='back-to',
    author_email='backto@protonmail.ch',
    packages=['liveproxy'],
    entry_points={
        'console_scripts': [
            'liveproxy=liveproxy.main:main'
        ],
    },
    install_requires=[
        'streamlink>=1.1.1',
    ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
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
