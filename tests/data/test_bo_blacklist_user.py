import pytest
from . import db
from .db import database

from tagtrain import data


def test_unknown_user(database):
    with pytest.raises(data.Group.DoesNotExist):
        data.by_owner.blacklist_user('non-existent', 'blockee', 'permalink', db.GROUP_NAME)


def test_unknown_group(database):
    with pytest.raises(data.Group.DoesNotExist):
        data.by_owner.blacklist_user(db.OWNER_NAME, 'blockee', 'permalink', 'non-existent')


def test_existing_blanket(database):
    with pytest.raises(data.by_owner.BlanketBlackList):
        data.by_owner.blacklist_user('user2', 'blockee', 'permalink', 'group2')


def test_existing_blacklist(database):
    PERMALINK = '123'
    blacklist, created = data.by_owner.blacklist_user(db.OWNER_NAME, 'blockee', PERMALINK, db.GROUP_NAME)

    assert created is False
    assert blacklist.perma_proof != PERMALINK


def test_good_blanket(database):
    OWNER_NAME = db.OWNER_NAME
    MEMBER_NAME = 'four'
    PERMALINK = 'my123'

    bls = list(data.by_owner.find_blacklists(OWNER_NAME, MEMBER_NAME))
    assert len(bls) == 0

    groups = list(data.by_member.find_groups(MEMBER_NAME))
    assert len(groups) == 4


    bl, created = data.by_owner.blacklist_user(OWNER_NAME, MEMBER_NAME, PERMALINK)
    assert created is True
    assert bl.owner_reddit_name == OWNER_NAME
    assert bl.blocked_reddit_name == MEMBER_NAME
    assert bl.group is None
    assert bl.perma_proof == PERMALINK

    bls = list(data.by_owner.find_blacklists(OWNER_NAME, MEMBER_NAME))
    assert len(bls) == 1

    groups = list(data.by_member.find_groups(MEMBER_NAME))
    assert len(groups) == 1


def test_good_group1(database):
    OWNER_NAME = db.OWNER_NAME
    MEMBER_NAME = 'blockee'
    GROUP_NAME = 'group3'
    PERMALINK = 'my123'

    bls = list(data.by_owner.find_blacklists(OWNER_NAME, MEMBER_NAME))
    assert len(bls) == 2

    bl, created = data.by_owner.blacklist_user(OWNER_NAME, MEMBER_NAME, PERMALINK, GROUP_NAME)
    assert created is True
    assert bl.owner_reddit_name == OWNER_NAME
    assert bl.blocked_reddit_name == MEMBER_NAME
    assert bl.group is not None
    assert bl.group.name == GROUP_NAME
    assert bl.perma_proof == PERMALINK

    bls = list(data.by_owner.find_blacklists(OWNER_NAME, MEMBER_NAME))
    assert len(bls) == 3


def test_good_group_delete(database):
    OWNER_NAME = db.OWNER_NAME
    MEMBER_NAME = 'four'
    GROUP_NAME = 'group3'
    PERMALINK = 'my123'

    bls = list(data.by_owner.find_blacklists(OWNER_NAME, MEMBER_NAME))
    assert len(bls) == 0

    groups = list(data.by_member.find_groups(MEMBER_NAME))
    assert len(groups) == 4

    bl, created = data.by_owner.blacklist_user(OWNER_NAME, MEMBER_NAME, PERMALINK, GROUP_NAME)
    assert created is True
    assert bl.owner_reddit_name == OWNER_NAME
    assert bl.blocked_reddit_name == MEMBER_NAME
    assert bl.group is not None
    assert bl.group.name == GROUP_NAME
    assert bl.perma_proof == PERMALINK

    bls = list(data.by_owner.find_blacklists(OWNER_NAME, MEMBER_NAME))
    assert len(bls) == 1

    groups = list(data.by_member.find_groups(MEMBER_NAME))
    assert len(groups) == 3
