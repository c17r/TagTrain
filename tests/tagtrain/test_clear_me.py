from unittest.mock import MagicMock, patch, call
from . import fake

from tagtrain.tagtrain.tt_clear_me import ClearMe


@patch('tagtrain.data.by_member.remove_from_all_groups')
def test_no_groups(remove_from_all_groups):
    remove_from_all_groups.return_value = []

    app, reply, message, match = fake.create_all()

    ClearMe(app).run(reply, message, match)

    remove_from_all_groups.assert_called_once_with('AuthorName')
    reply.append.assert_called_once_with('You are not a Member of any Groups.')


@patch('tagtrain.data.by_member.remove_from_all_groups')
def test_good(remove_from_all_groups):
    remove_from_all_groups.return_value = [fake.create_group(name='GroupName', reddit_name='RedditName')]

    app, reply, message, match = fake.create_all()

    ClearMe(app).run(reply, message, match)

    remove_from_all_groups.assert_called_once_with('AuthorName')
    reply.append.assert_has_calls([
        call('You were removed as a Member from 1 Groups.'),
        call('\n'),
        call(' | | | '),
        call(' - | - | - '),
        call("`RedditName`'s `GroupName` |  | "),
    ])
