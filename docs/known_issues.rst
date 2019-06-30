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

If you want to use FFmpeg or RTMP Streams,
you will need a compiled version of FFmpeg or RTMPdump for your system.

Don't use them if it doesn't work for you.
