"""
    This is a mirror file with custom changes of

    - src/streamlink_cli/argparser.py
"""
import argparse
import re

from string import printable
from textwrap import dedent

from streamlink.utils.times import hours_minutes_seconds

from .constants import (
    STREAMLINK_VERSION, STREAM_PASSTHROUGH, DEFAULT_PLAYER_ARGUMENTS
)
from .shared import logger

try:
    from .utils import find_default_player
except ImportError:
    # ignore for Kodi
    def find_default_player():
        pass

_filesize_re = re.compile(r"""
    (?P<size>\d+(\.\d+)?)
    (?P<modifier>[Kk]|[Mm])?
    (?:[Bb])?
""", re.VERBOSE)
_keyvalue_re = re.compile(r"(?P<key>[^=]+)\s*=\s*(?P<value>.*)")
_printable_re = re.compile(r"[{0}]".format(printable))
_option_re = re.compile(r"""
    (?P<name>[A-z-]+) # A option name, valid characters are A to z and dash.
    \s*
    (?P<op>=)? # Separating the option and the value with a equals sign is
               # common, but optional.
    \s*
    (?P<value>.*) # The value, anything goes.
""", re.VERBOSE)


class ArgumentParser(argparse.ArgumentParser):
    def convert_arg_line_to_args(self, line):
        # Strip any non-printable characters that might be in the
        # beginning of the line (e.g. Unicode BOM marker).
        match = _printable_re.search(line)
        if not match:
            return
        line = line[match.start():].strip()

        # Skip lines that do not start with a valid option (e.g. comments)
        option = _option_re.match(line)
        if not option:
            return

        name, value = option.group("name", "value")
        if name and value:
            yield "--{0}={1}".format(name, value)
        elif name:
            yield "--{0}".format(name)


class HelpFormatter(argparse.RawDescriptionHelpFormatter):
    """A nicer help formatter.

    Help for arguments can be indented and contain new lines.
    It will be de-dented and arguments in the help will be
    separated by a blank line for better readability.

    Originally written by Jakub Roztocil of the httpie project.
    """

    def __init__(self, max_help_position=4, *args, **kwargs):
        # A smaller indent for args help.
        kwargs["max_help_position"] = max_help_position
        argparse.RawDescriptionHelpFormatter.__init__(self, *args, **kwargs)

    def _split_lines(self, text, width):
        text = dedent(text).strip() + "\n\n"
        return text.splitlines()


def comma_list(values):
    return [val.strip() for val in values.split(",")]


def comma_list_filter(acceptable):
    def func(p):
        values = comma_list(p)
        return list(filter(lambda v: v in acceptable, values))

    return func


def num(type, min=None, max=None):
    def func(value):
        value = type(value)

        if min is not None and not (value > min):
            raise argparse.ArgumentTypeError(
                "{0} value must be more than {1} but is {2}".format(
                    type.__name__, min, value
                )
            )

        if max is not None and not (value <= max):
            raise argparse.ArgumentTypeError(
                "{0} value must be at most {1} but is {2}".format(
                    type.__name__, max, value
                )
            )

        return value

    func.__name__ = type.__name__

    return func


def filesize(value):
    match = _filesize_re.match(value)
    if not match:
        raise ValueError

    size = float(match.group("size"))
    if not size:
        raise ValueError

    modifier = match.group("modifier")
    if modifier in ("M", "m"):
        size *= 1024 * 1024
    elif modifier in ("K", "k"):
        size *= 1024

    return num(int, min=0)(size)


def keyvalue(value):
    match = _keyvalue_re.match(value)
    if not match:
        raise ValueError

    return match.group("key", "value")


def boolean(value):
    truths = ["yes", "1", "true", "on"]
    falses = ["no", "0", "false", "off"]
    if value.lower() not in truths + falses:
        raise argparse.ArgumentTypeError("{0} was not one of {{{1}}}".format(value, ', '.join(truths + falses)))

    return value.lower() in truths


