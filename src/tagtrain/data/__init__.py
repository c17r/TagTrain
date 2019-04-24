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


class DataException(Exception):
    pass


class BaseModel(peewee.Model):
    class Meta:
        database = database


class Group(BaseModel):
    name = peewee.CharField(max_length=255)
    reddit_name = peewee.CharField(max_length=30)
    added = peewee.DateTimeField(default=_now)
    member_count = peewee.IntegerField(default=0)
    locked = peewee.DateTimeField(null=True)

    class Meta:
        indexes = (
            (('name', 'reddit_name'), True),
        )


class Member(BaseModel):
    group = peewee.ForeignKeyField(Group, backref='members', index=True)
    reddit_name = peewee.CharField(max_length=30)
    added = peewee.DateTimeField(default=_now)
    perma_proof = peewee.CharField(max_length=512, null=True)


class Blacklist(BaseModel):
    owner_reddit_name = peewee.CharField(max_length=255)
    blocked_reddit_name = peewee.CharField(max_length=255)
    group = peewee.ForeignKeyField(Group, backref='+', null=True)
    added = peewee.DateTimeField(default=_now)
    perma_proof = peewee.CharField(max_length=512)


from . import by_owner  # noqa: F401, E402
from . import by_member  # noqa: F401, E402
