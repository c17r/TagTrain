import re
import logging
from itertools import zip_longest

from .. import data
from ..reddit import RedditStreamingProcessBase, Reply

USERNAME = 'TagTrain'
USERNAME_FULL = f'u/{USERNAME}'
MEMBER_LIMIT = 3

R_INTRO = f'(?:/?u/{USERNAME} )?'
C_GROUP = '(?:/?u/)?(?P<group>[^ ]+)'
C_MEMBER = '(?:/?u/)?(?P<member>[^ ]+)'
C_NAME = '(?:/?u/)?(?P<name>[^ ]+)'

R_GROUPS = ('groups', re.compile(f'^{R_INTRO}groups$'))
R_HELP = ('help', re.compile(f'^{R_INTRO}(hello|help)$'))
R_USE = ('use', re.compile(f'^{R_INTRO}use {C_GROUP}$'))
R_GROUP = ('group', re.compile(f'^{R_INTRO}group {C_GROUP}$'))
R_CLEAR = ('clear', re.compile(f'^{R_INTRO}clear {C_GROUP}$'))
R_ADD = ('add', re.compile(f'^{R_INTRO}add {C_MEMBER} to {C_GROUP}$'))
R_REMOVE = ('remove', re.compile(f'^{R_INTRO}remove {C_MEMBER} from {C_GROUP}$'))
R_RENAME = ('rename', re.compile(f'^{R_INTRO}rename {C_GROUP} to {C_NAME}$'))

R_ALL = [R_HELP, R_GROUPS, R_GROUP, R_ADD, R_REMOVE, R_USE, R_CLEAR, R_RENAME]

_logger = logging.getLogger('tagtrain')


def _grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


