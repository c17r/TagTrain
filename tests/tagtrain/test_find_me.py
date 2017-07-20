from unittest.mock import MagicMock, patch, call
from . import fake

from tagtrain.tagtrain.tt_find_me import FindMe


@patch('tagtrain.data.by_member.find_groups')
def test_no_groups(find_groups):
    find_groups.return_value = []

    app, reply, message, match = fake.create_all()

    FindMe(app).run(reply, message, match)

    find_groups.assert_called_once_with('AuthorName')
    reply.append.assert_called_once_with('You are not a Member of any Groups.')


@patch('tagtrain.data.by_member.find_groups')
def test_good(find_groups):
    find_groups.return_value = iter([
        fake.create_group(name='GroupName', reddit_name='RedditName')
    ])

    app, reply, message, match = fake.create_all()

    FindMe(app).run(reply, message, match)

    find_groups.assert_called_once_with('AuthorName')
    reply.append.assert_has_calls([
        call('You are a Member of 1 Groups.'),
        call('\n'),
        call(' | | | '),
        call(' - | - | - '),
        call("`RedditName`'s `GroupName` |  | "),
    ])
