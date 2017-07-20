import pytest
from . import db
from .db import database

from tagtrain import data


def test_unknown_owner(database):
    with pytest.raises(data.Group.DoesNotExist):
        group = data.by_owner.rename_group('non-existent', db.GROUP_NAME, 'doesnt-matter')


def test_unknown_group(database):
    with pytest.raises(data.Group.DoesNotExist):
        group = data.by_owner.rename_group(db.OWNER_NAME, 'non-existent', 'doesnt-matter')


def test_good(database):
    NEW_NAME = 'new-name'

    group = data.by_owner.find_group(db.OWNER_NAME, db.GROUP_NAME)
    assert group.name == db.GROUP_NAME

    with pytest.raises(data.Group.DoesNotExist):
        group = data.by_owner.find_group(db.OWNER_NAME, NEW_NAME)

    data.by_owner.rename_group(db.OWNER_NAME, db.GROUP_NAME, 'new-name')

    group = data.by_owner.find_group(db.OWNER_NAME, NEW_NAME)
    assert group.name == NEW_NAME

    with pytest.raises(data.Group.DoesNotExist):
        group = data.by_owner.find_group(db.OWNER_NAME, db.GROUP_NAME)
