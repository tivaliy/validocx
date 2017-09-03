#
#    Copyright 2017 Vitalii Kulanov
#


class DOCXDocument(object):
    """Class for retrieving docx document attributes."""

    def __init__(self, document):
        self._document = document
        self._author = document.core_properties.author
        self._created = document.core_properties.created
        self._modified = document.core_properties.modified
        self._last_modified_by = document.core_properties.last_modified_by

    @property
    def author(self):
        return self._author

    @property
    def created(self):
        return self._created

    @property
    def modified(self):
        return self._modified

    @property
    def last_modified_by(self):
        return self._last_modified_by

    def iter_paragraphs(self, styles=None):
        """Iterate over paragraphs of document.

        :param styles: Paragraph styles as a list (tuple) of strings that
                       have to be fetched. None value implies all paragraphs
        :type styles: tuple|list of string
        """

        for paragraph in self._document.paragraphs:
            if styles is not None:
                for style in styles:
                    if paragraph.style.name in style:
                        yield paragraph
            else:
                yield paragraph

    def iter_sections(self):
        """Iterate over sections in docx document."""

        for section in self._document.sections:
            yield section

    def get_font_attributes(self, paragraph, unit='pt'):
        """Get font attributes for specified paragraph."""

        font_size = self._find_attribute(paragraph.style, 'font', 'size')
        font_family = self._find_attribute(paragraph.style, 'font', 'name')
        fetched_attributes = [font_size.__getattribute__(unit), font_family]
        for attribute, member in type(paragraph.style.font).__dict__.items():
            if isinstance(member, property):
                if member.__get__(paragraph.style.font) is True:
                    fetched_attributes.append(attribute)
        return fetched_attributes

    def get_section_attributes(self, section, unit='cm'):
        """Get attributes for specified section."""

        fetched_attributes = {
            attr: self._convert_unit(section.__getattribute__(attr), unit)
            for attr, p in type(section).__dict__.items()
            if isinstance(p, property)
        }
        return fetched_attributes

    def get_paragraph_attributes(self, paragraph, unit='cm'):
        """Get attributes for specified paragraph."""

        _except_attributes = ('tab_stops',)

        fetched_attributes = {}
        for attr, member in type(paragraph.paragraph_format).__dict__.items():
            if isinstance(member, property) and attr not in _except_attributes:
                fetched_attributes[attr] = self._convert_unit(
                        paragraph.paragraph_format.__getattribute__(attr) or
                        self._find_attribute(paragraph.style,
                                             'paragraph_format', attr), unit)
        return fetched_attributes

    def _find_attribute(self, p_style, p_element, attr):
        value = p_style.__getattribute__(p_element).__getattribute__(attr)
        if value is None and p_style.base_style is not None:
            return self._find_attribute(p_style.base_style, p_element, attr)
        return value

    @staticmethod
    def _convert_unit(value, unit):
        try:
            value = value.__getattribute__(unit)
        except AttributeError:
            pass
        return value


def extract(document, styles):
    """Extract data from docx document.

    :param document: Document object loaded from docx
    :type document: docx.Document
    :param styles: Styles defined that have to be fetched
    :type styles: tuple\list
    """

    docx = DOCXDocument(document)
    return {
        "author": docx.author,
        "created": docx.created.isoformat(),
        "modified": docx.modified.isoformat(),
        "last_modified_by": docx.last_modified_by,
        "sections": [
            docx.get_section_attributes(section) for section
            in docx.iter_sections()
        ],
        "contents": {
            "headings": [
                {
                    "text": heading.text,
                    "style": heading.style.name,
                    "font": docx.get_font_attributes(heading),
                    "paragraph_format": docx.get_paragraph_attributes(heading)
                } for heading in docx.iter_paragraphs(styles=styles)
            ]
        }
    }
