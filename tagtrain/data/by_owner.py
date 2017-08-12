from . import Group, Member, _update_member_count, _now


def find_group(owner_name, group_name):
    return (Group
            .select()
            .where(Group.name ** group_name, Group.reddit_name ** owner_name)
            .get())


def find_groups(owner_name):
    return (Group
            .select()
            .where(Group.reddit_name ** owner_name)
            .order_by(Group.name)
            .iterator())


def find_members_of_group(owner_name, group_name):
    group = find_group(owner_name, group_name)
    return group.members


def create_group(owner_name, group_name):
    group, created = Group.get_or_create(name=group_name.lower(), reddit_name=owner_name)
    return group, created


def remove_group(owner_name, group_name):
    group = find_group(owner_name, group_name)
    group.delete_instance(recursive=True)


def remove_user_from_group(owner_name, group_name, reddit_name):
    group = find_group(owner_name, group_name)
    member = Member.get(Member.group == group, Member.reddit_name ** reddit_name)

    member.delete_instance()
    _update_member_count(group)
    return group


def rename_group(owner_name, group_name, new_name):
    group = find_group(owner_name, group_name)
    group.name = new_name
    _update_member_count(group)


class InvalidRequest(Exception):
    pass


def lock_group(owner_name, group_name):
    return _lock_unlock(owner_name, group_name, True)


def unlock_group(owner_name, group_name):
    return _lock_unlock(owner_name, group_name, False)


def _lock_unlock(owner_name, group_name, lock):
    group = find_group(owner_name, group_name)

    if (lock and group.locked) or (not lock and not group.locked):
        raise InvalidRequest

    group.locked = _now() if lock else None
    group.save()
    return group
