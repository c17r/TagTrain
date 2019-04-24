from tagtrain import data
from tagtrain.tagtrain import TagTrainResponse, C_GROUP


class Unlock(TagTrainResponse):
    CMD_REGEX = f'lock {C_GROUP}'
    HELP_TEXT = "`u/{botname} unlock <group-name>` - Unlocks the specified Group; others can add themselves."
    TYPE = TagTrainResponse.TYPE_COMMENTORMESSAGE

    def run(self, reply, message, match):
        self.LOGGER.debug('lock')
        owner_name = message.author.name
        group_name = match.group('group')

        try:
            data.by_owner.unlock_group(owner_name, group_name)

        except data.Group.DoesNotExist:
            reply.append(f'Group `{group_name}` does not exist.  Skipping.')
            return

        except data.by_owner.InvalidRequest:
            reply.append(f'Group `{group_name}` already unlocked.  Skipping.')
            return

        reply.append(f'Group `{group_name}` is now unlocked.')
