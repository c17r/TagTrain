from .. import data
from . import TagTrainResponse, C_OWNER, C_GROUP


class AddMe(TagTrainResponse):
    TYPE = TagTrainResponse.TYPE_COMMENTORMESSAGE
    CMD_REGEX = f'addme to {C_OWNER} {C_GROUP}'
    HELP_TEXT = "`u/{botname} addme to <user> <group-name>` - Adds yourself to the specified User's Group"

    def run(self, reply, message, match):
        self.LOGGER.debug('addme...')
        member_name = message.author.name
        owner_name = match.group('owner')
        group_name = match.group('group')
        permalink = message.permalink()

        try:
            # we first try to find it so it will throw an exception if it doesn't exist.  We don't want
            # someone creating a list that is owned by someone else.
            group = data.by_owner.find_group(owner_name, group_name)

            if group.locked:
                reply.append(f'Group `{group_name}` is locked.  Only `{owner_name}` can add you.  Skipping.')
                return

            group, created = data.by_member.add_user_to_group(owner_name, group_name, member_name, permalink)

        except data.Group.DoesNotExist:
            reply.append(f'User `{owner_name}` does not have a Group `{group_name}`.  Skipping.')
            return

        except data.by_member.Blacklisted:
            reply.append(f'You are Blacklisted from adding yourself to Group `{group_name}`.  Skipping.')
            return

        if not created:
            reply.append(f"You are already a Member of `{owner_name}`'s Group `{group_name}`.  Skipping.")
            return

        reply.append(f"You were added to `{owner_name}`'s Group `{group_name}`, {group.member_count} total Members.")
