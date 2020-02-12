import os

from streamlink.compat import is_py2, is_win32

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

STREAM_SYNONYMS = ['best', 'worst', 'best-unfiltered', 'worst-unfiltered']
STREAM_PASSTHROUGH = ['hls', 'http', 'rtmp']

try:
    # Kodi - service.liveproxy
    import xbmc
    if is_py2:
        CONFIG_FILES.extend([xbmc.translatePath('special://profile/addon_data/service.liveproxy/config').encode('utf-8')])
        PLUGINS_DIR.extend([
            xbmc.translatePath('special://profile/addon_data/service.liveproxy/plugins/').encode('utf-8'),
            xbmc.translatePath('special://home/addons/script.module.back-to-plugins/lib/data/').encode('utf-8'),
            xbmc.translatePath('special://home/addons/script.module.streamlink-plugins/lib/data/').encode('utf-8'),
        ])
    else:
        CONFIG_FILES.extend([xbmc.translatePath('special://profile/addon_data/service.liveproxy/config')])
        PLUGINS_DIR.extend([
            xbmc.translatePath('special://profile/addon_data/service.liveproxy/plugins/'),
            xbmc.translatePath('special://home/addons/script.module.back-to-plugins/lib/data/'),
            xbmc.translatePath('special://home/addons/script.module.streamlink-plugins/lib/data/'),
        ])
except ImportError:
    pass

FILE_OUTPUT_LIST = ['.m3u', '.m3u8', '.new', '.txt']

__all__ = [
    'CONFIG_FILES',
    'PLUGINS_DIR',
    'STREAM_PASSTHROUGH',
    'STREAM_SYNONYMS',
    'FILE_OUTPUT_LIST',
]
