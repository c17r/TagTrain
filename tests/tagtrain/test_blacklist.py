from unittest.mock import MagicMock, patch
from tagtrain import data
from . import fake

from tagtrain.tagtrain.tt_blacklist import Blacklist


@patch('tagtrain.data.by_owner.blacklist_user')
def test_unknown_group(blacklist_user):
    blacklist_user.side_effect = data.Group.DoesNotExist()

    app, reply, message, match = fake.create_all()

    Blacklist(app).run(reply, message, match)

    blacklist_user.assert_called_once_with('AuthorName', 'MemberName', 'PermaLink', 'GroupName')
    reply.append.assert_called_once_with('Group `GroupName` does not exist.  Skipping.')


@patch('tagtrain.data.by_owner.blacklist_user')
def test_existing_blanket(blacklist_user):
    blacklist_user.side_effect = data.by_owner.BlanketBlackList()

    app, reply, message, match = fake.create_all()

    Blacklist(app).run(reply, message, match)

    blacklist_user.assert_called_once_with('AuthorName', 'MemberName', 'PermaLink', 'GroupName')
    reply.append.assert_called_once_with('Blanket Blacklist for `MemberName` exists.  Skipping.')


@patch('tagtrain.data.by_owner.blacklist_user')
def test_existing(blacklist_user):
    bl = fake.create_blacklist(owner_reddit_name='AuthorName', blocked_reddit_name='MemberName')
    blacklist_user.return_value = (bl, False)

    app, reply, message, match = fake.create_all()

    Blacklist(app).run(reply, message, match)

    blacklist_user.assert_called_once_with('AuthorName', 'MemberName', 'PermaLink', 'GroupName')
    reply.append.assert_called_once_with('Group `GroupName` Blacklist for `MemberName` exists.  Skipping.')


@patch('tagtrain.data.by_owner.blacklist_user')
def test_good_blanket(blacklist_user):
    bl = fake.create_blacklist(owner_reddit_name='AuthorName', blocked_reddit_name='MemberName')
    blacklist_user.return_value = (bl, True)

    app, reply, message, _ = fake.create_all()
    match = fake.create_match({
        'group': None,
        'member': 'MemberName',
        'owner': 'OwnerName',
        'name': 'NewName',
    })

    Blacklist(app).run(reply, message, match)

    blacklist_user.assert_called_once_with('AuthorName', 'MemberName', 'PermaLink', None)
    reply.append.assert_called_once_with('Blanket Blacklist for `MemberName` created.')


@patch('tagtrain.data.by_owner.blacklist_user')
def test_good_group(blacklist_user):
    bl = fake.create_blacklist(owner_reddit_name='AuthorName', blocked_reddit_name='MemberName')
    blacklist_user.return_value = (bl, True)

    app, reply, message, match = fake.create_all()

    Blacklist(app).run(reply, message, match)

    blacklist_user.assert_called_once_with('AuthorName', 'MemberName', 'PermaLink', 'GroupName')
    reply.append.assert_called_once_with('Group `GroupName` Blacklist for `MemberName` created.')
