import pytest
from . import db
from .db import database

from tagtrain import data


def test_unknown_owner(database):
    bls = list(data.by_owner.find_blacklists(db.OWNER_NAME, 'non-existent'))

    assert len(bls) == 0


def test_unknown_member(database):
    bls = list(data.by_owner.find_blacklists('non-existent', 'blockee'))

    assert len(bls) == 0

def test_good(database):
    bls = list(data.by_owner.find_blacklists(db.OWNER_NAME, 'blockee'))

    assert len(bls) == 2