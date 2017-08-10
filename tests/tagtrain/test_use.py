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
        call('`OwnerName` used `TagTrain` Bot to mention you: u/User1, u/User2, u/User3'),
        call('`OwnerName` used `TagTrain` Bot to mention you: u/User4'),
    ])
