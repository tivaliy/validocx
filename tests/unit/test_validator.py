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
       "unit": "cm"},
      {"attributes": {'orientation': 0,
                      'page_width': 21.59,
                      'page_height': 27.94},
       "unit": "cm"}],
     [('validocx.validator', logging.ERROR,
       "'Section 0': attribute 'orientation' with value "
       "PORTRAIT (0) does not match required value 1")]),
    ([{"attributes": {'orientation': 0},
       "unit": "cm"},
      {"attributes": {'orientation': 0},
       "unit": "cm"}], []),
    ([{"attributes": {'orientation': 0,
                      'page_width': 21.59,
                      'page_height': 27.94},
       "unit": "cm"}],
     [('validocx.validator', logging.WARNING,
       "The requirements for 'Section 1' are not specified.")]),
])
def test_validate_sections(validator, caplog, section_requirements, expected):
    validator.validate_sections(section_requirements)
    assert caplog.record_tuples == expected


@pytest.mark.parametrize('style_requirements, expected', [
    ({"Title": {
        "font": {"unit": "pt", "attributes": [26, "Calibri"]},
        "paragraph": {"unit": "cm", "attributes": {"line_spacing": 1}}
    }},
     [('validocx.validator', logging.WARNING, "Undefined style: 'Heading 1'."),
      ('validocx.validator', logging.WARNING, "Undefined style: 'Heading 2'."),
      ('validocx.validator', logging.WARNING, "Undefined style: 'Normal'."),
      ('validocx.validator', logging.WARNING, "Undefined style: 'Normal'.")]
    ),
    ({"Title": {
        "font": {"unit": "pt", "attributes": [14, "Calibri"]},
        "paragraph": {"unit": "cm", "attributes": {"line_spacing": 1}}
    }},
     [('validocx.validator', logging.ERROR,
       "Font attributes (26.0, Calibri) mismatch required (14, Calibri) "
       "in paragraph with style 'Title':\n'Fake Title'"),
      ('validocx.validator', logging.WARNING, "Undefined style: 'Heading 1'."),
      ('validocx.validator', logging.WARNING, "Undefined style: 'Heading 2'."),
      ('validocx.validator', logging.WARNING, "Undefined style: 'Normal'."),
      ('validocx.validator', logging.WARNING, "Undefined style: 'Normal'.")]
    ),
])
def test_validate_styles(validator, caplog, style_requirements, expected):
    validator.validate_styles(style_requirements)
    assert caplog.record_tuples == expected


@pytest.mark.parametrize('font_requirements, expected', [
    ({"unit": "pt", "attributes": [26, "Calibri"]}, []),
    ({"unit": "pt", "attributes": [26, "Times New Roman"]},
     [('validocx.validator', 40, "Font attributes (26.0, Calibri) mismatch "
                                 "required (26, Times New Roman) in paragraph "
                                 "with style 'Title':\n'Fake Title'")])
])
def test_validate_font(validator, caplog, font_requirements, expected):
    paragraph = list(validator._docx.iter_paragraphs('Title'))[0]
    validator.validate_font(paragraph, font_requirements)
    assert caplog.record_tuples == expected


@pytest.mark.parametrize('p_requirements, expected', [
    ({"unit": "cm", "attributes": {"line_spacing": 1, "alignment": 3}}, []),
    ({"unit": "cm", "attributes": {"page_break_before": True}},
     [('validocx.validator', logging.ERROR,
       "The attribute of paragraph 'page_break_before' is not defined. "
       "The required value is True: \n'Some bold and some italic.'")]),
    ({"unit": "cm", "attributes": {"line_spacing": 1, "alignment": 1}},
     [('validocx.validator', logging.ERROR,
       "The attribute of paragraph 'alignment' (Normal) with value JUSTIFY (3)"
       " does not match required value 1: \n'Some bold and some italic.'")])
])
def test_validate_paragraph(validator, caplog, p_requirements, expected):
    paragraph = list(validator._docx.iter_paragraphs('Normal'))[0]
    validator.validate_paragraph(paragraph, p_requirements)
    assert caplog.record_tuples == expected
