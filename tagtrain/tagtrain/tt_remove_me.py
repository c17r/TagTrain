from .. import data
from . import TagTrainResponse, C_OWNER, C_GROUP


class RemoveMe(TagTrainResponse):
    CMD_REGEX = f'removeme from {C_OWNER} {C_GROUP}'
    HELP_TEXT = "`u/{botname} removeme from <user> <group-name>` - Removes yourself from specified User's Group"
    TYPE = TagTrainResponse.TYPE_COMMENTORMESSAGE

    def run(self, reply, message, match):
        self.LOGGER.debug('removeme...')
        member_name = message.author.name
        owner_name = match.group('owner')
        group_name = match.group('group')

        try:
            group = data.by_owner.remove_user_from_group(owner_name, group_name, member_name)
            member_count = group.member_count

        except data.Group.DoesNotExist:
            reply.append(f'User `{owner_name}` does not have a Group `{group_name}`, skipping.')
            return

        except data.Member.DoesNotExist:
            reply.append(f"You are not a Member of `{owner_name}`'s Group `{group_name}`, skipping.")
            return

        reply.append(f"You were removed from `{owner_name}`'s Group `{group_name}`, {member_count} total Members.")
