# LiveProxy

LiveProxy can redirect Livestreams to your favorite player on a lot of devices.

- Issue Tracker: https://github.com/back-to/liveproxy/issues
- Github: https://github.com/back-to/liveproxy

# INSTALLATION

## pip as user

```sh
# Latest pip version:
python3 -m pip install --upgrade liveproxy

# Latest dev version:
python3 -m pip install --upgrade git+https://github.com/back-to/liveproxy.git
```

## pip as root

```sh
# Latest pip version:
sudo -H python3 -m pip install --upgrade liveproxy

# Latest dev version:
sudo -H python3 -m pip install --upgrade git+https://github.com/back-to/liveproxy.git
```

## source

```text
git clone https://github.com/back-to/liveproxy.git
cd liveproxy
python3 setup.py install
```

# URL-GUIDE

## Tutorial

First, start LiveProxy on your system.

```text
$ liveproxy
[main][INFO] For LiveProxy support visit https://github.com/back-to/liveproxy
[main][INFO] Starting server: 127.0.0.1 on port 53422
```

host and port can be changed with `--host` / `--port`

```text
$ liveproxy --host 0.0.0.0 --port 12345
[main][INFO] For LiveProxy support visit https://github.com/back-to/liveproxy
[main][INFO] Starting server: 0.0.0.0 on port 12345
```

Now that LiveProxy is running, you will have to create a valid URL.

For the examples here, ``53422`` is used as **default port**.

## Base64

You will need to base64 encode your used commands.

#### Streamlink

```text
http://127.0.0.1:53422/base64/STREAMLINK-COMMANDS/
```

Example for `streamlink https://www.youtube.com/user/france24/live best`

```text
http://127.0.0.1:53422/base64/c3RyZWFtbGluayBodHRwczovL3d3dy55b3V0dWJlLmNvbS91c2VyL2ZyYW5jZTI0L2xpdmUgYmVzdA==/
```

#### Youtube-DL

```text
http://127.0.0.1:53422/base64/YOUTUBE-DL-COMMANDS/
```

Example for `youtube-dl https://www.youtube.com/user/france24/live`

```text
http://127.0.0.1:53422/base64/eW91dHViZS1kbCBodHRwczovL3d3dy55b3V0dWJlLmNvbS91c2VyL2ZyYW5jZTI0L2xpdmU=/
```

#### YT-DLP

```text
http://127.0.0.1:53422/base64/YT-DLP-COMMANDS/
```

Example for `yt-dlp https://www.youtube.com/user/france24/live`

```text
http://127.0.0.1:53422/base64/eXQtZGxwIGh0dHBzOi8vd3d3LnlvdXR1YmUuY29tL3VzZXIvZnJhbmNlMjQvbGl2ZQ==/
```

### LiveProxy-Command

LiveProxy can create this URL automatically.

Create a new file with your commands.

```text
#EXTM3U
#EXTINF:-1,Arte FR
streamlink https://www.arte.tv/fr/direct/ 720p,720p_alt,best
#EXTINF:-1,France24
streamlink https://www.youtube.com/user/france24/live best
#EXTINF:-1 tvg-id="EuroNews" tvg-name="EuroNews",Euronews
streamlink https://www.euronews.com/live best
#EXTINF:-1,France24 YOUTUBE-DL
youtube-dl https://www.youtube.com/user/france24/live
#EXTINF:-1,France24 YT-DLP
yt-dlp https://www.youtube.com/user/france24/live
```

For this example the filename is `example.m3u`

```text
liveproxy --file example.m3u
```

It will create a new file `example.m3u.new` with valid URLs,
only lines with `streamlink`, `youtube-dl`, `youtube_dl`, `yt-dlp` or `yt_dlp` at the start will be changed.

```text
#EXTM3U
#EXTINF:-1,Arte FR
http://127.0.0.1:53422/base64/c3RyZWFtbGluayBodHRwczovL3d3dy5hcnRlLnR2L2ZyL2RpcmVjdC8gNzIwcCw3MjBwX2FsdCxiZXN0/
#EXTINF:-1,France24
http://127.0.0.1:53422/base64/c3RyZWFtbGluayBodHRwczovL3d3dy55b3V0dWJlLmNvbS91c2VyL2ZyYW5jZTI0L2xpdmUgYmVzdA==/
#EXTINF:-1 tvg-id="EuroNews" tvg-name="EuroNews",Euronews
http://127.0.0.1:53422/base64/c3RyZWFtbGluayBodHRwczovL3d3dy5ldXJvbmV3cy5jb20vbGl2ZSBiZXN0/
#EXTINF:-1,France24 YOUTUBE-DL
http://127.0.0.1:53422/base64/eW91dHViZS1kbCBodHRwczovL3d3dy55b3V0dWJlLmNvbS91c2VyL2ZyYW5jZTI0L2xpdmU=/
#EXTINF:-1,France24 YT-DLP
http://127.0.0.1:53422/base64/eXQtZGxwIGh0dHBzOi8vd3d3LnlvdXR1YmUuY29tL3VzZXIvZnJhbmNlMjQvbGl2ZQ==/
```

You can also use ``--file-output`` for a specified new file,
but be careful don't overwrite any important files.

```text
liveproxy --file example.m3u --file-output my_file.m3u
```
