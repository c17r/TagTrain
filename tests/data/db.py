from datetime import datetime
import pytest

from tagtrain import data

OWNER_NAME = 'user1'
GROUP_NAME = 'group1'


@pytest.fixture()
def database():
    data.init(':memory:')
    data.database.create_tables([data.Group, data.Member, data.Blacklist])

    group = data.Group.create(name=GROUP_NAME, reddit_name=OWNER_NAME, member_count=4, locked=None)
    data.Member.create(group=group, reddit_name='one')
    data.Member.create(group=group, reddit_name='two')
    data.Member.create(group=group, reddit_name='three')
    data.Member.create(group=group, reddit_name='four')

    group2 = data.Group.create(name='group2', reddit_name=OWNER_NAME, member_count=3, locked=None)
    data.Member.create(group=group2, reddit_name='eh')
    data.Member.create(group=group2, reddit_name='be')
    data.Member.create(group=group2, reddit_name='see')
    data.Member.create(group=group2, reddit_name='four')

    group3 = data.Group.create(name='group3', reddit_name=OWNER_NAME, member_count=2, locked=None)
    data.Member.create(group=group3, reddit_name='ecks')
    data.Member.create(group=group3, reddit_name='why')
    data.Member.create(group=group3, reddit_name='four')

    data.Blacklist.create(
        owner_reddit_name=OWNER_NAME,
        blocked_reddit_name='blockee',
        group=group,
        perma_proof='p/permalink'
    )

    data.Blacklist.create(
        owner_reddit_name=OWNER_NAME,
        blocked_reddit_name='blockee',
        group=group2,
        perma_proof='p/permalink'
    )

    data.Blacklist.create(
        owner_reddit_name=OWNER_NAME,
        blocked_reddit_name='blockee12',
        group=group,
        perma_proof='p/permalink12'
    )

    group = data.Group.create(name='group2', reddit_name='user2', member_count=4, locked=datetime.utcnow())
    data.Member.create(group=group, reddit_name='three')
    data.Member.create(group=group, reddit_name='four')
    data.Member.create(group=group, reddit_name='five')
    data.Member.create(group=group, reddit_name='six')

    data.Blacklist.create(
        owner_reddit_name='user2',
        blocked_reddit_name='blockee',
        perma_proof='p/permalink2'
    )

    data.Blacklist.create(
        owner_reddit_name='user2',
        blocked_reddit_name='blockee22',
        perma_proof='p/permalink22'
    )
