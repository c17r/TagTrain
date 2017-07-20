from unittest.mock import MagicMock, patch, call
from tagtrain import data
from . import fake

from tagtrain.tagtrain.tt_rename import Rename


@patch('tagtrain.data.by_owner.rename_group')
def test_unknown_group(rename_group):
    rename_group.side_effect = data.Group.DoesNotExist()

    app, reply, message, match = fake.create_all()

    Rename(app).run(reply, message, match)

    rename_group.assert_called_once_with('AuthorName', 'GroupName', 'NewName')
    reply.append.assert_called_once_with('Group `GroupName` does not exist, skipping.')



@patch('tagtrain.data.by_owner.rename_group')
def test_good(rename_group):
    rename_group.return_value = None

    app, reply, message, match = fake.create_all()

    Rename(app).run(reply, message, match)

    rename_group.assert_called_once_with('AuthorName', 'GroupName', 'NewName')
    reply.append.assert_called_once_with('Group `GroupName` renamed to `NewName`.')
