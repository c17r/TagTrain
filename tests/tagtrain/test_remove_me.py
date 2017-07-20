from unittest.mock import MagicMock, patch, call
from tagtrain import data
from . import fake

from tagtrain.tagtrain.tt_remove_me import RemoveMe


@patch('tagtrain.data.by_owner.remove_user_from_group')
def test_unknown_group(remove_user_from_group):
    remove_user_from_group.side_effect = data.Group.DoesNotExist()

    app, reply, message, match = fake.create_all()

    RemoveMe(app).run(reply, message, match)

    remove_user_from_group.assert_called_once_with('OwnerName', 'GroupName', 'AuthorName')
    reply.append.assert_called_once_with('User `OwnerName` does not have a Group `GroupName`, skipping.')


@patch('tagtrain.data.by_owner.remove_user_from_group')
def test_unknown_member(remove_user_from_group):
    remove_user_from_group.side_effect = data.Member.DoesNotExist()

    app, reply, message, match = fake.create_all()

    RemoveMe(app).run(reply, message, match)

    remove_user_from_group.assert_called_once_with('OwnerName', 'GroupName', 'AuthorName')
    reply.append.assert_called_once_with("You are not a Member of `OwnerName`'s Group `GroupName`, skipping.")


@patch('tagtrain.data.by_owner.remove_user_from_group')
def test_good(remove_user_from_group):
    remove_user_from_group.return_value = fake.create_group(name='GroupName', member_count=99)

    app, reply, message, match = fake.create_all()

    RemoveMe(app).run(reply, message, match)

    remove_user_from_group.assert_called_once_with('OwnerName', 'GroupName', 'AuthorName')
    reply.append.assert_called_once_with("You were removed from `OwnerName`'s Group `GroupName`, 99 total Members.")
