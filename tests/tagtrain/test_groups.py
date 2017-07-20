from unittest.mock import MagicMock, patch, call
from . import fake

from tagtrain.tagtrain.tt_groups import Groups

@patch('tagtrain.data.by_owner.find_groups')
def test_no_groups(find_groups):
    find_groups.return_value = []

    app, reply, message, match = fake.create_all()

    Groups(app).run(reply, message, match)

    find_groups.assert_called_once_with('AuthorName')
    reply.append.assert_called_once_with('You have no Groups.')


@patch('tagtrain.data.by_owner.find_groups')
def test_good(find_groups):
    find_groups.return_value = iter([
        fake.create_group(name='Group1', member_count=1),
        fake.create_group(name='Group2', member_count=2),
        fake.create_group(name='Group3', member_count=4),
        fake.create_group(name='Group4', member_count=6),
    ])

    app, reply, message, match = fake.create_all()

    Groups(app).run(reply, message, match)

    find_groups.assert_called_once_with('AuthorName')
    reply.append.assert_has_calls([
        call('Groups | Member Counts'),
        call('------ | -------------'),
        call('`Group1` | 1'),
        call('`Group2` | 2'),
        call('`Group3` | 4'),
        call('`Group4` | 6'),
    ])
