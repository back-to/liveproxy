.. _known_issues:

Known Issues
============

Logging Level
^^^^^^^^^^^^^

It is not fully set up.

Kodi: DEBUG spam
^^^^^^^^^^^^^^^^

currently a bit broken

::

    DEBUG: [liveproxy-server][info] Available streams: live (worst, best)
    DEBUG: .
    DEBUG: [liveproxy-server][info] Opening stream: live (hls)
    DEBUG: .
    DEBUG: [stream.hls][debug] Reloading playlist
    DEBUG: .

FFmpeg and RTMP
^^^^^^^^^^^^^^^

FFmpeg and RTMP streams might not work on every platform,
they work on Linux, but not on Windows for me.

Don't use them if it doesn't work for you.
