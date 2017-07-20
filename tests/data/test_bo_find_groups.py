import pytest
from . import db
from .db import database

from tagtrain import data


def test_unknown_owner(database):
    groups = list(data.by_owner.find_groups('non-existent'))

    assert len(groups) == 0


def test_good(database):
    groups = list(data.by_owner.find_groups(db.OWNER_NAME))

    assert len(groups) == 1
    assert groups[0].name == db.GROUP_NAME
    assert groups[0].reddit_name == db.OWNER_NAME
