# -*- coding: utf-8 -*-
import argparse
import base64
import errno
import logging
import os
import shlex
import socket

from collections import OrderedDict
from contextlib import contextmanager
from gettext import gettext

from streamlink import plugins, Streamlink
from streamlink.compat import (
    is_py2,
    parse_qsl,
    unquote,
    urlparse,
)
from streamlink.exceptions import (
    FatalPluginError,
    NoPluginError,
    PluginError,
    StreamError,
)
from streamlink.plugin import PluginOptions
from streamlink.stream import RTMPStream
from streamlink.stream.dash import DASHStream
from streamlink.stream.ffmpegmux import MuxedStream

from .compat import BaseHTTPRequestHandler, HTTPServer, ThreadingMixIn
from .constants import CONFIG_FILES, PLUGINS_DIR, STREAM_SYNONYMS
from streamlink_cli.argparser import build_parser
from .shared import logger

ACCEPTABLE_ERRNO = (
    errno.ECONNABORTED,
    errno.ECONNRESET,
    errno.EINVAL,
    errno.EPIPE,
)
try:
    ACCEPTABLE_ERRNO += (errno.WSAECONNABORTED,)
except AttributeError:
    pass  # Not windows

log = logging.getLogger('streamlink.liveproxy-server')


class TempData(object):
    pass


class LiveProxyStreamlink(Streamlink):
    def load_builtin_plugins(self):
        if not hasattr(TempData, '_loaded_plugins'):
            self.load_plugins(plugins.__path__[0])
            TempData._loaded_plugins = self.plugins.copy()
        else:
            self.plugins = TempData._loaded_plugins.copy()
            if is_py2:
                # Python 2.7
                for plugin in self.plugins.itervalues():
                    plugin.session = self
            else:
                for plugin in iter(self.plugins.values()):
                    plugin.session = self


# copy of - from .utils import ignored
@contextmanager
def ignored(*exceptions):
    try:
        yield
    except exceptions:
        pass


def resolve_stream_name(streams, stream_name):
    '''Returns the real stream name of a synonym.'''

    if stream_name in STREAM_SYNONYMS and stream_name in streams:
        for name, stream in streams.items():
            if stream is streams[stream_name] and name not in STREAM_SYNONYMS:
                return name

    return stream_name


def format_valid_streams(plugin, streams):
    '''Formats a dict of streams.

    Filters out synonyms and displays them next to
    the stream they point to.

    Streams are sorted according to their quality
    (based on plugin.stream_weight).

    '''

    delimiter = ', '
    validstreams = []

    for name, stream in sorted(streams.items(),
                               key=lambda stream: plugin.stream_weight(stream[0])):
        if name in STREAM_SYNONYMS:
            continue

        def synonymfilter(n):
            return stream is streams[n] and n is not name

        synonyms = list(filter(synonymfilter, streams.keys()))

        if len(synonyms) > 0:
            joined = delimiter.join(synonyms)
            name = '{0} ({1})'.format(name, joined)

        validstreams.append(name)

    return delimiter.join(validstreams)


def setup_args(parser, arglist=[], config_files=[], ignore_unknown=True):
    '''Parses arguments.'''

    # Load arguments from config files
    for config_file in filter(os.path.isfile, config_files):
        arglist.insert(0, '@' + config_file)

    args, unknown = parser.parse_known_args(arglist)
    if unknown and not ignore_unknown:
        msg = gettext('unrecognized arguments: %s')
        parser.error(msg % ' '.join(unknown))

    # Force lowercase to allow case-insensitive lookup
    if args.stream:
        args.stream = [stream.lower() for stream in args.stream]

    # force --url as args.url
    if args.url_param:
        args.url = args.url_param
    return args


def load_plugins(session, dirs):
    '''Attempts to load plugins from a list of directories.'''

    dirs = [os.path.expanduser(d) for d in dirs]

    for directory in dirs:
        if os.path.isdir(directory):
            session.load_plugins(directory)
        else:
            log.info('Plugin path {0} does not exist or is not '
                     'a directory!', directory)


def setup_config_args(session, args, parser, arglist):
    config_files = []

    if args.url:
        with ignored(NoPluginError):
            plugin = session.resolve_url(args.url)
            config_files += ['{0}.{1}'.format(fn, plugin.module) for fn in CONFIG_FILES]

    if args.config:
        # We want the config specified last to get highest priority
        config_files += list(reversed(args.config))
    else:
        # Only load first available default config
        for config_file in filter(os.path.isfile, CONFIG_FILES):
            config_files.append(config_file)
            break

    if config_files:
        args = setup_args(parser, arglist, config_files, ignore_unknown=True)
    return args


