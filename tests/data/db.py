import pytest

from tagtrain import data

OWNER_NAME = 'user1'
GROUP_NAME = 'group1'


@pytest.fixture()
def database():
    data.init(':memory:')
    group = data.Group.create(name=GROUP_NAME, reddit_name=OWNER_NAME, member_count=4)
    data.Member.create(group=group, reddit_name='one')
    data.Member.create(group=group, reddit_name='two')
    data.Member.create(group=group, reddit_name='three')
    data.Member.create(group=group, reddit_name='four')
