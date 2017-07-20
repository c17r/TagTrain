import pytest
from . import db
from .db import database

from tagtrain import data


def test_zero_groups(database):
    groups = data.by_member.remove_from_all_groups('non-existent')

    assert len(groups) == 0


def test_one_group(database):
    before = list(data.by_member.find_groups('one'))
    bc = [b.member_count for b in before]

    assert len(before) == 1

    rv = data.by_member.remove_from_all_groups('one')

    assert len(rv) == 1
    for b, n in zip(bc, rv):
        assert (b - 1) == n.member_count

    after = list(data.by_member.find_groups('one'))

    assert len(after) == 0


def test_two_groups(database):
    before = list(data.by_member.find_groups('three'))
    bc = [b.member_count for b in before]

    assert len(before) == 2

    rv = data.by_member.remove_from_all_groups('three')

    assert len(rv) == 2
    for b, n in zip(bc, rv):
        assert (b - 1) == n.member_count

    after = list(data.by_member.find_groups('three'))

    assert len(after) == 0
