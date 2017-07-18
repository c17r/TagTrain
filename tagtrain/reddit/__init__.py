import datetime
import logging
import time
import traceback
import praw
import prawcore

_logger = logging.getLogger('reddit')


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
            children += '\n'.join(['\t\t' + line for line in str(child).split('\n')])

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

    def process(self, message):
        body = '\n'.join(self.body)
        mine = message.reply(body)

        for child in self.children:
            child.process(mine)


class RedditStreamingEvents(object):
    config = None
    reddit = None
    process_object = None

    def __init__(self, config, process_object):
        self.config = config
        self.process_object = process_object

    def _create_reddit(self):
        _logger.debug('Creating reddit object...')
        self.reddit = praw.Reddit(**self.config)

    def _get_data(self):
        while True:
            try:
                yield from self._get_data_inner()
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

    def _get_data_inner(self):
        while True:
            messages = list(self.reddit.inbox.unread(limit=None))
            if not messages:
                break

            _logger.info('Processing backlog...')
            for msg in messages:
                yield msg

        _logger.info('Processing stream...')
        for msg in self.reddit.inbox.stream():
            yield msg

    def _process_event(self, message):
        return self.process_object.process(message)

    def _send_error_report(self, log, exc, stack):
        lines = '\n'.join([f'    {line}' for line in stack.split('\n')])
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
                reply = self.process_object.process(self, message)
                reply.process(message)
                _logger.info('Reply sent...')
            except Exception as exc:
                stack = traceback.format_exc()
                self._send_error_report(log, exc, stack)
            finally:
                message.mark_read()


class RedditStreamingEventsTest(RedditStreamingEvents):
    def _reply(self, message, reply):
        print(f"""
----
Original Message:
{message.body}
--
Our Reply:
{reply}
----""")


class RedditStreamingProcessBase(object):
    def process(self, RSE, message):
        raise NotImplementedError('Base Class')