class TagTrain(RedditStreamingProcessBase):
    def __init__(self, db_path):
        data.init(db_path)

    def _find_command(self, message):
        _logger.debug('_find_command...')
        for n, r in R_ALL:
            for line in message.body.split('\n'):
                rv = r.search(line)
                if rv:
                    return n, rv
        return None, None

    def _reply_help(self, reply, message, match):
        _logger.debug('_reply_help...')
        reply.append(f"""
TagTrain Bot, here to help you mass mention users in a Thread

- Groups are specific to a reddit user.  You can not add/remove/use another reddit user's list.
- Group names need to be unique per reddit user.
- Group names can not contain spaces.  Use dash, underscore, period, etc as a word separator.
- Members can be specified as `name`, `u/name`, or `/u/name`.
- A reddit user can (currently) have unlimited Groups.
- A Group can (currently) have unlimited Members.
- Why not MentionTrain or MessageTrain? TagTrain is nicely alliterative.
- Questions/Comments? Message `/u/c17r`.

In a Comment or Message:

- `u/TagTrain help` or `u/TagTrain hello` - Displays this message.
- `u/TagTrain groups` - Displays name of all your Groups with count of Members.
- `u/TagTrain group <group-name>` - Displays all Members for specified Group.
- `u/TagTrain add <user> to <group-name>` - Adds specified reddit user to the specified Group.
- `u/TagTrain remove <user> to <group-name>` - Removes specified Member from the specified Group, if Group is now empty it is deleted.
- `u/TagTrain` clear <group-name> - Deletes specified Group and Members.
- `u/TagTrain` rename <group-name> to <new-name> - Renames specified Group.

In a Comment:

- `u/TagTrain use <group-name>` - Loops through Members of specified Group, mentioning {MEMBER_LIMIT} Members at a time.
""")  # noqa: E501

    def _reply_use(self, reply, message, match):
        _logger.debug('_reply_use...')
        owner_name = message.author.name
        group_name = match.group('group')

        try:
            group = data.find_group(owner_name, group_name)

            reply.append(f'Using Group `{group.name}` to notify {group.member_count} Members')
            for groupings in _grouper(group.members.iterator(), MEMBER_LIMIT):
                tmp = ', '.join([f'u/{member.reddit_name}' for member in groupings if member])
                reply.new_child(f'`{group.reddit_name}` used `TagTrain` Bot to mention you: {tmp}')

        except data.Group.DoesNotExist:
            reply.append(f'Group `{group_name}` does not exist, no Members.')

    def _reply_groups(self, reply, message, match):
        _logger.debug('_reply_groups...')
        owner_name = message.author.name

        groups = data.find_groups(owner_name)

        response = [f'`{g.name}` | {g.member_count}' for g in groups]
        if response:
            response.insert(0, 'Groups | Member Counts')
            response.insert(1, '------ | -------------')
            reply.append('\n'.join(response))
        else:
            reply.append('You have no Groups')

    def _reply_group(self, reply, message, match):
        _logger.debug('_reply_group...')
        owner_name = message.author.name
        group_name = match.group('group')

        try:
            group = data.find_group(owner_name, group_name)
            sorted_members = sorted(group.members, key=lambda x: x.reddit_name.lower())

            response = [
                f'Group `{group.name}` has {group.member_count} Members:',
                '\n'
                ' | | | ',
                ' - | - | - '
            ]
            for groupings in _grouper(sorted_members, MEMBER_LIMIT):
                response.append(' | '.join([f'{"`" + g.reddit_name + "`" if g else ""}' for g in groupings]))
            reply.append('\n'.join(response))

        except data.Group.DoesNotExist:
            reply.append(f'Group `{group_name}` does not exist, no Members.')

    def _reply_clear(self, reply, message, match):
        _logger.debug('_reply_clear')
        owner_name = message.author.name
        group_name = match.group('group')

        try:
            data.remove_group(owner_name, group_name)
            reply.append(f'Group `{group_name}` and all Members removed.')

        except data.Group.DoesNotExist:
            reply.append(f'Group`{group_name}` does not exist.')

    def _reply_add(self, reply, message, match):
        _logger.debug('_reply_add...')
        owner_name = message.author.name
        group_name = match.group('group')
        member_name = match.group('member')

        group, created = data.add_user_to_group(owner_name, group_name, member_name)
        if group.member_count == 1:
            reply.append(f'Group `{group.name}` created with `{member_name}` as the first Member.')
        else:
            if created:
                reply.append(f'`{member_name}` added to Group `{group.name}`, {group.member_count} total Members')
            else:
                reply.append(
                    f'`{member_name}` already Member of Group `{group.name}`, {group.member_count} total Members')

    def _reply_remove(self, reply, message, match):
        _logger.debug('_reply_remove...')
        owner_name = message.author.name
        group_name = match.group('group')
        member_name = match.group('member')

        try:
            group = data.remove_user_from_group(owner_name, group_name, member_name)
        except data.Group.DoesNotExist:
            reply.append(f'Group `{group_name}` does not exist, doing nothing')
            return
        except data.Member.DoesNotExist:
            reply.append(f'`{member_name}` not Member of Group `{group_name}`')
            return

        tmp = f'`{member_name}` removed from Group `{group.name}`, '
        if group.member_count > 0:
            tmp += f'{group.member_count} total Members'
        else:
            tmp += f'Group has no Members left so it was removed'
        reply.append(tmp)

    def _reply_rename(self, reply, message, match):
        _logger.debug('_reply_rename')
        owner_name = message.author.name
        group_name = match.group('group')
        new_name = match.group('name')

        try:
            data.rename_group(owner_name, group_name, new_name)
        except data.Group.DoesNotExist:
            reply.append(f'Group `{group_name}` does not exist, doing nothing')
            return

        reply.append(f'Group `{group_name}` renamed to `{new_name}`')

    def _reply_error(self, reply, message, match):
        _logger.debug('_reply_error...')
        reply.append('Sorry, unknown command. Showing help')
        self._reply_help(reply, message, match)

    def process(self, message):
        _logger.debug('process...')
        name, match = self._find_command(message)
        func = getattr(self, f'_reply_{name}', None)
        reply = Reply()
        if func:
            reply.append('>' + match.group(0))
            reply.append('\n')
            func(reply, message, match)
        else:
            self._reply_error(reply, message, None)
        _logger.debug('Reply is ' + str(reply))
        return reply
