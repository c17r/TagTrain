import pytest
from . import db
from .db import database

from tagtrain import data


def test_unknown_owner(database):
    with pytest.raises(data.Group.DoesNotExist):
        data.by_owner.lock_group('non-existent', db.GROUP_NAME)


def test_unknown_group(database):
    with pytest.raises(data.Group.DoesNotExist):
        data.by_owner.lock_group(db.OWNER_NAME, 'non-existent')


def test_already_locked(database):
    with pytest.raises(data.by_owner.InvalidRequest):
        data.by_owner.lock_group('user2', 'group2')


def test_good(database):
    group = data.by_owner.find_group(db.OWNER_NAME, db.GROUP_NAME)

    assert group.locked is None

    data.by_owner.lock_group(db.OWNER_NAME, db.GROUP_NAME)

    group = data.by_owner.find_group(db.OWNER_NAME, db.GROUP_NAME)

    assert group.locked is not None
