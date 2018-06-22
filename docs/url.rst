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

.. Hint::
    There is also a tool that will create a valid m3u file for LiveProxy,
    it requires Python 3.6+ |br|
    https://github.com/back-to/iptv for more informations.

For this Examples ``53422`` is used as the **default port**.

Basic URL
---------

  The basic url where Livecli will handle the playback looks like this.

  ::

    http://127.0.0.1:53422/play/?url=https://www.youtube.com/user/france24

URL encoded
-----------

  The above solution will work for the most websites, |br|
  but URLs with special characters such as ``?`` or ``&`` might not work.

  For this case every parameter should be URL encoded, |br|
  the website `urlencoder.org <https://www.urlencoder.org/>`_ can be used for this.

  ::

    http://127.0.0.1:53422/play/?url=https%3A%2F%2Fexample.com%2Fexample

Quality
-------

  By default LiveProxy will open the best quality, |br|
  if you want a different quality you can use the parameter ``q`` |br|
  with every new parameter, you must add an ``&``

  For this example we will have the parameter ``url`` and ``q``

  ::

    http://127.0.0.1:53422/play/?url=URL&q=720p

Options
-------

  The **/play/** url can almoste handle every Streamlink command.

  Example ``--http-header "X-Forwarded-For=127.0.0.1"`` |br|
  will be ``http-header=X-Forwarded-For%3D127.0.0.1``

  ::

    http://127.0.0.1:53422/play/?url=URL&http-header=X-Forwarded-For%3D127.0.0.1

  .. Attention::
      Don't use Usernames and Passwords in the URL, use the configuration file.

Configuration file
------------------

  LiveProxy is fully compatible with the way Streamlink uses configuration files

  For more Details see `Streamlink-configuration-file`_

  The following path can be used for Kodi

  ::

    special://profile/addon_data/service.liveproxy/config

  .. Note:: strongly recommended for Usernames and Passwords

.. _Streamlink-configuration-file: https://streamlink.github.io/cli.html#configuration-file

Redirect
--------

  There is also a different version which only redirects the streaming url, |br|
  only the basic parameter will work for this such as ``url`` and ``q``

  LiveProxy is only used to get the url, your Player will handle the playback.

  ::

    http://127.0.0.1:53422/301/?url=URL


Userbouquet
-----------

  .. attention::

    Because this is used for the Userbouquet **:** is not allowed in the URL, |br|
    you will have to replace **:** with **%3a**

  **Before**

  ::

    http://127.0.0.1:53422/play/?url=URL

  **After**

  ::

    http%3a//127.0.0.1%3a53422/play/?url=URL


Examples
--------


URL
^^^

  Here are some finished working examples.

  **Euronews**

  ::

    http://127.0.0.1:53422/play/?url=https%253A%252F%252Fwww.euronews.com%252Flive

  **France24**

  ::

    http://127.0.0.1:53422/play/?url=https%3A%2F%2Fwww.youtube.com%2Fuser%2Ffrance24

M3U
^^^

  **Euronews**

  ::

    #EXTINF:-1 tvg-id="EURONEWS" group-title="English;News" tvg-logo="",Euronews
    http://127.0.0.1:53422/play/?url=https%253A%252F%252Fwww.euronews.com%252Flive

  **France24**

  ::

    #EXTINF:-1 tvg-id="France24" group-title="English;News" tvg-logo="",France24
    http://127.0.0.1:53422/play/?url=https%3A%2F%2Fwww.youtube.com%2Fuser%2Ffrance24


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

    #SERVICE 4097:0:1:0:0:0:0:0:0:0:http%3a//127.0.0.1%3a53422/play/?url=https%253A%252F%252Fwww.euronews.com%252Flive:Euronews
    #DESCRIPTION Euronews

  **France24**

  ::

    #SERVICE 4097:0:1:0:0:0:0:0:0:0:http%3a//127.0.0.1%3a53422/play/?url=https%3A%2F%2Fwww.youtube.com%2Fuser%2Ffrance24:France24
    #DESCRIPTION France24
