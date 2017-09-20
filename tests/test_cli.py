#
#    Copyright 2017 Vitalii Kulanov
#

import shlex

import pytest

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
