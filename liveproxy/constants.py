import os

from streamlink import __version__ as STREAMLINK_VERSION
from streamlink.compat import is_win32

DEFAULT_PLAYER_ARGUMENTS = u"{filename}"
DEFAULT_STREAM_METADATA = {
    "title": u"Unknown Title",
    "author": u"Unknown Author",
    "category": u"No Category",
    "game": u"No Game/Category"
}
SUPPORTED_PLAYERS = {
    "vlc": ["vlc", "vlc.exe"],
    "mpv": ["mpv", "mpv.exe"]
}
LIVESTREAMER_VERSION = STREAMLINK_VERSION

if is_win32:
    APPDATA = os.environ['APPDATA']
    CONFIG_FILES = [os.path.join(APPDATA, 'streamlink', 'streamlinkrc')]
    PLUGINS_DIR = [os.path.join(APPDATA, 'streamlink', 'plugins')]
else:
    XDG_CONFIG_HOME = os.environ.get('XDG_CONFIG_HOME', '~/.config')
    CONFIG_FILES = [
        os.path.expanduser(XDG_CONFIG_HOME + '/streamlink/config'),
        os.path.expanduser('~/.streamlinkrc')
    ]
    PLUGINS_DIR = [os.path.expanduser(XDG_CONFIG_HOME + '/streamlink/plugins')]

STREAM_SYNONYMS = ['best', 'worst']
STREAM_PASSTHROUGH = ['hls', 'http', 'rtmp']

try:
    # Kodi - service.liveproxy
    import xbmc
    CONFIG_FILES.extend([xbmc.translatePath('special://profile/addon_data/service.liveproxy/config').encode('utf-8')])
    PLUGINS_DIR.extend([
        xbmc.translatePath('special://profile/addon_data/service.liveproxy/plugins/').encode('utf-8'),
        xbmc.translatePath('special://home/addons/script.module.back-to-plugins/lib/data/').encode('utf-8'),
        xbmc.translatePath('special://home/addons/script.module.streamlink-plugins/lib/data/').encode('utf-8'),
    ])
except ImportError:
    pass

__all__ = [
    'CONFIG_FILES',
    'DEFAULT_PLAYER_ARGUMENTS',
    'DEFAULT_STREAM_METADATA',
    'LIVESTREAMER_VERSION',
    'PLUGINS_DIR',
    'STREAM_PASSTHROUGH',
    'STREAM_SYNONYMS',
    'STREAMLINK_VERSION',
    'SUPPORTED_PLAYERS',
]
