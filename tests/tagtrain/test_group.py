from unittest.mock import MagicMock, patch, call
from tagtrain import data
from . import fake

from tagtrain.tagtrain.tt_group import Group


@patch('tagtrain.data.by_owner.find_group')
def test_unknown_group(find_group):
    find_group.side_effect = data.Group.DoesNotExist()

    app, reply, message, match = fake.create_all()

    Group(app).run(reply, message, match)

    find_group.assert_called_once_with('AuthorName', 'GroupName')
    reply.append.assert_called_once_with('Group `GroupName` does not exist.  Skipping.')


@patch('tagtrain.data.by_owner.find_group')
def test_good(find_group):
    find_group.return_value = fake.create_group(name='GroupName', member_count=4, members=[
        MagicMock(reddit_name='User1'),
        MagicMock(reddit_name='User2'),
        MagicMock(reddit_name='User3'),
        MagicMock(reddit_name='User4'),
    ])

    app, reply, message, match = fake.create_all()

    Group(app).run(reply, message, match)

    find_group.assert_called_once_with('AuthorName', 'GroupName')
    reply.append.assert_has_calls([
        call('Group `GroupName` has 4 Members:'),
        call('\n'),
        call(' | | | '),
        call(' - | - | - '),
        call('`User1` | `User2` | `User3`'),
        call('`User4` |  | '),
    ])
