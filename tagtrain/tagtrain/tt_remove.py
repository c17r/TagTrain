from .. import data
from . import TagTrainResponse, C_MEMBER, C_GROUP


class Remove(TagTrainResponse):
    CMD_REGEX = f'remove {C_MEMBER} from {C_GROUP}'
    HELP_TEXT = ("`u/{botname} remove <user> to <group-name>` - "
                 "Removes specified Member from the specified Group, if Group is now empty it is deleted.")
    TYPE = TagTrainResponse.TYPE_COMMENTORMESSAGE

    def run(self, reply, message, match):
        self.LOGGER.debug('remove...')
        owner_name = message.author.name
        group_name = match.group('group')
        member_name = match.group('member')

        try:
            group = data.by_owner.remove_user_from_group(owner_name, group_name, member_name)

        except data.Group.DoesNotExist:
            reply.append(f'Group `{group_name}` does not exist, skipping.')
            return

        except data.Member.DoesNotExist:
            reply.append(f'`{member_name}` is not a Member of Group `{group_name}`, skipping.')
            return

        tmp = f'`{member_name}` removed from Group `{group.name}`, '
        if group.member_count > 0:
            tmp += f'{group.member_count} total Members.'
        else:
            tmp += f'Group has no Members left so it was removed.'
        reply.append(tmp)
