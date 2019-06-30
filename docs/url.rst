.. _url:

.. |br| raw:: html

  <br />

*********
URL Guide
*********

Tutorial
--------

LiveProxy is a local Proxyserver between Streamlink and an URL.

After installing and running LiveProxy you will be able to access Streamlink
from any device in your local network via an URL.

.. WARNING::
    LiveProxy is not supposed to run on remote servers,
    it is only meant for a local network.

Now to get into actually using LiveProxy, let's say you want to watch the
stream located on https://www.youtube.com/user/france24, you start off by
starting LiveProxy in your terminal.

.. code-block:: console

    $ liveproxy
    [liveproxy-main][info] For LiveProxy support visit https://github.com/back-to/liveproxy
    [liveproxy-main][info] Starting server: 127.0.0.1 on port 53422

The host or port can be changed with `--host` or `--port`

.. code-block:: console

    $ liveproxy --host 0.0.0.0 --port 12345
    [liveproxy-main][info] For LiveProxy support visit https://github.com/back-to/liveproxy
    [liveproxy-main][info] Starting server: 0.0.0.0 on port 12345

Now that LiveProxy is running, you will have to create a valid proxy url.

For this Examples ``53422`` is used as the **default port**.

Base64
------

  The LiveProxy URL build was simplified,
  the `STREAMLINK-COMMANDS` part must be replaced with your Streamlink commands
  after they got base64 encoded.

  ::

    http://127.0.0.1:53422/base64/STREAMLINK-COMMANDS/

  Example for `streamlink https://www.youtube.com/user/france24 best`

  ::

    http://127.0.0.1:53422/base64/c3RyZWFtbGluayBodHRwczovL3d3dy55b3V0dWJlLmNvbS91c2VyL2ZyYW5jZTI0IGJlc3Q=/

  Redirect with `--player-passthrough` is currently not supported,
  it will be added in a future update.

  LiveProxy can create this URL automatically.

  Create a new file with your Streamlink commands.

  ::

      #EXTM3U
      #EXTINF:-1,Arte FR
      streamlink https://www.arte.tv/fr/direct/ 720p,720p_alt,best
      #EXTINF:-1,France24
      streamlink https://www.youtube.com/user/france24 best
      #EXTINF:-1 tvg-id="EuroNews" tvg-name="EuroNews",Euronews
      streamlink https://www.euronews.com/live best

  For this example the filename is `example.m3u`,
  create a valid URL for LiveProxy.

  ::

      liveproxy --file example.m3u

  It will create a new file `example.m3u.new` with valid URLs,
  only lines with `streamlink` at the start will be changed.

  ::

      #EXTM3U
      #EXTINF:-1,Arte FR
      http://127.0.0.1:53422/base64/c3RyZWFtbGluayBodHRwczovL3d3dy5hcnRlLnR2L2ZyL2RpcmVjdC8gNzIwcCw3MjBwX2FsdCxiZXN0/
      #EXTINF:-1,France24
      http://127.0.0.1:53422/base64/c3RyZWFtbGluayBodHRwczovL3d3dy55b3V0dWJlLmNvbS91c2VyL2ZyYW5jZTI0IGJlc3Q=/
      #EXTINF:-1 tvg-id="EuroNews" tvg-name="EuroNews",Euronews
      http://127.0.0.1:53422/base64/c3RyZWFtbGluayBodHRwczovL3d3dy5ldXJvbmV3cy5jb20vbGl2ZSBiZXN0/

  You can also use ``--file-output`` for a specified new file,
  but be careful don't overwrite any important files.

  ::

      liveproxy --file example.m3u --file-output my_file.m3u

Configuration file
------------------

  LiveProxy is fully compatible with the way Streamlink uses configuration files

  For more Details see `Streamlink-configuration-file`_

  The following path can be used for Kodi

  ::

    special://profile/addon_data/service.liveproxy/config

  .. Note:: strongly recommended for Usernames and Passwords

.. _Streamlink-configuration-file: https://streamlink.github.io/cli.html#configuration-file


Examples
--------

URL
^^^

  Here are some finished working examples.

  **Euronews**

  ::

      http://127.0.0.1:53422/base64/c3RyZWFtbGluayBodHRwczovL3d3dy5ldXJvbmV3cy5jb20vbGl2ZSBiZXN0/

  **France24**

  ::

      http://127.0.0.1:53422/base64/c3RyZWFtbGluayBodHRwczovL3d3dy55b3V0dWJlLmNvbS91c2VyL2ZyYW5jZTI0IGJlc3Q=/

M3U
^^^

  **Euronews**

  ::

    #EXTINF:-1 tvg-id="EURONEWS" group-title="English;News" tvg-logo="",Euronews
    http://127.0.0.1:53422/base64/c3RyZWFtbGluayBodHRwczovL3d3dy5ldXJvbmV3cy5jb20vbGl2ZSBiZXN0/

  **France24**

  ::

    #EXTINF:-1 tvg-id="France24" group-title="English;News" tvg-logo="",France24
    http://127.0.0.1:53422/base64/c3RyZWFtbGluayBodHRwczovL3d3dy55b3V0dWJlLmNvbS91c2VyL2ZyYW5jZTI0IGJlc3Q=/


Userbouquet
^^^^^^^^^^^

  If you use the webinterface, you can just copy your finished URL there. |br|
  But if you use a text editor, you will have to create a valid Userbouquet.

  I will use the service id **4097** IPTV for my examples.

  You can use a different service id such as

  - service **5001** gstplayer (gstreamer)
  - service **5002** exteplayer3 (ffmpeg)

  You might need to install a serviceapp for **5001** and **5002**

  ::

    opkg install enigma2-plugin-systemplugins-serviceapp

  .. note::

      But I only tested it with **4097**

  **Euronews**

  ::

    #SERVICE 4097:0:1:0:0:0:0:0:0:0:http%3a//127.0.0.1%3a53422/base64/c3RyZWFtbGluayBodHRwczovL3d3dy5ldXJvbmV3cy5jb20vbGl2ZSBiZXN0/:Euronews
    #DESCRIPTION Euronews

  **France24**

  ::

    #SERVICE 4097:0:1:0:0:0:0:0:0:0:http%3a//127.0.0.1%3a53422/base64/c3RyZWFtbGluayBodHRwczovL3d3dy55b3V0dWJlLmNvbS91c2VyL2ZyYW5jZTI0IGJlc3Q=/:France24
    #DESCRIPTION France24
