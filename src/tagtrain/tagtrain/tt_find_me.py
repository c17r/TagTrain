from .. import data
from . import TagTrainResponse, grouper, MEMBER_LIMIT


def _format_group(group):
    if not group:
        return ""
    return f'`{group.reddit_name}`\'s `{group.name}`'


class FindMe(TagTrainResponse):
    CMD_REGEX = f'findme'
    HELP_TEXT = "`u/{botname} findme` - Lists all Groups that you are a Member of."
    TYPE = TagTrainResponse.TYPE_COMMENTORMESSAGE

    def run(self, reply, message, match):
        self.LOGGER.debug('findme...')
        reddit_name = message.author.name

        groups = list(data.by_member.find_groups(reddit_name))
        num_groups = len(groups)

        if not num_groups:
            reply.append(f'You are not a Member of any Groups.')
            return

        reply.append(f'You are a Member of {num_groups} Groups.')
        reply.append('\n')
        reply.append(' | | | ')
        reply.append(' - | - | - ')
        for groupings in grouper(groups, MEMBER_LIMIT):
            reply.append(' | '.join([_format_group(g) for g in groupings]))
