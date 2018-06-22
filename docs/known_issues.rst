.. _known_issues:

Known Issues
============

Logging Level
^^^^^^^^^^^^^

It is not fully set up.

Errno 32
^^^^^^^^

Unimportant Exception

::

    [liveproxy-server][info] Detected remote disconnect
    [stream.segmented][debug] Closing worker thread
    [stream.segmented][debug] Closing writer thread
    [liveproxy-server][info] Stream ended
    ----------------------------------------
    Exception happened during processing of request from ('127.0.0.1', 56830)
    Traceback (most recent call last):
      File "/usr/lib64/python2.7/SocketServer.py", line 596, in process_request_thread
        self.finish_request(request, client_address)
      File "/usr/lib64/python2.7/SocketServer.py", line 331, in finish_request
        self.RequestHandlerClass(request, client_address, self)
      File "/usr/lib64/python2.7/SocketServer.py", line 654, in __init__
        self.finish()
      File "/usr/lib64/python2.7/SocketServer.py", line 713, in finish
        self.wfile.close()
      File "/usr/lib64/python2.7/socket.py", line 283, in close
        self.flush()
      File "/usr/lib64/python2.7/socket.py", line 307, in flush
        self._sock.sendall(view[write_offset:write_offset+buffer_size])
    error: [Errno 32] Broken pipe
    ----------------------------------------

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
