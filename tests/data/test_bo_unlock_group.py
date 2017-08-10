import pytest
from . import db
from .db import database

from tagtrain import data


def test_unknown_owner(database):
    with pytest.raises(data.Group.DoesNotExist):
        data.by_owner.unlock_group('non-existent', db.GROUP_NAME)


def test_unknown_group(database):
    with pytest.raises(data.Group.DoesNotExist):
        data.by_owner.unlock_group(db.OWNER_NAME, 'non-existent')


def test_already_unlocked(database):
    with pytest.raises(data.by_owner.InvalidRequest):
        data.by_owner.unlock_group(db.OWNER_NAME, db.GROUP_NAME)


def test_good(database):
    OWNER_NAME = 'user2'
    GROUP_NAME = 'group2'

    group = data.by_owner.find_group(OWNER_NAME, GROUP_NAME)

    assert group.locked is not None

    data.by_owner.unlock_group(OWNER_NAME, GROUP_NAME)

    group = data.by_owner.find_group(OWNER_NAME, GROUP_NAME)

    assert group.locked is None
