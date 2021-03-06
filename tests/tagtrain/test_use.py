from unittest.mock import MagicMock, patch, call
from tagtrain import data
from . import fake

from tagtrain.tagtrain.tt_use import Use


@patch('tagtrain.data.by_owner.find_group')
def test_unknown_group(find_group):
    find_group.side_effect = data.Group.DoesNotExist()

    app, reply, message, match = fake.create_all()

    Use(app).run(reply, message, match)

    find_group.assert_called_once_with('AuthorName', 'GroupName')
    reply.append.assert_called_once_with('Group `GroupName` does not exist.  Skipping.')


@patch('tagtrain.data.by_owner.find_group')
def test_zero_members(find_group):
    group = fake.create_group(name='GroupName', reddit_name='OwnerName', member_count=0)
    group.members.iterator.return_value = []
    find_group.return_value = group

    app, reply, message, match = fake.create_all()

    Use(app).run(reply, message, match)

    find_group.assert_called_once_with('AuthorName', 'GroupName')
    reply.append.assert_called_once_with('Group `GroupName` has no Members.  Skipping.')


@patch('tagtrain.data.by_owner.find_group')
def test_good(find_group):
    group = fake.create_group(name='GroupName', reddit_name='OwnerName', member_count=4)
    group.members.iterator.return_value = iter([
        MagicMock(reddit_name='User1'),
        MagicMock(reddit_name='User2'),
        MagicMock(reddit_name='User3'),
        MagicMock(reddit_name='User4'),
    ])
    find_group.return_value = group

    app, reply, message, match = fake.create_all()

    Use(app).run(reply, message, match)

    find_group.assert_called_once_with('AuthorName', 'GroupName')
    reply.append.assert_called_once_with('Using Group `GroupName` to notify 4 Members.')
    reply.new_child.assert_has_calls([
        call('`OwnerName` used Group `GroupName` to mention you: u/User1, u/User2, u/User3\n\n---\nIf you no longer want to receive messages from this Group, reply to this comment with (no quotes): `removeme from OwnerName GroupName`'),
        call('`OwnerName` used Group `GroupName` to mention you: u/User4\n\n---\nIf you no longer want to receive messages from this Group, reply to this comment with (no quotes): `removeme from OwnerName GroupName`'),
    ])
