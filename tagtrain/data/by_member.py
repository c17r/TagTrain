from . import Group, Member, _update_member_count


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
