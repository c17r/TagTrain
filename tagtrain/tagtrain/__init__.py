import inspect
import logging
import os
import re
from importlib import import_module
from itertools import zip_longest

from ..reddit import Reply

MEMBER_LIMIT = 3

C_GROUP = '(?P<group>[^ ]+)'
C_NAME = '(?P<name>[^ ]+)'
C_MEMBER = '(?:/?u/)?(?P<member>[^ ]+)'
C_OWNER = '(?:/?u/)?(?P<owner>[^ ]+)'


_logger = logging.getLogger('tagtrain')


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def _get_commands(validate_func):
    _logger.debug('_get_commands...')

    path = os.path.dirname(os.path.abspath(__file__))
    files = ('.' + file[:-3] for file in os.listdir(path) if file.startswith('tt_') and file.endswith('.py'))

    for mod in [import_module(file, 'tagtrain.tagtrain') for file in files]:
        for name, obj in inspect.getmembers(mod):
            if validate_func(name, obj):
                yield name, obj


class TagTrain(object):
    config = None
    cmds = None
    R_INTRO = None

    def __init__(self, config):
        self.config = config
        self._init_intro()
        self._init_commands()

    def __call__(self, RSE, message):
        _logger.debug('process...')

        reply = Reply()
        for func, match in self._parse_commands(message):
            if reply.has_text():
                reply.append('\n&nbsp;\n')

            reply.append(f'\n> {match.group(0)}\n')
            if func:
                if self._check_valid_redditor(RSE, reply, match):
                    func(reply, message, match)

        _logger.debug(f'Reply is {reply}')
        return reply

    def _check_valid_redditor(self, RSE, reply, match):
        if not self.config['validate_username']:
            return True

        try:
            user = match.group('member')
        except IndexError:
            return True

        if RSE.valid_user(user):
            return True

        reply.append(f'`{user}` is not a valid Reddit user, skipping.')
        return False

    def _init_intro(self):
        self.R_INTRO = f'(?:/?u/{self.config["reddit"]["username"]} )?'

    def _init_commands(self):
        _logger.debug('_init_commands')

        existing_regex = set()
        valid_types = {
            TagTrainResponse.TYPE_COMMENT,
            TagTrainResponse.TYPE_MESSAGE,
            TagTrainResponse.TYPE_COMMENTORMESSAGE,
        }

        def validate(name, obj):
            if not inspect.isclass(obj):
                return False
            mro = obj.mro()
            if TagTrainResponse not in mro or mro.index(TagTrainResponse) == 0:
                return False
            regex = obj.CMD_REGEX
            if regex in existing_regex:
                _logger.warning(f'Command {name} using existing regex, skipping')
                return False
            existing_regex.add(regex)
            if obj.TYPE not in valid_types:
                _logger.warning(f'Command {name} not valid type, skipping')
                return False
            if not obj.HELP_TEXT:
                _logger.warning(f'Command {name} missing help text, skipping')
                return False

            return True

        self.cmds = [cls(self) for _, cls in _get_commands(validate)]
        _logger.info(f'{len(self.cmds)} commands loaded')

    def _parse_commands(self, message):
        _logger.debug('_parse_commands...')

        for line in message.body.split('\n'):
            for cmd in self.cmds:
                rv = cmd.search(line)
                if rv:
                    yield cmd, rv


class TagTrainResponse(object):
    TYPE_MESSAGE = 1
    TYPE_COMMENT = 2
    TYPE_COMMENTORMESSAGE = 3

    TYPE_TEXT = {
        TYPE_COMMENT: 'Comment',
        TYPE_MESSAGE: 'Message',
        TYPE_COMMENTORMESSAGE: 'Comment or Message',
    }

    CMD_REGEX = None
    HELP_TEXT = None
    TYPE = None

    LOGGER = _logger
    APP = None

    def __init__(self, app):
        self.APP = app
        self._init_regex()

    def __call__(self, reply, message, match):
        if not self._valid_type(reply, message):
            return

        return self.run(reply, message, match)

    def _init_regex(self):
        if self.CMD_REGEX:
            regex = self.CMD_REGEX
            self.CMD_REGEX = re.compile(f'^{self.APP.R_INTRO}{regex}$', re.I)

    def _valid_type(self, reply, message):
        msg_type = TagTrainResponse.TYPE_COMMENT if message.subreddit else TagTrainResponse.TYPE_MESSAGE

        if self.TYPE == msg_type:
            return True
        if self.TYPE == self.TYPE_COMMENTORMESSAGE and msg_type in {self.TYPE_MESSAGE, self.TYPE_COMMENT}:
            return True

        reply.append(f'Command can not be used in a {self.TYPE_TEXT[msg_type]}, skipping.')
        return False

    def search(self, line):
        if self.CMD_REGEX:
            return self.CMD_REGEX.search(line)

    def run(self, reply, message, match):
        raise NotImplementedError('Base Class')
