from . import Group, Member, Blacklist, _update_member_count, _now, DataException


def find_group(owner_name, group_name):
    return (Group
            .select()
            .where(Group.name == group_name.lower(), Group.reddit_name ** owner_name)
            .get())


def find_groups(owner_name):
    return (Group
            .select()
            .where(Group.reddit_name ** owner_name)
            .order_by(Group.name)
            .iterator())


def find_blacklists(owner_name, member_name):
    return (Blacklist
            .select()
            .where(Blacklist.owner_reddit_name ** owner_name, Blacklist.blocked_reddit_name ** member_name)
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


class InvalidRequest(DataException):
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


class BlanketBlackList(DataException):
    pass


def blacklist_user(owner_name, reddit_name, permalink, group_name=None):
    group = find_group(owner_name, group_name) if group_name else None
    blacklists = list(find_blacklists(owner_name, reddit_name))

    if any([b for b in blacklists if b.group is None]):
        raise BlanketBlackList()

    if group:
        for b in blacklists:
            if b.group == group:
                return b, False

    bl = Blacklist.create(
        owner_reddit_name=owner_name,
        blocked_reddit_name=reddit_name,
        group=group,
        perma_proof=permalink
    )

    for group in find_groups(owner_name):
        if group_name is None or group.name == group_name.lower():
            members = [m for m in group.members if m.reddit_name.lower() == reddit_name.lower()]
            if len(members) == 1:
                members[0].delete_instance()
                _update_member_count(group)

    return bl, True


def unblacklist_user(owner_name, reddit_name, group_name=None):
    group = find_group(owner_name, group_name) if group_name else None
    blacklists = list(find_blacklists(owner_name, reddit_name))

    blacklist = [b for b in blacklists if b.group == group]
    if len(blacklist) != 1:
        raise Blacklist.DoesNotExist()

    blacklist[0].delete_instance()

    return blacklist[0]
