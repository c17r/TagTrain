from unittest.mock import MagicMock, patch, call
from tagtrain import data
from . import fake

from tagtrain.tagtrain.tt_clear import Clear


@patch('tagtrain.data.by_owner.remove_group')
def test_unknown_group(remove_group):
    remove_group.side_effect = data.Group.DoesNotExist()

    app, reply, message, match = fake.create_all()

    Clear(app).run(reply, message, match)

    remove_group.assert_called_once_with('AuthorName', 'GroupName')
    reply.append.assert_called_once_with('Group `GroupName` does not exist.  Skipping.')


@patch('tagtrain.data.by_owner.remove_group')
def test_good(remove_group):
    remove_group.return_value = None

    app, reply, message, match = fake.create_all()

    Clear(app).run(reply, message, match)

    remove_group.assert_called_once_with('AuthorName', 'GroupName')
    reply.append.assert_called_once_with('Group `GroupName` and all Members removed.')
