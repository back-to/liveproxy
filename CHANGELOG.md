# Changelog

## 1.0.0

- Fixed bug - base64 TypeError: Incorrect padding
  see https://github.com/back-to/liveproxy/commit/3dbcc8550b8aa108a5d84fff2f96b722feb9ab2a
- Fixed Kodi Python3 encoding bug

## 0.3.0

### Added

- New command `--file-output`

### Changed

- requiere Streamlink version 1.1.1
- Dropped support for Python 3.4
- Removed streamlink_cli mirror files.

## 0.2.0

### Changed

- requiere Streamlink version 1.0.0
- fix if the stream quality name is invalid

## 0.1.1

### Changed

- if `--url` was used as an argument, it will be used instead of the nargs

## 0.1.0

### Added

- Improve Streamlink default Plugins load speed
- New commands `--file` and `--format` got added,
  they can create valid URLs from a file for the new base64 URL style.

### Changed

- Custom plugins with `from streamlink.plugin.api import http` are not allowed,
  use `self.session`
- The LiveProxy URL build was simplified, a Streamlink command like
  `streamlink https://www.youtube.com/user/france24 best`
  can be used after it got base64 encoded.
  URL example `http://127.0.0.1:53422/base64/c3RyZWFtbGluayBodHRwczovL3d3dy55b3V0dWJlLmNvbS91c2VyL2ZyYW5jZTI0IGJlc3Q=/`
  more details can be found on the website.

## 0.0.3

Skip 0.0.2 because it was used as a hotfix for E2.

### Added

- Allow FFmpeg and RTMP streams, they might not work on every platform,
  they work on Linux, but not on Windows for me.

  Don't use them if it doesn't work for you,
  this streamlink command can be used to disable them.
  https://streamlink.github.io/cli.html#cmdoption-stream-types

### Changed

- Streamlink version 0.14.0 is required
- Removed help text from mirror argparser
- Allow `/streamlink/` for `/path/` in URLs
- Allow `/streamlink_301/` for `/301/` in URLs
