import pytest
from . import db
from .db import database

from tagtrain import data


def test_existing_group(database):
    groups = list(data.by_owner.find_groups(db.OWNER_NAME))
    assert len(groups) == 1

    group, created = data.by_owner.create_group(db.OWNER_NAME, db.GROUP_NAME)
    assert created is False

    groups = list(data.by_owner.find_groups(db.OWNER_NAME))
    assert len(groups) == 1


def test_good(database):
    groups = list(data.by_owner.find_groups(db.OWNER_NAME))
    assert len(groups) == 1

    group, created = data.by_owner.create_group(db.OWNER_NAME, 'new-group')
    assert created is True

    groups = list(data.by_owner.find_groups(db.OWNER_NAME))
    assert len(groups) == 2
