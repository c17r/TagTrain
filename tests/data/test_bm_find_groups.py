import pytest
from . import db
from .db import database

from tagtrain import data


def test_zero_groups(database):
    groups = list(data.by_member.find_groups('non-existent'))

    assert len(groups) == 0


def test_one_group(database):
    groups = list(data.by_member.find_groups('one'))

    assert len(groups) == 1
    assert groups[0].name == db.GROUP_NAME
    assert groups[0].reddit_name == db.OWNER_NAME


def test_two_groups(database):
    groups = list(data.by_member.find_groups('three'))

    assert len(groups) == 2
    assert groups[0].name == db.GROUP_NAME
    assert groups[0].reddit_name == db.OWNER_NAME
