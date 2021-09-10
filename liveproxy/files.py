import base64
import codecs
import logging
import os

from liveproxy.argparser import FILE_OUTPUT_LIST

log = logging.getLogger(__name__.replace('liveproxy.', ''))


def create_file(args):
    HOST = str(args.host)
    PORT = int(args.port)

    if not os.path.isfile(args.file):
        log.error('File does not exist: {0}'.format(args.file))
        return
    elif not os.access(args.file, os.F_OK):
        log.error('Can\'t read file: {0}'.format(args.file))
        return

    if args.format == 'm3u':
        URL_TEMPLATE = 'http://{host}:{port}/base64/{base64}/'
        # %3a
    elif args.format == 'e2':
        URL_TEMPLATE = 'http%3a//{host}%3a{port}/base64/{base64}/'
    else:
        return

    new_lines = []
    log.info('open old file: {0}'.format(args.file))
    with codecs.open(args.file, 'r', 'utf-8') as temp:
        text = temp.read()
        for line in text.splitlines():
            if line.startswith(('streamlink', 'youtube-dl', 'youtube_dl', 'yt-dlp', 'yt_dlp')):
                line = URL_TEMPLATE.format(
                    host=HOST,
                    port=PORT,
                    base64=base64.urlsafe_b64encode(line.encode('utf-8')).decode('utf-8'),
                )
            new_lines.append(line)

    if args.file_output:
        new_file = args.file_output
    else:
        new_file = args.file + '.new'

    if args.file == new_file:
        log.warning('Don\'t use the same name for the old and the new file.')
        return

    if not new_file.endswith(tuple(FILE_OUTPUT_LIST)):
        log.error(f'Invalid file type: {new_file}')
        return

    log.info('open new file: {0}'.format(new_file))
    with codecs.open(new_file, 'w', 'utf-8') as new_temp:
        for line in new_lines:
            new_temp.write(line + '\n')

    log.info('Done.')


__all__ = ('create_file')
