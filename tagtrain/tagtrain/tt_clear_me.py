from .. import data
from . import TagTrainResponse, grouper, MEMBER_LIMIT


def _format_group(group):
    if not group:
        return ""
    return f'`{group.reddit_name}`\'s `{group.name}`'


class ClearMe(TagTrainResponse):
    CMD_REGEX = f'clearme'
    HELP_TEXT = "`U/TagTrain clearme` - Removes you from all Groups."
    TYPE = TagTrainResponse.TYPE_COMMENTORMESSAGE

    def run(self, reply, message, match):
        self.LOGGER.debug('clearme...')
        reddit_name = message.author.name

        groups = data.by_member.remove_from_all_groups(reddit_name)
        num_groups = len(groups)

        if not num_groups:
            reply.append(f'You are not a Member of any Groups.')
            return

        reply.append(f'You were removed as a Member from {num_groups} Groups.')
        reply.append('\n')
        reply.append(' | | | ')
        reply.append(' - | - | - ')
        for groupings in grouper(groups, MEMBER_LIMIT):
            reply.append(' | '.join([_format_group(g) for g in groupings]))
