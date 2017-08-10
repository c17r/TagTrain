from .. import data
from . import TagTrainResponse, C_MEMBER, C_GROUP


class Add(TagTrainResponse):
    CMD_REGEX = f'add {C_MEMBER} to {C_GROUP}'
    HELP_TEXT = "`u/{botname} add <user> to <group-name>` - Adds specified reddit user to the specified Group."
    TYPE = TagTrainResponse.TYPE_COMMENTORMESSAGE

    def run(self, reply, message, match):
        self.LOGGER.debug('add...')
        owner_name = message.author.name
        group_name = match.group('group')
        member_name = match.group('member')

        group, created = data.by_owner.add_user_to_group(owner_name, group_name, member_name)

        if not created:
            reply.append(f'`{member_name}` already Member of Group `{group.name}`.  Skipping.')
            return

        if group.member_count == 1:
            reply.append(f'Group `{group.name}` created with `{member_name}` as the first Member.')
            return

        reply.append(f'`{member_name}` added to Group `{group.name}`, {group.member_count} total Members.')
