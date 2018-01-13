#
#    Copyright 2018 Vitalii Kulanov
#

import pytest

from validocx import wrapper


@pytest.fixture(scope='module')
def docx_wrapper(document):
    return wrapper.DocumentWrapper(document)


def test_fetch_author_data(docx_wrapper):
    assert docx_wrapper.author == 'python-docx'


def test_fetch_date_of_creation(docx_wrapper):
    assert docx_wrapper.created.isoformat(' ') == '2013-12-23 23:15:00'


def test_fetch_date_of_modification(docx_wrapper):
    assert docx_wrapper.modified.isoformat(' ') == '2013-12-23 23:15:00'


def test_fetch_last_modifier_data(docx_wrapper):
    assert docx_wrapper.last_modified_by == ''


@pytest.mark.parametrize('paragraph_styles, expected_length', [
    (['Title'], 1),
    (['Heading 1', 'Heading 2'], 2),
    (['Non-existing-style'], 0),
    (None, 4)
])
def test_fetch_paragraph_data(docx_wrapper, paragraph_styles, expected_length):
    paragraphs = docx_wrapper.iter_paragraphs(paragraph_styles)
    assert len(list(paragraphs)) == expected_length


def test_fetch_section_data(docx_wrapper):
    assert len(list(docx_wrapper.iter_sections())) == 1


@pytest.mark.parametrize('p_style, expected', [
    ('Title', [[26.0, 'Calibri']]),
    ('Normal', [[12.0, 'Calibri'], [12.0, 'Calibri', 'bold'],
                [12.0, 'Calibri'], [12.0, 'Calibri', 'italic']])
])
def test_fetch_font_attributes(docx_wrapper, p_style, expected):
    p = list(docx_wrapper.iter_paragraphs(p_style))[0]
    runs = docx_wrapper.get_font_attributes(p)
    assert runs == expected


def test_fetch_section_attributes(docx_wrapper):
    section = list(docx_wrapper.iter_sections())[0]
    section_attr = docx_wrapper.get_section_attributes(section)
    assert section_attr == {'page_height': 27.94, 'left_margin': 3.175,
                            'page_width': 21.59, 'gutter': 0.0,
                            'bottom_margin': 2.54, 'orientation': 0,
                            'header_distance': 1.27, 'footer_distance': 1.27,
                            'top_margin': 2.54, 'right_margin': 3.175,
                            'start_type': 2}


def test_fetch_paragraph_attributes(docx_wrapper):
    p = list(docx_wrapper.iter_paragraphs('Normal'))[0]
    p_attr = docx_wrapper.get_paragraph_attributes(p)
    assert p_attr == {'page_break_before': None,
                      'keep_together': None,
                      'line_spacing': 1.000125,
                      'space_after': 1.000125,
                      'space_before': 1.000125,
                      'keep_with_next': True,
                      'alignment': 3,
                      'right_indent': 0.49918055555555557,
                      'line_spacing_rule': 4,
                      'left_indent': 0.49918055555555557,
                      'first_line_indent': 1.2505972222222221,
                      'widow_control': None}
