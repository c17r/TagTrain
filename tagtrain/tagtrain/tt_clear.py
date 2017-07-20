from .. import data
from . import TagTrainResponse, C_GROUP


class Clear(TagTrainResponse):
    CMD_REGEX = f'clear {C_GROUP}'
    HELP_TEXT = "`u/{botname} clear <group-name>` - Deletes specified Group and Members."
    TYPE = TagTrainResponse.TYPE_COMMENTORMESSAGE

    def run(self, reply, message, match):
        self.LOGGER.debug('clear...')
        owner_name = message.author.name
        group_name = match.group('group')

        try:
            data.by_owner.remove_group(owner_name, group_name)

        except data.Group.DoesNotExist:
            reply.append(f'Group `{group_name}` does not exist, skipping.')
            return

        reply.append(f'Group `{group_name}` and all Members removed.')
