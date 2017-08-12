from datetime import datetime
from unittest.mock import MagicMock, patch
from tagtrain import data
from . import fake

from tagtrain.tagtrain.tt_create import Create


@patch('tagtrain.data.by_owner.create_group')
def test_existing(create_group):
    group = fake.create_group(name='GroupName', member_count=1)
    create_group.return_value = (group, False)

    app, reply, message, match = fake.create_all()

    Create(app).run(reply, message, match)

    create_group.assert_called_once_with('AuthorName', 'GroupName')
    reply.append.assert_called_once_with('Group `GroupName` already exists.  Skipping.')


@patch('tagtrain.data.by_owner.create_group')
def test_good(create_group):
    group = fake.create_group(name='GroupName', member_count=1)
    create_group.return_value = (group, True)

    app, reply, message, match = fake.create_all()

    Create(app).run(reply, message, match)

    create_group.assert_called_once_with('AuthorName', 'GroupName')
    reply.append.assert_called_once_with('Group `GroupName` created, no Members.')