def setup_plugins(session, args):
    '''Loads any additional plugins.'''
    if args.plugin_dirs:
        PLUGINS_DIR.extend(args.plugin_dirs)

    load_plugins(session, PLUGINS_DIR)


def setup_http_session(session, args):
    '''Sets the global HTTP settings, such as proxy and headers.'''
    if args.http_proxy:
        session.set_option('http-proxy', args.http_proxy)

    if args.https_proxy:
        session.set_option('https-proxy', args.https_proxy)

    if args.http_cookie:
        session.set_option('http-cookies', dict(args.http_cookie))

    if args.http_header:
        session.set_option('http-headers', dict(args.http_header))

    if args.http_query_param:
        session.set_option('http-query-params', dict(args.http_query_param))

    if args.http_ignore_env:
        session.set_option('http-trust-env', False)

    if args.http_no_ssl_verify:
        session.set_option('http-ssl-verify', False)

    if args.http_disable_dh:
        session.set_option('http-disable-dh', True)

    if args.http_ssl_cert:
        session.set_option('http-ssl-cert', args.http_ssl_cert)

    if args.http_ssl_cert_crt_key:
        session.set_option('http-ssl-cert', tuple(args.http_ssl_cert_crt_key))

    if args.http_timeout:
        session.set_option('http-timeout', args.http_timeout)

    if args.http_cookies:
        session.set_option('http-cookies', args.http_cookies)

    if args.http_headers:
        session.set_option('http-headers', args.http_headers)

    if args.http_query_params:
        session.set_option('http-query-params', args.http_query_params)


def setup_options(session, args):
    '''Sets streamlink options.'''
    if args.hls_live_edge:
        session.set_option('hls-live-edge', args.hls_live_edge)

    if args.hls_segment_attempts:
        session.set_option('hls-segment-attempts', args.hls_segment_attempts)

    if args.hls_playlist_reload_attempts:
        session.set_option('hls-playlist-reload-attempts', args.hls_playlist_reload_attempts)

    if args.hls_segment_threads:
        session.set_option('hls-segment-threads', args.hls_segment_threads)

    if args.hls_segment_timeout:
        session.set_option('hls-segment-timeout', args.hls_segment_timeout)

    if args.hls_segment_ignore_names:
        session.set_option('hls-segment-ignore-names', args.hls_segment_ignore_names)

    if args.hls_timeout:
        session.set_option('hls-timeout', args.hls_timeout)

    if args.hls_audio_select:
        session.set_option('hls-audio-select', args.hls_audio_select)

    if args.hls_start_offset:
        session.set_option('hls-start-offset', args.hls_start_offset)

    if args.hls_duration:
        session.set_option('hls-duration', args.hls_duration)

    if args.hls_live_restart:
        session.set_option('hls-live-restart', args.hls_live_restart)

    if args.hds_live_edge:
        session.set_option('hds-live-edge', args.hds_live_edge)

    if args.hds_segment_attempts:
        session.set_option('hds-segment-attempts', args.hds_segment_attempts)

    if args.hds_segment_threads:
        session.set_option('hds-segment-threads', args.hds_segment_threads)

    if args.hds_segment_timeout:
        session.set_option('hds-segment-timeout', args.hds_segment_timeout)

    if args.hds_timeout:
        session.set_option('hds-timeout', args.hds_timeout)

    if args.http_stream_timeout:
        session.set_option('http-stream-timeout', args.http_stream_timeout)

    if args.ringbuffer_size:
        session.set_option('ringbuffer-size', args.ringbuffer_size)

    if args.rtmp_proxy:
        session.set_option('rtmp-proxy', args.rtmp_proxy)

    if args.rtmp_rtmpdump:
        session.set_option('rtmp-rtmpdump', args.rtmp_rtmpdump)

    if args.rtmp_timeout:
        session.set_option('rtmp-timeout', args.rtmp_timeout)

    if args.stream_segment_attempts:
        session.set_option('stream-segment-attempts', args.stream_segment_attempts)

    if args.stream_segment_threads:
        session.set_option('stream-segment-threads', args.stream_segment_threads)

    if args.stream_segment_timeout:
        session.set_option('stream-segment-timeout', args.stream_segment_timeout)

    if args.stream_timeout:
        session.set_option('stream-timeout', args.stream_timeout)

    if args.ffmpeg_ffmpeg:
        session.set_option('ffmpeg-ffmpeg', args.ffmpeg_ffmpeg)
    if args.ffmpeg_verbose:
        session.set_option('ffmpeg-verbose', args.ffmpeg_verbose)
    if args.ffmpeg_verbose_path:
        session.set_option('ffmpeg-verbose-path', args.ffmpeg_verbose_path)
    if args.ffmpeg_video_transcode:
        session.set_option('ffmpeg-video-transcode', args.ffmpeg_video_transcode)
    if args.ffmpeg_audio_transcode:
        session.set_option('ffmpeg-audio-transcode', args.ffmpeg_audio_transcode)

    session.set_option('subprocess-errorlog', args.subprocess_errorlog)
    session.set_option('subprocess-errorlog-path', args.subprocess_errorlog_path)
    session.set_option('locale', args.locale)


