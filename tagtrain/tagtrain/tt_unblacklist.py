from tagtrain import data
from tagtrain.tagtrain import TagTrainResponse, C_MEMBER, C_GROUP


class UnBlacklist(TagTrainResponse):
    TYPE = TagTrainResponse.TYPE_COMMENTORMESSAGE
    CMD_REGEX = f'unblacklist {C_MEMBER} {C_GROUP}?'
    HELP_TEXT = ("`u/{botname} unblacklist <member-name> [<group-name>]` - "
                 "Allows previously blacklisted specified Member to add themselves, either for all "
                 "your Groups or just specified Group")

    def run(self, reply, message, match):
        self.LOGGER.debug('blacklist')
        owner_name = message.author.name
        member_name = match.group('member')
        group_name = match.group('group')

        try:
            data.by_owner.unblacklist_user(owner_name, member_name, group_name)

        except data.Group.DoesNotExist:
            reply.append(f'Group `{group_name}` does not exist.  Skipping.')
            return

        except data.Blacklist.DoesNotExist:
            t = f'Group `{group_name}`' if group_name else 'Blanket'
            reply.append(t + f' Blacklist for Member `{member_name}` does not exist.  Skipping.')
            return

        t = f'Group `{group_name}`' if group_name else 'Blanket'
        reply.append(t + f' Blacklist for Member `{member_name}` removed.')
