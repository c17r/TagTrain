from unittest.mock import MagicMock, PropertyMock, patch, call
from . import fake

from tagtrain.tagtrain.tt_help import Help
from tagtrain.tagtrain import TagTrainResponse


def make_cmd(**kwargs):
    rv = MagicMock(**kwargs)
    help_prop = PropertyMock(return_value=kwargs['HELP_TEXT'])
    type(rv).help = help_prop
    return rv


def test_good_all():

    app, reply, message, match = fake.create_all()

    app.configure_mock(cmds=[
        make_cmd(TYPE=TagTrainResponse.TYPE_COMMENTORMESSAGE, HELP_TEXT='CM1'),
        make_cmd(TYPE=TagTrainResponse.TYPE_COMMENTORMESSAGE, HELP_TEXT='CM2'),

        make_cmd(TYPE=TagTrainResponse.TYPE_MESSAGE, HELP_TEXT='M1'),
        make_cmd(TYPE=TagTrainResponse.TYPE_MESSAGE, HELP_TEXT='M2'),

        make_cmd(TYPE=TagTrainResponse.TYPE_COMMENT, HELP_TEXT='C1'),
        make_cmd(TYPE=TagTrainResponse.TYPE_COMMENT, HELP_TEXT='C2'),
    ])

    help = Help(app)
    help.run(reply, message, match)

    reply.append.assert_has_calls([
        call(help.MAIN_TEXT),
        call('\n'),
        call('\n'),
        call('In a Comment or Message:'),
        call('\n'),
        call('- CM1'),
        call('- CM2'),
        call('\n'),
        call('In a Message:'),
        call('\n'),
        call('- M1'),
        call('- M2'),
        call('\n'),
        call('In a Comment:'),
        call('\n'),
        call('- C1'),
        call('- C2'),
    ])


def test_good_some():

    app, reply, message, match = fake.create_all()

    app.configure_mock(cmds=[
        make_cmd(TYPE=TagTrainResponse.TYPE_COMMENTORMESSAGE, HELP_TEXT='CM1'),
        make_cmd(TYPE=TagTrainResponse.TYPE_COMMENTORMESSAGE, HELP_TEXT='CM2'),

        make_cmd(TYPE=TagTrainResponse.TYPE_COMMENT, HELP_TEXT='C1'),
        make_cmd(TYPE=TagTrainResponse.TYPE_COMMENT, HELP_TEXT='C2'),
    ])

    help = Help(app)
    help.run(reply, message, match)

    reply.append.assert_has_calls([
        call(help.MAIN_TEXT),
        call('\n'),
        call('\n'),
        call('In a Comment or Message:'),
        call('\n'),
        call('- CM1'),
        call('- CM2'),
        call('\n'),
        call('In a Comment:'),
        call('\n'),
        call('- C1'),
        call('- C2'),
    ])

def test_good_cache():

    app, reply, message, match = fake.create_all()

    app.configure_mock(cmds=[
        make_cmd(TYPE=TagTrainResponse.TYPE_COMMENTORMESSAGE, HELP_TEXT='CM1'),
        make_cmd(TYPE=TagTrainResponse.TYPE_COMMENTORMESSAGE, HELP_TEXT='CM2'),

        make_cmd(TYPE=TagTrainResponse.TYPE_COMMENT, HELP_TEXT='C1'),
        make_cmd(TYPE=TagTrainResponse.TYPE_COMMENT, HELP_TEXT='C2'),
    ])

    help = Help(app)
    help.run(reply, message, match)

    reply.reset_mock()

    help.run(reply, message, match)

    reply.append.assert_has_calls([
        call(help.MAIN_TEXT),
        call('\n'),
        call('\n'),
        call('In a Comment or Message:'),
        call('\n'),
        call('- CM1'),
        call('- CM2'),
        call('\n'),
        call('In a Comment:'),
        call('\n'),
        call('- C1'),
        call('- C2'),
    ])
