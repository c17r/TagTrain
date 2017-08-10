from datetime import datetime
from unittest.mock import MagicMock, patch
from tagtrain import data
from . import fake

from tagtrain.tagtrain.tt_unlock import Unlock


@patch('tagtrain.data.by_owner.unlock_group')
def test_unknown_group(unlock_group):
    unlock_group.side_effect = data.Group.DoesNotExist()

    app, reply, message, match = fake.create_all()

    Unlock(app).run(reply, message, match)

    unlock_group.assert_called_once_with('AuthorName', 'GroupName')
    reply.append.assert_called_once_with('Group `GroupName` does not exist.  Skipping.')


@patch('tagtrain.data.by_owner.unlock_group')
def test_already_locked(unlock_group):
    unlock_group.side_effect = data.by_owner.InvalidRequest()

    app, reply, message, match = fake.create_all()

    Unlock(app).run(reply, message, match)

    unlock_group.assert_called_once_with('AuthorName', 'GroupName')
    reply.append.assert_called_once_with('Group `GroupName` already unlocked.  Skipping.')


@patch('tagtrain.data.by_owner.unlock_group')
def test_good(unlock_group):
    group = fake.create_group(name='GroupName', member_count=1, locked=None)
    unlock_group.return_value = group

    app, reply, message, match = fake.create_all()

    Unlock(app).run(reply, message, match)

    unlock_group.assert_called_once_with('AuthorName', 'GroupName')
    reply.append.assert_called_once_with('Group `GroupName` is now unlocked.')