def build_parser():
    parser = ArgumentParser(
        fromfile_prefix_chars="@",
        formatter_class=HelpFormatter,
        add_help=False,
        usage="%(prog)s [OPTIONS] <URL> [STREAM]",
        description=dedent("""
        Streamlink is command-line utility that extracts streams from
        various services and pipes them into a video player of choice.
        """),
        epilog=dedent("""
        For more in-depth documentation see:
          https://streamlink.github.io

        Please report broken plugins or bugs to the issue tracker on Github:
          https://github.com/streamlink/streamlink/issues
        """)
    )

    # LiveProxy can't handle 'Positional arguments' correctly
    positional = parser.add_argument_group("Positional arguments")
    positional.add_argument(
        "--dont-error-url",
        dest="url",
        metavar="URL",
        required=False,
        help=argparse.SUPPRESS
    )
    # custom command --q for quality, so it can be used in the url
    positional.add_argument(
        "--q",
        dest="stream",
        metavar="STREAM",
        type=comma_list,
        required=False,
        help=argparse.SUPPRESS
    )

    general = parser.add_argument_group("General options")
    general.add_argument(
        "-h", "--help",
        action="store_true"
    )
    general.add_argument(
        "-V", "--version",
        action="version",
        version="%(prog)s {0}".format(STREAMLINK_VERSION)
    )
    general.add_argument(
        "--plugins",
        action="store_true"
    )
    general.add_argument(
        "--plugin-dirs",
        metavar="DIRECTORY",
        type=comma_list
    )
    general.add_argument(
        "--can-handle-url",
        metavar="URL"
    )
    general.add_argument(
        "--can-handle-url-no-redirect",
        metavar="URL"
    )
    general.add_argument(
        "--config",
        action="append",
        metavar="FILENAME"
    )
    general.add_argument(
        "-l", "--loglevel",
        metavar="LEVEL",
        choices=logger.levels,
        default="info"
    )
    general.add_argument(
        "-Q", "--quiet",
        action="store_true"
    )
    general.add_argument(
        "-j", "--json",
        action="store_true"
    )
    general.add_argument(
        "--auto-version-check",
        type=boolean,
        metavar="{yes,true,1,on,no,false,0,off}",
        default=False
    )
    general.add_argument(
        "--version-check",
        action="store_true"
    )
    general.add_argument(
        "--locale",
        type=str,
        metavar="LOCALE"
    )
    general.add_argument(
        "--twitch-oauth-authenticate",
        action="store_true"
    )

    player = parser.add_argument_group("Player options")
    player.add_argument(
        "-p", "--player",
        metavar="COMMAND",
        default=find_default_player()
    )
    player.add_argument(
        "-a", "--player-args",
        metavar="ARGUMENTS",
        default=DEFAULT_PLAYER_ARGUMENTS
    )
    player.add_argument(
        "-v", "--verbose-player",
        action="store_true"
    )
    player.add_argument(
        "-n", "--player-fifo", "--fifo",
        action="store_true"
    )
    player.add_argument(
        "--player-http",
        action="store_true"
    )
    player.add_argument(
        "--player-continuous-http",
        action="store_true"
    )
    player.add_argument(
        "--player-external-http",
        action="store_true"
    )
    player.add_argument(
        "--player-external-http-port",
        metavar="PORT",
        type=num(int, min=0, max=65535),
        default=0
    )
    player.add_argument(
        "--player-passthrough",
        metavar="TYPES",
        type=comma_list_filter(STREAM_PASSTHROUGH),
        default=[]
    )
    player.add_argument(
        "--player-no-close",
        action="store_true"
    )

    output = parser.add_argument_group("File output options")
    output.add_argument(
        "-o", "--output",
        metavar="FILENAME"
    )
    output.add_argument(
        "-f", "--force",
        action="store_true"
    )
    output.add_argument(
        "-O", "--stdout",
        action="store_true"
    )

    stream = parser.add_argument_group("Stream options")
    stream.add_argument(
        "--url",
        dest="url_param",
        metavar="URL"
    )
    stream.add_argument(
        "--default-stream",
        type=comma_list,
        metavar="STREAM"
    )
    stream.add_argument(
        "--retry-streams",
        metavar="DELAY",
        type=num(float, min=0)
    )
    stream.add_argument(
        "--retry-max",
        metavar="COUNT",
        type=num(int, min=-1)
    )
    stream.add_argument(
        "--retry-open",
        metavar="ATTEMPTS",
        type=num(int, min=0),
        default=1
    )
    stream.add_argument(
        "--stream-types", "--stream-priority",
        metavar="TYPES",
        type=comma_list
    )
    stream.add_argument(
        "--stream-sorting-excludes",
        metavar="STREAMS",
        type=comma_list
    )

    transport = parser.add_argument_group("Stream transport options")
    transport.add_argument(
        "--hds-live-edge",
        type=num(float, min=0),
        metavar="SECONDS"
    )
    transport.add_argument(
        "--hds-segment-attempts",
        type=num(int, min=0),
        metavar="ATTEMPTS"
    )
    transport.add_argument(
        "--hds-segment-threads",
        type=num(int, max=10),
        metavar="THREADS"
    )
    transport.add_argument(
        "--hds-segment-timeout",
        type=num(float, min=0),
        metavar="TIMEOUT"
    )
    transport.add_argument(
        "--hds-timeout",
        type=num(float, min=0),
        metavar="TIMEOUT"
    )
    transport.add_argument(
        "--hls-live-edge",
        type=num(int, min=0),
        metavar="SEGMENTS"
    )
    transport.add_argument(
        "--hls-segment-attempts",
        type=num(int, min=0),
        metavar="ATTEMPTS"
    )
    transport.add_argument(
        "--hls-playlist-reload-attempts",
        type=num(int, min=0),
        metavar="ATTEMPTS"
    )
    transport.add_argument(
        "--hls-segment-threads",
        type=num(int, max=10),
        metavar="THREADS"
    )
    transport.add_argument(
        "--hls-segment-timeout",
        type=num(float, min=0),
        metavar="TIMEOUT")
    transport.add_argument(
        "--hls-segment-ignore-names",
        metavar="NAMES",
        type=comma_list
    )
    transport.add_argument(
        "--hls-audio-select",
        type=comma_list,
        metavar="CODE"
    )
    transport.add_argument(
        "--hls-timeout",
        type=num(float, min=0),
        metavar="TIMEOUT"
    )
    transport.add_argument(
        "--hls-start-offset",
        type=hours_minutes_seconds,
        metavar="HH:MM:SS",
        default=None
    )
    transport.add_argument(
        "--hls-duration",
        type=hours_minutes_seconds,
        metavar="HH:MM:SS",
        default=None
    )
    transport.add_argument(
        "--hls-live-restart",
        action="store_true"
    )
    transport.add_argument(
        "--http-stream-timeout",
        type=num(float, min=0),
        metavar="TIMEOUT"
    )
    transport.add_argument(
        "--ringbuffer-size",
        metavar="SIZE",
        type=filesize
    )
    transport.add_argument(
        "--rtmp-proxy", "--rtmpdump-proxy",
        metavar="PROXY"
    )
    transport.add_argument(
        "--rtmp-rtmpdump", "--rtmpdump", "-r",
        metavar="FILENAME"
    )
    transport.add_argument(
        "--rtmp-timeout",
        type=num(float, min=0),
        metavar="TIMEOUT"
    )
    transport.add_argument(
        "--stream-segment-attempts",
        type=num(int, min=0),
        metavar="ATTEMPTS"
    )
    transport.add_argument(
        "--stream-segment-threads",
        type=num(int, max=10),
        metavar="THREADS"
    )
    transport.add_argument(
        "--stream-segment-timeout",
        type=num(float, min=0),
        metavar="TIMEOUT"
    )
    transport.add_argument(
        "--stream-timeout",
        type=num(float, min=0),
        metavar="TIMEOUT"
    )
    transport.add_argument(
        "--stream-url",
        action="store_true"
    )
    transport.add_argument(
        "--subprocess-cmdline", "--cmdline", "-c",
        action="store_true"
    )
    transport.add_argument(
        "--subprocess-errorlog", "--errorlog", "-e",
        action="store_true"
    )
    transport.add_argument(
        "--subprocess-errorlog-path", "--errorlog-path",
        type=str,
        metavar="PATH"
    )
    transport.add_argument(
        "--ffmpeg-ffmpeg",
        metavar="FILENAME"
    )
    transport.add_argument(
        "--ffmpeg-verbose",
        action="store_true"
    )
    transport.add_argument(
        "--ffmpeg-verbose-path",
        type=str,
        metavar="PATH"
    )
    transport.add_argument(
        "--ffmpeg-video-transcode",
        metavar="CODEC"
    )
    transport.add_argument(
        "--ffmpeg-audio-transcode",
        metavar="CODEC"
    )

    http = parser.add_argument_group("HTTP options")
    http.add_argument(
        "--http-proxy",
        metavar="HTTP_PROXY"
    )
    http.add_argument(
        "--https-proxy",
        metavar="HTTPS_PROXY"
    )
    http.add_argument(
        "--http-cookie",
        metavar="KEY=VALUE",
        type=keyvalue,
        action="append"
    )
    http.add_argument(
        "--http-header",
        metavar="KEY=VALUE",
        type=keyvalue,
        action="append"
    )
    http.add_argument(
        "--http-query-param",
        metavar="KEY=VALUE",
        type=keyvalue,
        action="append"
    )
    http.add_argument(
        "--http-ignore-env",
        action="store_true"
    )
    http.add_argument(
        "--http-no-ssl-verify",
        action="store_true"
    )
    http.add_argument(
        "--http-disable-dh",
        action="store_true"
    )
    http.add_argument(
        "--http-ssl-cert",
        metavar="FILENAME"
    )
    http.add_argument(
        "--http-ssl-cert-crt-key",
        metavar=("CRT_FILENAME", "KEY_FILENAME"),
        nargs=2
    )
    http.add_argument(
        "--http-timeout",
        metavar="TIMEOUT",
        type=num(float, min=0)
    )

    # Deprecated options
    stream.add_argument(
        "--best-stream-default",
        action="store_true",
        help=argparse.SUPPRESS
    )
    player.add_argument(
        "-q", "--quiet-player",
        action="store_true",
        help=argparse.SUPPRESS
    )
    transport.add_argument(
        "--hds-fragment-buffer",
        type=int,
        metavar="fragments",
        help=argparse.SUPPRESS
    )
    http.add_argument(
        "--http-cookies",
        metavar="COOKIES",
        help=argparse.SUPPRESS
    )
    http.add_argument(
        "--http-headers",
        metavar="HEADERS",
        help=argparse.SUPPRESS
    )
    http.add_argument(
        "--http-query-params",
        metavar="PARAMS",
        help=argparse.SUPPRESS
    )
    general.add_argument(
        "--no-version-check",
        action="store_true",
        help=argparse.SUPPRESS
    )
    return parser


__all__ = ["build_parser"]
