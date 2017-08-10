from datetime import datetime
from unittest.mock import MagicMock, patch
from tagtrain import data
from . import fake

from tagtrain.tagtrain.tt_add_me import AddMe


@patch('tagtrain.data.by_owner.add_user_to_group')
@patch('tagtrain.data.by_owner.find_group')
def test_unknown_group(find_group, add_user_to_group):
    find_group.side_effect = data.Group.DoesNotExist()

    app, reply, message, match = fake.create_all()

    AddMe(app).run(reply, message, match)

    find_group.assert_called_once_with('OwnerName', 'GroupName')
    add_user_to_group.assert_not_called()
    reply.append.assert_called_once_with('User `OwnerName` does not have a Group `GroupName`.  Skipping.')


@patch('tagtrain.data.by_owner.add_user_to_group')
@patch('tagtrain.data.by_owner.find_group')
def test_existing_member(find_group, add_user_to_group):
    group = fake.create_group(name='GroupName', member_count=1, locked=None)
    find_group.return_value = group
    add_user_to_group.return_value = (group, False)

    app, reply, message, match = fake.create_all()

    AddMe(app).run(reply, message, match)

    find_group.assert_called_once_with('OwnerName', 'GroupName')
    add_user_to_group.assert_called_once_with('OwnerName', 'GroupName', 'AuthorName')
    reply.append.assert_called_once_with("You are already a Member of `OwnerName`'s Group `GroupName`.  Skipping.")


@patch('tagtrain.data.by_owner.add_user_to_group')
@patch('tagtrain.data.by_owner.find_group')
def test_group_locked(find_group, add_user_to_group):
    group = fake.create_group(name='GroupName', member_count=1, locked=datetime.utcnow())
    find_group.return_value = group
    add_user_to_group.return_value = (group, False)

    app, reply, message, match = fake.create_all()

    AddMe(app).run(reply, message, match)

    find_group.assert_called_once_with('OwnerName', 'GroupName')
    add_user_to_group.assert_not_called()
    reply.append.assert_called_once_with("Group `GroupName` is locked.  Only `OwnerName` can add you.  Skipping.")


@patch('tagtrain.data.by_owner.add_user_to_group')
@patch('tagtrain.data.by_owner.find_group')
def test_good(find_group, add_user_to_group):
    group = fake.create_group(name='GroupName', member_count=1, locked=None)
    find_group.return_value = group
    add_user_to_group.return_value = (group, True)

    app, reply, message, match = fake.create_all()

    AddMe(app).run(reply, message, match)

    find_group.assert_called_once_with('OwnerName', 'GroupName')
    add_user_to_group.assert_called_once_with('OwnerName', 'GroupName', 'AuthorName')
    reply.append.assert_called_once_with("You were added to `OwnerName`'s Group `GroupName`, 1 total Members.")
