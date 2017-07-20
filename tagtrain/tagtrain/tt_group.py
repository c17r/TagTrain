from .. import data
from . import TagTrainResponse, C_GROUP, grouper, MEMBER_LIMIT


def _format_member(member):
    if not member:
        return ""
    return f'`{member.reddit_name}`'


class Group(TagTrainResponse):
    CMD_REGEX = f'group {C_GROUP}'
    HELP_TEXT = "`u/{botname} group <group-name>` - Displays all Members for specified Group."
    TYPE = TagTrainResponse.TYPE_COMMENTORMESSAGE

    def run(self, reply, message, match):
        self.LOGGER.debug('group...')
        owner_name = message.author.name
        group_name = match.group('group')

        try:
            group = data.by_owner.find_group(owner_name, group_name)

        except data.Group.DoesNotExist:
            reply.append(f'Group `{group_name}` does not exist, skipping.')
            return

        sorted_members = sorted(group.members, key=lambda x: x.reddit_name.lower())

        reply.append(f'Group `{group.name}` has {group.member_count} Members:')
        reply.append('\n')
        reply.append(' | | | ')
        reply.append(' - | - | - ')

        for groupings in grouper(sorted_members, MEMBER_LIMIT):
            reply.append(' | '.join([_format_member(m) for m in groupings]))
