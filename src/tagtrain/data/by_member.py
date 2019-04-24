from . import DataException, Group, Member, _update_member_count
from tagtrain.data import by_owner


def remove_from_all_groups(reddit_name):
    groups = list(find_groups(reddit_name))

    (Member
     .delete()
     .where(Member.reddit_name ** reddit_name)
     .execute())

    for group in groups:
        _update_member_count(group)

    return groups


def find_groups(reddit_name):
    return (Group
            .select()
            .join(Member)
            .where(Member.reddit_name ** reddit_name)
            .order_by(Group.name)
            .iterator())


class Blacklisted(DataException):
    pass


def add_user_to_group(owner_name, group_name, reddit_name, permalink):
    group = by_owner.find_group(owner_name, group_name)

    bls = by_owner.find_blacklists(owner_name, reddit_name)
    for b in bls:
        if b.group is None or b.group == group:
            raise Blacklisted()

    member, created = Member.get_or_create(
        group=group,
        reddit_name=reddit_name,
        defaults={
            'perma_proof': permalink,
        }
    )

    _update_member_count(group)
    return group, created
