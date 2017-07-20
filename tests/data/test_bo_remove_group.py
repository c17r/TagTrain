import pytest
from . import db
from .db import database

from tagtrain import data


def test_unknown_owner(database):
    with pytest.raises(data.Group.DoesNotExist):
        data.by_owner.remove_group('non-existent', db.GROUP_NAME)


def test_unknown_group(database):
    with pytest.raises(data.Group.DoesNotExist):
        data.by_owner.remove_group(db.OWNER_NAME, 'non-existent')


def test_good(database):
    group = data.by_owner.find_group(db.OWNER_NAME, db.GROUP_NAME)

    data.by_owner.remove_group(db.OWNER_NAME, db.GROUP_NAME)

    with pytest.raises(data.Group.DoesNotExist):
        group = data.by_owner.find_group(db.OWNER_NAME, db.GROUP_NAME)
