import datetime
import logging
import time
import traceback
import praw
import prawcore

_logger = logging.getLogger('reddit')


def _preface_each_line(text, preface):
    lines = text.split('\n')
    lines = [preface + line for line in lines]
    return '\n'.join(lines)


class Reply(object):
    body = None
    children = None
    last_child = None

    def __init__(self, msg=None):
        self.body = []
        self.children = []
        self.last_child = None
        if msg:
            self.append(msg)

    def __str__(self):
        sep = '-' * 20
        body = '\n'.join(self.body)
        children = ''
        for child in self.children:
            children += _preface_each_line(str(child), '\t\t')

        return f'''
{sep}
Body:
{body}

Children: {children}
{sep}
'''

    def prepend(self, msg):
        if not msg:
            return
        self.body.insert(0, msg)

    def append(self, msg):
        if not msg:
            return
        self.body.append(msg)

    def extend(self, msgs):
        if not msgs:
            return
        self.body.extend(msgs)

    def new_child(self, msg):
        if not msg:
            return
        self.last_child = child = Reply(msg)
        self.children.append(child)
        return child

    def append_last_child(self, msg):
        if not msg:
            return
        self.children[-1].append(msg)

    def prepend_last_child(self, msg):
        if not msg:
            return
        self.children[-1].prepend(msg)

    def has_text(self):
        if self.body or self.children:
            return True
        return False

    def process(self, message):
        body = '\n'.join(self.body)
        mine = message.reply(body)

        for child in self.children:
            child.process(mine)


class RedditStreamingEvents(object):
    config = None
    reddit = None
    process_func = None

    def __init__(self, config, process_func):
        self.config = config
        self.process_func = process_func

    def _create_reddit(self):
        _logger.debug('Creating reddit object...')
        self.reddit = praw.Reddit(**self.config['reddit'])

    def _get_data(self):
        _logger.debug('_get_data...')
        while True:
            try:
                yield from self._get_data_backlog()
                yield from self._get_data_stream()

            except KeyboardInterrupt:
                _logger.info('Shutdown requested, stopping...')
                raise

            except prawcore.exceptions.RequestException as e:
                _logger.error('Prawcore Exception: ' + str(e))
                time.sleep(2.0)
                self._create_reddit()

            except Exception as e:
                _logger.exception(f'--\n--\nUnplanned Exception: {e}\n--\n')
                self._create_reddit()

    def _get_data_backlog(self):
        messages = list(self.reddit.inbox.unread(limit=None))
        while messages:
            _logger.info('Processing backlog...')
            for msg in messages:
                yield msg
            messages = list(self.reddit.inbox.unread(limit=None))

    def _get_data_stream(self):
        _logger.info('Processing stream...')
        yield from self.reddit.inbox.stream()

    def _send_error_report(self, log, exc, stack):
        _logger.debug('_send_error_report...')
        lines = _preface_each_line(stack, '    ')
        self.reddit.redditor('c17r').message('TagTrain Exception', f'{log}\n\n{lines}')
        _logger.warning("Exception " + log)
        _logger.exception(exc)

    def valid_user(self, user_name):
        try:
            self.reddit.redditor(user_name).fullname
        except prawcore.exceptions.NotFound:
            return False

        return True

    def run(self):
        _logger.debug('run...')
        self._create_reddit()

        for message in self._get_data():
            if not message.new:
                _logger.info('Read message, skipping...')
                continue

            log = (
                f'Processing'
                f' {message.subreddit_name_prefixed if message.subreddit_name_prefixed else "Direct"} Comment'
                f' from {message.author.name}'
                f' sent {datetime.datetime.fromtimestamp(int(message.created_utc)).strftime("%Y-%m-%d %H:%M:%S")}'
                f' : {message.body}'
            )
            _logger.info(log)

            try:
                reply = self.process_func(self, message)
                if reply.has_text():
                    reply.process(message)
                    _logger.info('Reply sent...')
                else:
                    _logger.info('Empty reply, doing nothing...')

            except Exception as exc:
                stack = traceback.format_exc()
                self._send_error_report(log, exc, stack)

            finally:
                message.mark_read()
