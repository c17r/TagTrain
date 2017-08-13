from unittest.mock import MagicMock, patch
from tagtrain import data
from . import fake

from tagtrain.tagtrain.tt_unblacklist import UnBlacklist


@patch('tagtrain.data.by_owner.unblacklist_user')
def test_unknown_group(unblacklist_user):
    unblacklist_user.side_effect = data.Group.DoesNotExist()

    app, reply, message, match = fake.create_all()

    UnBlacklist(app).run(reply, message, match)

    unblacklist_user.assert_called_once_with('AuthorName', 'MemberName', 'GroupName')
    reply.append.assert_called_once_with('Group `GroupName` does not exist.  Skipping.')


@patch('tagtrain.data.by_owner.unblacklist_user')
def test_unknown_blanket_blacklist(unblacklist_user):
    unblacklist_user.side_effect = data.Blacklist.DoesNotExist()

    app, reply, message, _ = fake.create_all()
    match = fake.create_match({
        'group': None,
        'member': 'MemberName',
        'owner': 'OwnerName',
        'name': 'NewName',
    })

    UnBlacklist(app).run(reply, message, match)

    unblacklist_user.assert_called_once_with('AuthorName', 'MemberName', None)
    reply.append.assert_called_once_with('Blanket Blacklist for Member `MemberName` does not exist.  Skipping.')


@patch('tagtrain.data.by_owner.unblacklist_user')
def test_unknown_group_blacklist(unblacklist_user):
    unblacklist_user.side_effect = data.Blacklist.DoesNotExist()

    app, reply, message, match = fake.create_all()

    UnBlacklist(app).run(reply, message, match)

    unblacklist_user.assert_called_once_with('AuthorName', 'MemberName', 'GroupName')
    reply.append.assert_called_once_with('Group `GroupName` Blacklist for Member `MemberName` does not exist.  Skipping.')


@patch('tagtrain.data.by_owner.unblacklist_user')
def test_good_blanket(unblacklist_user):
    unblacklist_user.return_value = fake.create_blacklist(owner_reddit_name='AuthorName', blocked_reddit_name='MemberName')

    app, reply, message, _ = fake.create_all()
    match = fake.create_match({
        'group': None,
        'member': 'MemberName',
        'owner': 'OwnerName',
        'name': 'NewName',
    })

    UnBlacklist(app).run(reply, message, match)

    unblacklist_user.assert_called_once_with('AuthorName', 'MemberName', None)
    reply.append.assert_called_once_with('Blanket Blacklist for Member `MemberName` removed.')

@patch('tagtrain.data.by_owner.unblacklist_user')
def test_good_group(unblacklist_user):
    unblacklist_user.return_value = fake.create_blacklist(owner_reddit_name='AuthorName', blocked_reddit_name='MemberName')

    app, reply, message, match = fake.create_all()

    UnBlacklist(app).run(reply, message, match)

    unblacklist_user.assert_called_once_with('AuthorName', 'MemberName', 'GroupName')
    reply.append.assert_called_once_with('Group `GroupName` Blacklist for Member `MemberName` removed.')