def setup_plugin_args(session, parser):
    '''Sets Streamlink plugin options.'''

    plugin_args = parser.add_argument_group('Plugin options')
    for pname, plugin in session.plugins.items():
        defaults = {}
        for parg in plugin.arguments:
            plugin_args.add_argument(parg.argument_name(pname), **parg.options)
            defaults[parg.dest] = parg.default

        plugin.options = PluginOptions(defaults)


def setup_plugin_options(session, args, plugin):
    '''Sets Streamlink plugin options.'''
    pname = plugin.module
    required = OrderedDict({})
    for parg in plugin.arguments:
        if parg.options.get('help') != argparse.SUPPRESS:
            if parg.required:
                required[parg.name] = parg
            value = getattr(args, parg.namespace_dest(pname))
            session.set_plugin_option(pname, parg.dest, value)
            # if the value is set, check to see if any of the required arguments are not set
            if parg.required or value:
                try:
                    for rparg in plugin.arguments.requires(parg.name):
                        required[rparg.name] = rparg
                except RuntimeError:
                    log.error('{0} plugin has a configuration error and the arguments '
                              'cannot be parsed'.format(pname))
                    break
    if required:
        for req in required.values():
            if not session.get_plugin_option(pname, req.dest):
                prompt = req.prompt or 'Enter {0} {1}'.format(pname, req.name)
                session.set_plugin_option(pname, req.dest,
                                          plugin.input_ask_password(prompt)
                                          if req.sensitive else
                                          plugin.input_ask(prompt))


def main_play(HTTPBase, arglist, redirect=False):
    parser = build_parser()
    args = setup_args(parser, arglist, ignore_unknown=True)

    # create a new session for every request
    session = LiveProxyStreamlink()

    log.info('User-Agent: {0}'.format(HTTPBase.headers.get('User-Agent', '???')))
    log.info('Client: {0}'.format(HTTPBase.client_address))
    log.info('Address: {0}'.format(HTTPBase.address_string()))

    setup_plugins(session, args)
    setup_plugin_args(session, parser)
    # call setup args again once the plugin specific args have been added
    args = setup_args(parser, arglist, ignore_unknown=True)
    args = setup_config_args(session, args, parser, arglist)
    logger.root.setLevel(args.loglevel)
    setup_http_session(session, args)

    if args.url:
        setup_options(session, args)

        try:
            plugin = session.resolve_url(args.url)
            setup_plugin_options(session, args, plugin)
            log.info('Found matching plugin {0} for URL {1}',
                     plugin.module, args.url)

            plugin_args = []
            for parg in plugin.arguments:
                value = plugin.get_option(parg.dest)
                if value:
                    plugin_args.append((parg, value))

            if plugin_args:
                log.debug('Plugin specific arguments:')
                for parg, value in plugin_args:
                    log.debug(' {0}={1} ({2})'.format(parg.argument_name(plugin.module),
                                                      value if not parg.sensitive else ('*' * 8),
                                                      parg.dest))

            if redirect is True:
                streams = session.streams(
                    args.url,
                    stream_types=['hls', 'http'])
            else:
                streams = session.streams(
                    args.url,
                    stream_types=args.stream_types,
                    sorting_excludes=args.stream_sorting_excludes)
        except FatalPluginError as err:
            log.error('FatalPluginError {0}', str(err))
            HTTPBase._headers(404, 'text/html', connection='close')
            return
        except NoPluginError:
            log.error('No plugin can handle URL: {0}', args.url)
            HTTPBase._headers(404, 'text/html', connection='close')
            return
        except PluginError as err:
            log.error('PluginError {0}', str(err))
            HTTPBase._headers(404, 'text/html', connection='close')
            return

        if not streams:
            log.error('No playable streams found on this URL: {0}', args.url)
            HTTPBase._headers(404, 'text/html', connection='close')
            return

        if args.default_stream and not args.stream:
            args.stream = args.default_stream

        if not args.stream:
            args.stream = ['best']

        stream_ended = False
        validstreams = format_valid_streams(plugin, streams)
        for stream_name in args.stream:
            if stream_name in streams:
                log.info('Available streams: {0}', validstreams)

                '''Decides what to do with the selected stream.'''

                stream_name = resolve_stream_name(streams, stream_name)
                stream = streams[stream_name]

                # Find any streams with a '_alt' suffix and attempt
                # to use these in case the main stream is not usable.
                alt_streams = list(filter(lambda k: stream_name + '_alt' in k,
                                          sorted(streams.keys())))

                for stream_name in [stream_name] + alt_streams:
                    stream = streams[stream_name]
                    stream_type = type(stream).shortname()

                    log.info('Opening stream: {0} ({1})', stream_name,
                             stream_type)

                    if isinstance(stream, (RTMPStream)):
                        log.info('RTMP streams '
                                 'might not work on every platform.')
                    elif isinstance(stream, (MuxedStream, DASHStream)):
                        log.info('FFmpeg streams (dash, muxed) '
                                 'might not work on every platform.')

                    # 301
                    if redirect is True:
                        log.info('301 - URL: {0}'.format(stream.url))
                        HTTPBase.send_response(301)
                        HTTPBase.send_header('Location', stream.url)
                        HTTPBase.end_headers()
                        log.info('301 - done')
                        stream_ended = True
                        break

                    # play
                    try:
                        fd = stream.open()
                    except StreamError as err:
                        log.error('Could not open stream: {0}'.format(err))
                        continue

                    cache = 4096
                    HTTPBase._headers(200, 'video/unknown')
                    try:
                        log.debug('Pre-buffering {0} bytes'.format(cache))
                        while True:
                            buff = fd.read(cache)
                            if not buff:
                                log.error('No Data for buff!')
                                break
                            HTTPBase.wfile.write(buff)
                        HTTPBase.wfile.close()
                    except socket.error as e:
                        if isinstance(e.args, tuple):
                            if e.errno == errno.EPIPE:
                                # remote peer disconnected
                                log.info('Detected remote disconnect')
                            else:
                                log.error(str(e))
                        else:
                            log.error(str(e))

                    fd.close()
                    log.info('Stream ended')
                    fd = None
                    stream_ended = True

                    break

                if not stream_ended:
                    HTTPBase._headers(404, 'text/html', connection='close')
                return

        else:
            err = ('The specified stream(s) \'{0}\' could not be '
                   'found'.format(', '.join(args.stream)))

            log.error('{0}.\n       Available streams: {1}',
                      err, validstreams)
            HTTPBase._headers(404, 'text/html', connection='close')
            return


