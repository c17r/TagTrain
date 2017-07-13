import pytest
from . import db
from .db import database

from tagtrain import data

def test_new_group(database):
    groups = list(data.find_groups(db.OWNER_NAME))

    assert len(groups) == 1

    group, created = data.add_user_to_group(db.OWNER_NAME, 'new-group', 'new-member')

    assert created is True
    assert group.name == 'new-group'
    assert group.reddit_name == db.OWNER_NAME
    assert group.member_count == 1
    assert len(list(group.members)) == 1
    assert group.members[0].reddit_name == 'new-member'

    groups = list(data.find_groups(db.OWNER_NAME))

    assert len(groups) == 2


def test_new_owner(database):
    groups = list(data.find_groups('new-guy'))

    assert len(groups) == 0

    group, created = data.add_user_to_group('new-guy', 'new-group', 'new-member')

    assert created is True
    assert group.name == 'new-group'
    assert group.reddit_name == 'new-guy'
    assert group.member_count == 1
    assert len(list(group.members)) == 1
    assert group.members[0].reddit_name == 'new-member'

    groups = list(data.find_groups('new-guy'))

    assert len(groups) == 1


def test_new_member(database):
    members = list(data.find_members_of_group(db.OWNER_NAME, db.GROUP_NAME))

    assert len(members) == 4

    group, created = data.add_user_to_group(db.OWNER_NAME, db.GROUP_NAME, 'new-member')

    assert created is True
    assert group.name == db.GROUP_NAME
    assert group.reddit_name == db.OWNER_NAME
    assert group.member_count == 5
    assert len(list(group.members)) == 5
    assert group.members[-1].reddit_name == 'new-member'

    members = list(data.find_members_of_group(db.OWNER_NAME, db.GROUP_NAME))

    assert len(members) == 5


def test_existing_member(database):
    members = list(data.find_members_of_group(db.OWNER_NAME, db.GROUP_NAME))

    assert len(members) == 4

    group, created = data.add_user_to_group(db.OWNER_NAME, db.GROUP_NAME, 'one')

    assert created is False
    assert group.name == db.GROUP_NAME
    assert group.reddit_name == db.OWNER_NAME
    assert group.member_count == 4
    assert len(list(group.members)) == 4

    members = list(data.find_members_of_group(db.OWNER_NAME, db.GROUP_NAME))

    assert len(members) == 4

