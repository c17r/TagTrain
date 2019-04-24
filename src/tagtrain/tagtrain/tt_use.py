from .. import data
from . import TagTrainResponse, grouper, C_GROUP, MEMBER_LIMIT


class Use(TagTrainResponse):
    TYPE = TagTrainResponse.TYPE_COMMENT
    CMD_REGEX = f'use {C_GROUP}'
    HELP_TEXT = ("`u/{botname} use <group-name>` - "
                 f"Loops through Members of specified Group, mentioning {MEMBER_LIMIT} Members at a time.")

    def run(self, reply, message, match):
        self.LOGGER.debug('use...')
        owner_name = message.author.name
        group_name = match.group('group')

        try:
            group = data.by_owner.find_group(owner_name, group_name)

        except data.Group.DoesNotExist:
            reply.append(f'Group `{group_name}` does not exist.  Skipping.')
            return

        if group.member_count == 0:
            reply.append(f'Group `{group_name}` has no Members.  Skipping.')
            return

        reply.append(f'Using Group `{group.name}` to notify {group.member_count} Members.')
        for groupings in grouper(group.members.iterator(), MEMBER_LIMIT):
            tmp = ', '.join([f'u/{member.reddit_name}' for member in groupings if member])

            msg = (
                f"`{group.reddit_name}` used Group `{group.name}` to mention you: {tmp}\n"
                f"\n"
                f"---\n"
                f"If you no longer want to receive messages from this Group, "
                f"reply to this comment with (no quotes): "
                f"`removeme from {group.reddit_name} {group.name}`"
            )
            reply.new_child(msg)
