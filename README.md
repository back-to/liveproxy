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

## CMD

If needed, you can use `quote` for special characters
https://docs.python.org/3/library/urllib.parse.html#urllib.parse.quote

```text
http://127.0.0.1:53422/cmd/COMMANDS/
```

Example for `streamlink https://www.youtube.com/user/france24/live best`

```text
http://127.0.0.1:53422/cmd/streamlink https://www.youtube.com/user/france24/live best/
```

Example for `yt-dlp https://www.youtube.com/user/france24/live`

```text
http://127.0.0.1:53422/cmd/yt-dlp https://www.youtube.com/user/france24/live/
```

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
