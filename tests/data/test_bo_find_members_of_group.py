import pytest
from . import db
from .db import database

from tagtrain import data


def test_unknown_owner(database):
    with pytest.raises(data.Group.DoesNotExist):
        members = data.by_owner.find_members_of_group('non-existent', db.GROUP_NAME)


def test_unknown_group(database):
    with pytest.raises(data.Group.DoesNotExist):
        members = data.by_owner.find_members_of_group(db.OWNER_NAME, 'non-existent')


def test_good(database):
    members = list(data.by_owner.find_members_of_group(db.OWNER_NAME, db.GROUP_NAME))

    assert len(members) == 4
