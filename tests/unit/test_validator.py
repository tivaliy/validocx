#
#    Copyright 2018 Vitalii Kulanov
#

import logging

import pytest

from validocx import Validator


@pytest.fixture(scope='module')
def validator(document):
    return Validator(document)


@pytest.mark.parametrize('section_requirements, expected', [
    ([{"attributes": {'orientation': 1,
                      'page_width': 21.59,
                      'page_height': 27.94},
       "unit": "cm"}],
     [('validocx.validator', logging.ERROR,
       "'Section 0': attribute 'orientation' with value "
       "PORTRAIT (0) does not match required value 1")]),
    ([{"attributes": {'orientation': 0,
                      'page_width': 21.59,
                      'page_height': 27.94},
       "unit": "cm"}], []),
])
def test_validate_sections(validator, caplog, section_requirements, expected):
    validator.validate_sections(section_requirements)
    assert caplog.record_tuples == expected
