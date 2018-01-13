#
#    Copyright 2017 Vitalii Kulanov
#

import logging
import shlex

import pytest
import yaml

from validocx import cli


def exec_command(command=''):
    """Executes validocx with the specified arguments."""

    argv = shlex.split(command)
    args = cli.parse_args(argv)
    cli.run(arguments=args)


def test_cli_with_empty_args_fail(capsys):
    with pytest.raises(SystemExit):
        exec_command()
    out, err = capsys.readouterr()
    assert ("error: the following arguments are required: "
            "docx-file, -r/--requirements" in err)


@pytest.mark.parametrize('cmd, required_argument', [
    ('--requirements /tmp/fake_requirements.yaml', 'docx-file'),
    ('/tmp/fake.docx', '-r/--requirements')
])
def test_cli_wo_file_argument_fail(cmd, required_argument, mocker, capsys):
    mocker.patch('validocx.cli.os.path.lexists', return_value=True)
    with pytest.raises(SystemExit):
        exec_command(cmd)
    out, err = capsys.readouterr()
    assert ("error: the following arguments are required:"
            " {0}".format(required_argument) in err)


@pytest.mark.parametrize('side_effect, file_name', [
    ([True, False], 'requirements.yaml'),
    ([False, True], 'fake.docx')
])
def test_cli_file_missing_fail(side_effect, file_name, mocker, capsys):
    cmd = 'fake.docx --requirements requirements.yaml'
    mocker.patch('validocx.cli.os.path.lexists', side_effect=side_effect)
    with pytest.raises(SystemExit):
        exec_command(cmd)
    out, err = capsys.readouterr()
    assert "File '{0}' does not exist".format(file_name) in err


def test_cli_verbosity_level_w_mutually_exclusive_params_fail(mocker, capsys):
    cmd = 'fake.docx --requirements requirements.yaml -q -v'
    mocker.patch('validocx.cli.os.path.lexists', return_value=True)
    with pytest.raises(SystemExit):
        exec_command(cmd)
    out, err = capsys.readouterr()
    assert ("error: argument -v/--verbose: "
            "not allowed with argument -q/--quiet" in err)


@pytest.fixture
def message_counter_handler(mocker):
    m_msg_lvl_cnt = mocker.patch.object(cli.MessageCounterHandler,
                                        'msg_level_count',
                                        new_callable=mocker.PropertyMock)
    yield m_msg_lvl_cnt
    root_logger = logging.getLogger()
    root_logger.handlers = [h for h in root_logger.handlers if
                            not isinstance(h, cli.MessageCounterHandler)]


def test_cli_validate(message_counter_handler, mocker, caplog):
    message_counter_handler.return_value = {'ERROR': 5, 'WARNING': 10}
    mocker.patch('validocx.cli.os.path.lexists', return_value=True)
    docx_file = '/tmp/fake.docx'
    requirements = {'fake': {'foo': ['bar']}}
    req_file = '/tmp/requirements.yaml'
    cmd = '{0} --requirements {1}'.format(docx_file, req_file)
    m_open = mocker.mock_open(read_data=yaml.dump(requirements))
    mocker.patch('validocx.utils.open', m_open, create=True)
    m_validate = mocker.patch('validocx.cli.validate')
    exec_command(cmd)
    m_open.assert_called_once_with(req_file, 'r')
    m_validate.assert_called_once_with(docx_file, requirements)
    assert caplog.record_tuples == [
        ('root', 20, 'Summary results: Errors - 5, Warnings - 10')]


def test_cli_validate_w_log_file(message_counter_handler, tmpdir, mocker):
    message_counter_handler.return_value = {'ERROR': 5, 'WARNING': 10}
    mocker.patch('validocx.cli.os.path.lexists', return_value=True)
    log_file = tmpdir.join('fake.log')
    docx_file = '/tmp/fake.docx'
    requirements = {'fake': {'foo': ['bar']}}
    req_file = '/tmp/requirements.yaml'
    cmd = '{0} --requirements {1} --log-file {2}'.format(
        docx_file, req_file, log_file)
    m_open = mocker.mock_open(read_data=yaml.dump(requirements))
    mocker.patch('validocx.utils.open', m_open, create=True)
    m_validate = mocker.patch('validocx.cli.validate')
    exec_command(cmd)
    m_open.assert_called_once_with(req_file, 'r')
    m_validate.assert_called_once_with(docx_file, requirements)
    assert "Summary results: Errors - 5, Warnings - 10" in log_file.read()
