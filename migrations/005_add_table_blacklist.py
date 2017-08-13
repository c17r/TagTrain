"""Peewee migrations -- 005_add_table_blacklist.py.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['model_name']            # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.python(func, *args, **kwargs)        # Run python code
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.drop_index(model, *col_names)
    > migrator.add_not_null(model, *field_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)

"""

import datetime as dt
import peewee


def migrate(migrator, database, fake=False, **kwargs):
    """Write your migrations here."""
    Group = migrator.orm['group']

    def _now():
        pass

    @migrator.create_model
    class Blacklist(peewee.Model):
        owner_reddit_name = peewee.CharField(max_length=255)
        blocked_reddit_name = peewee.CharField(max_length=255)
        group = peewee.ForeignKeyField(Group, related_name='+', null=True)
        added = peewee.DateTimeField(default=_now)
        perma_proof = peewee.CharField(max_length=512)


def rollback(migrator, database, fake=False, **kwargs):
    """Write your rollback migrations here."""

