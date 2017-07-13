import pytest
from . import db
from .db import database

from tagtrain import data


def test_unknown_owner(database):
    with pytest.raises(data.Group.DoesNotExist):
        group = data.find_group('non-existent', db.GROUP_NAME)


def test_unknown_group(database):
    with pytest.raises(data.Group.DoesNotExist):
        group = data.find_group(db.OWNER_NAME, 'non-existent')


def test_good(database):
    group = data.find_group(db.OWNER_NAME, db.GROUP_NAME)

    assert group.name == db.GROUP_NAME
    assert group.reddit_name == db.OWNER_NAME
    assert group.member_count == 4
    assert len(group.members) == 4
