#
#    Copyright 2017 Vitalii Kulanov
#

import pytest

from validocx import utils


@pytest.mark.parametrize('data, file_name, expected', [
    ('---\nfake:\n  foo:\n  - bar\n', 'fake.yaml', {'fake': {'foo': ['bar']}}),
    ('{"fake":{"foo":["bar"]}}', 'fake.json', {'fake': {'foo': ['bar']}})
])
def test_read_from_file(data, file_name, expected, tmpdir):
    fake_file = tmpdir.join(file_name)
    fake_file.write(data)
    assert utils.read_from_file(fake_file.strpath) == expected


def test_read_from_file_bad_format_fail(tmpdir):
    fake_file = tmpdir.join("format_file.bad")
    fake_file.write('')
    with pytest.raises(ValueError) as excinfo:
        utils.read_from_file(fake_file.strpath)
    assert 'Unsupported data format.' in str(excinfo.value)


@pytest.mark.parametrize('data, file_name, expected', [
    ({'fake': {'foo': ['bar']}}, 'fake.yaml', 'fake:\n  foo:\n  - bar\n'),
    ({'fake': {'foo': ['bar']}}, 'fake.json', '{\n'
                                              '    "fake": {\n'
                                              '        "foo": [\n'
                                              '            "bar"\n'
                                              '        ]\n'
                                              '    }\n'
                                              '}')
])
def test_write_file(data, file_name, expected, tmpdir):
    fake_file = tmpdir.join(file_name)
    utils.write_to_file(fake_file.strpath, data)
    assert fake_file.read() == expected


def test_write_file_bad_format_fail(tmpdir):
    fake_file = tmpdir.join("format_file.bad")
    with pytest.raises(ValueError) as excinfo:
        utils.write_to_file(fake_file.strpath, data={})
    assert 'Unsupported data format.' in str(excinfo.value)
