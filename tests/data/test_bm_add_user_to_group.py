import pytest
from . import db
from .db import database

from tagtrain import data


def test_unknow_group(database):

    with pytest.raises(data.Group.DoesNotExist):
        group, created = data.by_member.add_user_to_group(db.OWNER_NAME, 'new-group', 'new-member', 'permalink')


def test_new_member(database):
    members = list(data.by_owner.find_members_of_group(db.OWNER_NAME, db.GROUP_NAME))

    assert len(members) == 4

    group, created = data.by_member.add_user_to_group(db.OWNER_NAME, db.GROUP_NAME, 'new-member', 'permalink')

    assert created is True
    assert group.name == db.GROUP_NAME
    assert group.reddit_name == db.OWNER_NAME
    assert group.member_count == 5
    assert len(list(group.members)) == 5
    assert group.members[-1].reddit_name == 'new-member'

    members = list(data.by_owner.find_members_of_group(db.OWNER_NAME, db.GROUP_NAME))

    assert len(members) == 5


def test_existing_member(database):
    members = list(data.by_owner.find_members_of_group(db.OWNER_NAME, db.GROUP_NAME))

    assert len(members) == 4

    group, created = data.by_member.add_user_to_group(db.OWNER_NAME, db.GROUP_NAME, 'one', 'permalink')

    assert created is False
    assert group.name == db.GROUP_NAME
    assert group.reddit_name == db.OWNER_NAME
    assert group.member_count == 4
    assert len(list(group.members)) == 4

    members = list(data.by_owner.find_members_of_group(db.OWNER_NAME, db.GROUP_NAME))

    assert len(members) == 4

