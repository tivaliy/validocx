#
#    Copyright 2017 Vitalii Kulanov
#

import pytest

from validocx import utils


def test_read_from_file_yaml(tmpdir):
    fake_data = """
---
fake:
  foo:
    - bar
"""
    fake_file = tmpdir.join("fake.yaml")
    fake_file.write(fake_data)
    data = utils.read_from_file(fake_file.strpath)
    assert data == {'fake': {'foo': ['bar']}}


def test_read_from_file_json(tmpdir):
    fake_data = '{"fake":{"foo":["bar"]}}'
    fake_file = tmpdir.join("fake.json")
    fake_file.write(fake_data)
    data = utils.read_from_file(fake_file.strpath)
    assert data == {'fake': {'foo': ['bar']}}


def test_read_from_file_bad_format_fail(tmpdir):
    fake_file = tmpdir.join("format_file.bad")
    fake_file.write('')
    with pytest.raises(ValueError) as excinfo:
        utils.read_from_file(fake_file.strpath)
    assert 'Unsupported data format.' in str(excinfo.value)


def test_write_file_json(tmpdir):
    expected_value = """{
    "fake": {
        "foo": [
            "bar"
        ]
    }
}"""
    data = {'fake': {'foo': ['bar']}}
    fake_file = tmpdir.join("fake.json")
    utils.write_to_file(fake_file.strpath, data)
    assert fake_file.read() == expected_value


def test_write_file_yaml(tmpdir):
    data = {'fake': {'foo': ['bar']}}
    fake_file = tmpdir.join("fake.yaml")
    utils.write_to_file(fake_file.strpath, data=data)
    assert fake_file.read() == 'fake:\n  foo:\n  - bar\n'


def test_write_file_bad_format_fail(tmpdir):
    fake_file = tmpdir.join("format_file.bad")
    with pytest.raises(ValueError) as excinfo:
        utils.write_to_file(fake_file.strpath, data={})
    assert 'Unsupported data format.' in str(excinfo.value)