def arglist_from_query(path):
    old_data = parse_qsl(urlparse(path).query)
    arglist = []
    for k, v in old_data:
        if k == 'q':
            # backwards compatibility --q
            k = 'default-stream'
        arglist += ['--{0}'.format(unquote(k)), unquote(v)]
    return arglist


class HTTPRequest(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        # log.debug('%s - %s' % (self.address_string(), format % args))
        pass

    def _headers(self, status, content, connection=False):
        self.send_response(status)
        self.send_header('Server', 'LiveProxy')
        self.send_header('Content-type', content)
        if connection:
            self.send_header('Connection', connection)
        self.end_headers()

    def do_HEAD(self):
        '''Respond to a HEAD request.'''
        self._headers(404, 'text/html', connection='close')

    def do_GET(self):
        '''Respond to a GET request.'''
        if self.path.startswith(('/play/', '/streamlink/')):
            # http://127.0.0.1:53422/play/?url=https://foo.bar&q=worst
            arglist = arglist_from_query(self.path)
            main_play(self, arglist)
        elif self.path.startswith(('/301/', '/streamlink_301/')):
            # http://127.0.0.1:53422/301/?url=https://foo.bar&q=worst
            arglist = arglist_from_query(self.path)
            main_play(self, arglist, redirect=True)
        elif self.path.startswith(('/base64/')):
            # http://127.0.0.1:53422/base64/STREAMLINK-COMMANDS/
            base64_path = self.path[8:]
            if base64_path.endswith('/'):
                base64_path = base64_path[:-1]
            arglist = shlex.split(base64.urlsafe_b64decode(base64_path).decode('UTF-8'))
            if arglist[0].lower() == 'streamlink':
                arglist = arglist[1:]
            main_play(self, arglist)
        else:
            self._headers(404, 'text/html', connection='close')


class Server(HTTPServer):
    '''HTTPServer class with timeout.'''
    timeout = 5

    def finish_request(self, request, client_address):
        """Finish one request by instantiating RequestHandlerClass."""
        try:
            self.RequestHandlerClass(request, client_address, self)
        except socket.error as err:
            if err.errno not in ACCEPTABLE_ERRNO:
                raise


class ThreadedHTTPServer(ThreadingMixIn, Server):
    '''Handle requests in a separate thread.'''
    allow_reuse_address = True
    daemon_threads = True


__all__ = [
    'HTTPRequest',
    'ThreadedHTTPServer',
]
