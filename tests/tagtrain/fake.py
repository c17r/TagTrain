from unittest.mock import MagicMock


def create_app(regex='u/TagTrain '):
    app = MagicMock()
    regex = MagicMock(return_value=regex)
    app.R_INTRO = regex

    return app


def create_message(name='AuthorName'):
    message = MagicMock()
    author = MagicMock()
    author.configure_mock(name=name)
    message.author = author
    return message


def create_match(items=None):
    if not items:
        items = {
            'group': 'GroupName',
            'member': 'MemberName',
            'owner': 'OwnerName',
            'name': 'NewName',
        }

    def match_group(item):
        return items[item]

    match = MagicMock()
    match.group.side_effect = match_group
    return match


def create_reply():
    reply = MagicMock()
    return reply


def create_group(**kwargs):
    group = MagicMock()
    group.configure_mock(**kwargs)
    return group


def create_all():
    app = create_app()
    reply = create_reply()
    message = create_message()
    match = create_match()

    return app, reply, message, match
