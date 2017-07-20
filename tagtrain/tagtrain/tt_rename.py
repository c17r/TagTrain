from .. import data
from . import TagTrainResponse, C_GROUP, C_NAME


class Rename(TagTrainResponse):
    CMD_REGEX = f'rename {C_GROUP} to {C_NAME}'
    HELP_TEXT = "`u/TagTrain rename <group-name> to <new-name>` - Renames specified Group."
    TYPE = TagTrainResponse.TYPE_COMMENTORMESSAGE

    def run(self, reply, message, match):
        self.LOGGER.debug('rename...')
        owner_name = message.author.name
        group_name = match.group('group')
        new_name = match.group('name')

        try:
            data.by_owner.rename_group(owner_name, group_name, new_name)

        except data.Group.DoesNotExist:
            reply.append(f'Group `{group_name}` does not exist, skipping.')
            return

        reply.append(f'Group `{group_name}` renamed to `{new_name}`.')
