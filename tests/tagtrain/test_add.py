from unittest.mock import MagicMock, patch
from . import fake

from tagtrain.tagtrain.tt_add import Add


@patch('tagtrain.data.by_owner.add_user_to_group')
def test_existing_member(add_user_to_group):
    add_user_to_group.return_value = (fake.create_group(name='GroupName'), False)

    app, reply, message, match = fake.create_all()

    Add(app).run(reply, message, match)

    add_user_to_group.assert_called_once_with('AuthorName', 'GroupName', 'MemberName')
    reply.append.assert_called_once_with('`MemberName` already Member of Group `GroupName`, skipping.')


@patch('tagtrain.data.by_owner.add_user_to_group')
def test_good_new_group(add_user_to_group):
    add_user_to_group.return_value = (fake.create_group(name='GroupName', member_count=1), True)

    app, reply, message, match = fake.create_all()

    Add(app).run(reply, message, match)

    add_user_to_group.assert_called_once_with('AuthorName', 'GroupName', 'MemberName')
    reply.append.assert_called_once_with('Group `GroupName` created with `MemberName` as the first Member.')


@patch('tagtrain.data.by_owner.add_user_to_group')
def test_good_existing_group(add_user_to_group):
    add_user_to_group.return_value = (fake.create_group(name='GroupName', member_count=2), True)

    app, reply, message, match = fake.create_all()

    Add(app).run(reply, message, match)

    add_user_to_group.assert_called_once_with('AuthorName', 'GroupName', 'MemberName')
    reply.append.assert_called_once_with('`MemberName` added to Group `GroupName`, 2 total Members.')
