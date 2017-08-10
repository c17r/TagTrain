from datetime import datetime
from unittest.mock import MagicMock, patch
from tagtrain import data
from . import fake

from tagtrain.tagtrain.tt_lock import Lock


@patch('tagtrain.data.by_owner.lock_group')
def test_unknown_group(lock_group):
    lock_group.side_effect = data.Group.DoesNotExist()

    app, reply, message, match = fake.create_all()

    Lock(app).run(reply, message, match)

    lock_group.assert_called_once_with('AuthorName', 'GroupName')
    reply.append.assert_called_once_with('Group `GroupName` does not exist.  Skipping.')


@patch('tagtrain.data.by_owner.lock_group')
def test_already_locked(lock_group):
    lock_group.side_effect = data.by_owner.InvalidRequest()

    app, reply, message, match = fake.create_all()

    Lock(app).run(reply, message, match)

    lock_group.assert_called_once_with('AuthorName', 'GroupName')
    reply.append.assert_called_once_with('Group `GroupName` already locked.  Skipping.')


@patch('tagtrain.data.by_owner.lock_group')
def test_good(lock_group):
    group = fake.create_group(name='GroupName', member_count=1, locked=datetime.utcnow())
    lock_group.return_value = group

    app, reply, message, match = fake.create_all()

    Lock(app).run(reply, message, match)

    lock_group.assert_called_once_with('AuthorName', 'GroupName')
    reply.append.assert_called_once_with('Group `GroupName` is now locked.')
