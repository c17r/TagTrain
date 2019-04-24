from .. import data
from . import TagTrainResponse


def _format_line(group):
    return f'`{group.name}` | {group.member_count}'


class Groups(TagTrainResponse):
    CMD_REGEX = f'groups'
    HELP_TEXT = "`u/{botname} groups` - Displays name of all your Groups with count of Members."
    TYPE = TagTrainResponse.TYPE_COMMENTORMESSAGE

    def run(self, reply, message, match):
        self.LOGGER.debug('groups...')
        owner_name = message.author.name

        groups = list(data.by_owner.find_groups(owner_name))
        group_count = len(groups)

        if not group_count:
            reply.append('You have no Groups.')
            return

        reply.append('Groups | Member Counts')
        reply.append('------ | -------------')
        [reply.append(_format_line(g)) for g in groups]
