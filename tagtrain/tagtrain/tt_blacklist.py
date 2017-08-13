from tagtrain import data
from tagtrain.tagtrain import TagTrainResponse, C_MEMBER, C_GROUP


class Blacklist(TagTrainResponse):
    TYPE = TagTrainResponse.TYPE_COMMENTORMESSAGE
    CMD_REGEX = f'blacklist {C_MEMBER} {C_GROUP}?'
    HELP_TEXT = ("`u/{botname} blacklist <member-name> [<group-name>]` - "
                 "Prevents specified Member from adding themselves, either for all "
                 "your Groups or just specified Group")

    def run(self, reply, message, match):
        self.LOGGER.debug('blacklist')
        owner_name = message.author.name
        member_name = match.group('member')
        group_name = match.group('group')
        permalink = message.permalink()

        try:
            blacklist, created = data.by_owner.blacklist_user(owner_name, member_name, permalink, group_name)

        except data.Group.DoesNotExist:
            reply.append(f'Group `{group_name}` does not exist.  Skipping.')
            return

        except data.by_owner.BlanketBlackList:
            reply.append(f'Blanket Blacklist for `{member_name}` exists.  Skipping.')
            return

        if not created:
            reply.append(f'Group `{group_name}` Blacklist for `{member_name}` exists.  Skipping.')
            return

        t = f'Group `{group_name}`' if group_name else 'Blanket'
        reply.append(t + f' Blacklist for `{member_name}` created.')
