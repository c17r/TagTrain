import pytest
from . import db
from .db import database

from tagtrain import data


def test_unknown_owner(database):
    with pytest.raises(data.Group.DoesNotExist):
        group = data.remove_user_from_group('non-existent', db.GROUP_NAME, 'doesnt-matter')


def test_unknown_group(database):
    with pytest.raises(data.Group.DoesNotExist):
        group = data.remove_user_from_group(db.OWNER_NAME, 'non-existent', 'doesnt-matter')


def test_unknown_member(database):
    with pytest.raises(data.Member.DoesNotExist):
        group = data.remove_user_from_group(db.OWNER_NAME, db.GROUP_NAME, 'non-existent')


def test_good_non_empty(database):
    group = data.find_group(db.OWNER_NAME, db.GROUP_NAME)

    assert group.member_count == 4
    assert len(list(group.members)) == 4

    group = data.remove_user_from_group(db.OWNER_NAME, db.GROUP_NAME, 'one')

    assert group.name == db.GROUP_NAME
    assert group.reddit_name == db.OWNER_NAME
    assert group.member_count == 3
    assert len(list(group.members)) == 3
    assert group.members[0].reddit_name == 'two'

    group = data.find_group(db.OWNER_NAME, db.GROUP_NAME)

    assert group.member_count == 3
    assert len(list(group.members)) == 3


def test_good_empty(database):
    group = data.find_group(db.OWNER_NAME, db.GROUP_NAME)

    assert group.member_count == 4
    assert len(list(group.members)) == 4

    members_to_delete = [m.reddit_name for m in group.members]

    for m in members_to_delete:
        group = data.remove_user_from_group(db.OWNER_NAME, db.GROUP_NAME, m)

    assert group.name == db.GROUP_NAME
    assert group.reddit_name == db.OWNER_NAME
    assert group.member_count == 0
    assert len(list(group.members)) == 0

    with pytest.raises(data.Group.DoesNotExist):
        group = data.find_group(db.OWNER_NAME, db.GROUP_NAME)
