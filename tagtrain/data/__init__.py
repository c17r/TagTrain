import datetime
import logging
import peewee


_logger = logging.getLogger('data')
database = peewee.SqliteDatabase(None)


def _now():
    return datetime.datetime.utcnow()


def _update_member_count(group):
    group.member_count = group.members.count()
    group.save()


def init(db_path):
    if not database.is_closed():
        database.close()
    database.init(db_path)
    database.create_tables([Group, Member], safe=True)


def find_group(owner_name, group_name):
    return (Group
            .select()
            .where(Group.name == group_name, Group.reddit_name == owner_name)
            .get())


def remove_group(owner_name, group_name):
    group = find_group(owner_name, group_name)
    group.delete_instance(recursive=True)


def find_groups(owner_name):
    return (Group
            .select()
            .where(Group.reddit_name == owner_name)
            .order_by(Group.name)
            .iterator())


def find_members_of_group(owner_name, group_name):
    group = find_group(owner_name, group_name)
    return group.members


def add_user_to_group(owner_name, group_name, member_name):
    group, _ = Group.get_or_create(name=group_name, reddit_name=owner_name)
    member, created = Member.get_or_create(group=group, reddit_name=member_name)
    _update_member_count(group)
    return group, created


def remove_user_from_group(owner_name, group_name, member_name):
    group = find_group(owner_name, group_name)
    member = Member.get(Member.group == group, Member.reddit_name == member_name)

    member.delete_instance()
    _update_member_count(group)
    if group.member_count == 0:
        group.delete_instance()

    return group


class BaseModel(peewee.Model):
    class Meta:
        database = database


class Group(BaseModel):
    name = peewee.CharField(max_length=255)
    reddit_name = peewee.CharField(max_length=30)
    added = peewee.DateTimeField(default=_now)
    member_count = peewee.IntegerField(default=0)

    class Meta:
        indexes = (
            (('name', 'reddit_name'), True),
        )


class Member(BaseModel):
    group = peewee.ForeignKeyField(Group, related_name='members', index=True)
    reddit_name = peewee.CharField(max_length=30)
    added = peewee.DateTimeField(default=_now)
