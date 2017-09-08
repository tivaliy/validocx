#
#    Copyright 2017 Vitalii Kulanov
#


class DocumentWrapper(object):
    """Wrapper class for retrieving docx document attributes."""

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

    def iter_paragraphs(self, style=None):
        """Iterate over paragraphs of document.

        :param style: Paragraph style that have to be fetched.
                      None value implies all paragraphs
        :type style: str
        """

        for paragraph in self._document.paragraphs:
            if style:
                if paragraph.style.name == style:
                    yield paragraph
            else:
                yield paragraph

    def iter_sections(self):
        """Iterate over sections in docx document."""

        for section in self._document.sections:
            yield section

    def get_font_attributes(self, paragraph, unit='pt'):
        """Get font attributes for specified paragraph."""

        runs = []
        for run in paragraph.runs:
            size = (run.font.size or
                    self._find_paragraph_attribute(paragraph.style,
                                                   'font', 'size'))
            family = (run.font.name or
                      self._find_paragraph_attribute(paragraph.style,
                                                     'font', 'name'))
            fetched_attributes = [size.__getattribute__(unit), family]
            for attr, member in type(paragraph.style.font).__dict__.items():
                if isinstance(member, property):
                    val = (run.font.__getattribute__(attr) or
                           paragraph.style.font.__getattribute__(attr))
                    if val is True:
                        fetched_attributes.append(attr)
            runs.append(fetched_attributes)
        return runs

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
                    self._find_paragraph_attribute(paragraph.style,
                                                   'paragraph_format',
                                                   attr),
                    unit)
        return fetched_attributes

    def _find_paragraph_attribute(self, p_style, p_element, attr):
        value = p_style.__getattribute__(p_element).__getattribute__(attr)
        if value is None and p_style.base_style is not None:
            return self._find_paragraph_attribute(p_style.base_style,
                                                  p_element, attr)
        return value

    @staticmethod
    def _convert_unit(value, unit):
        try:
            value = value.__getattribute__(unit)
        except AttributeError:
            pass
        return value
