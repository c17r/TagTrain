from collections import defaultdict
from . import TagTrainResponse


class Help(TagTrainResponse):
    CMD_REGEX = f'(hello|help)'
    HELP_TEXT = "`u/TagTrain help` or `u/TagTrain hello` - this message"
    TYPE = TagTrainResponse.TYPE_COMMENTORMESSAGE

    MAIN_TEXT = """
TagTrain Bot, here to help you mass mention users in a Thread

- Groups are specific to a reddit user.
  - You can **NOT** use another reddit user's list.
  - You **CAN** add yourself to another reddit user's list.
  - You **CAN** remove yourself from another reddit user's list.
- Group names need to be unique per reddit user.
- Group names can not contain spaces.  Use dash, underscore, period, etc as a word separator.
- Members can be specified as `name`, `u/name`, or `/u/name`.
- A reddit user can (currently) have unlimited Groups.
- A Group can (currently) have unlimited Members.
- Multiple commands can be sent a single message.  Separate each with a blank line.
- Why not MentionTrain or MessageTrain? TagTrain is nicely alliterative.
- Questions/Comments? Message `/u/c17r`.
"""

    buckets = None

    bucket_order = [
        TagTrainResponse.TYPE_COMMENTORMESSAGE,
        TagTrainResponse.TYPE_MESSAGE,
        TagTrainResponse.TYPE_COMMENT
    ]

    def _create_buckets(self):
        if self.buckets:
            return
        self.buckets = defaultdict(list)
        [self.buckets[c.TYPE].append(c) for c in self.APP.cmds]

    def run(self, reply, message, match):
        self.LOGGER.debug('help...')

        self._create_buckets()

        reply.append(self.MAIN_TEXT)
        reply.append('\n')

        for bucket in self.bucket_order:
            cmds = self.buckets[bucket]
            if not cmds:
                continue

            reply.append('\n')
            reply.append('In a ' + self.TYPE_TEXT[bucket] + ':')
            reply.append('\n')

            for cmd in cmds:
                reply.append('- ' + cmd.HELP_TEXT)
