from tagtrain import data
from tagtrain.tagtrain import TagTrainResponse, C_GROUP


class Create(TagTrainResponse):
    TYPE = TagTrainResponse.TYPE_COMMENTORMESSAGE
    CMD_REGEX = f'create {C_GROUP}'
    HELP_TEXT = "`u/{botname} create <group-name>` - Creates the specified Group with no Members"

    def run(self, reply, message, match):
        self.LOGGER.debug('create')
        owner_name = message.author.name
        group_name = match.group('group')

        group, created = data.by_owner.create_group(owner_name, group_name)

        if not created:
            reply.append(f'Group `{group_name}` already exists.  Skipping.')
            return

        reply.append(f'Group `{group_name}` created, no Members.')
