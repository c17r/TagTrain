import pytest
from . import db
from .db import database

from tagtrain import data


def test_unknown_user(database):
    with pytest.raises(data.Group.DoesNotExist):
        data.by_owner.unblacklist_user('non-existent', 'doesnt-matter', db.GROUP_NAME)


def test_unknown_group(database):
    with pytest.raises(data.Group.DoesNotExist):
        data.by_owner.unblacklist_user(db.OWNER_NAME, 'doesnt-matter', 'non-existent')


def test_unknown_blanket_blacklist(database):
    with pytest.raises(data.Blacklist.DoesNotExist):
        data.by_owner.unblacklist_user(db.OWNER_NAME, 'non-existent')


def test_unknown_group_blacklist(database):
    with pytest.raises(data.Blacklist.DoesNotExist):
        data.by_owner.unblacklist_user(db.OWNER_NAME, 'non-existent', db.GROUP_NAME)


def test_good_blanket(database):
    OWNER_NAME = 'user2'
    MEMBER_NAME = 'blockee'

    bls = list(data.by_owner.find_blacklists(OWNER_NAME, MEMBER_NAME))
    assert len(bls) == 1

    bl = data.by_owner.unblacklist_user(OWNER_NAME, MEMBER_NAME)
    assert bl.owner_reddit_name == OWNER_NAME
    assert bl.blocked_reddit_name == MEMBER_NAME
    assert bl.group is None

    bls = list(data.by_owner.find_blacklists(OWNER_NAME, MEMBER_NAME))
    assert len(bls) == 0


def test_good_group(database):
    OWNER_NAME = db.OWNER_NAME
    GROUP_NAME = db.GROUP_NAME
    MEMBER_NAME = 'blockee'

    bls = list(data.by_owner.find_blacklists(OWNER_NAME, MEMBER_NAME))
    assert len(bls) == 2

    bl = data.by_owner.unblacklist_user(OWNER_NAME, MEMBER_NAME, GROUP_NAME)
    assert bl.owner_reddit_name == OWNER_NAME
    assert bl.blocked_reddit_name == MEMBER_NAME
    assert bl.group is not None
    assert bl.group.name == db.GROUP_NAME

    bls = list(data.by_owner.find_blacklists(OWNER_NAME, MEMBER_NAME))
    assert len(bls) == 1
