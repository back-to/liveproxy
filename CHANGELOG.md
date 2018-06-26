# Changelog

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
