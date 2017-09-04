#
#    Copyright 2017 Vitalii Kulanov
#

import math
from validocx.wrapper import DocumentWrapper


class Validator(object):
    """Class for validating docx documents."""

    def __init__(self, document):
        """
        :param document: docx.Document
        """
        self._docx = DocumentWrapper(document)

    def validate_sections(self, schema):
        for item, section in enumerate(self._docx.iter_sections()):
            fetched_attr = self._docx.get_section_attributes(section)
            for attr, value in schema['sections'][item].items():
                if not math.isclose(fetched_attr[attr], value, rel_tol=1e-03):
                    raise ValueError(
                        "Section '{0}': Attribute '{1}' with value {2} does "
                        "not meet required value {3}".format(
                            item, attr, fetched_attr[attr], value
                        )
                    )

    def validate_styles(self, schema):
        available_styles = [style for style in schema['styles']]
        for p in self._docx.iter_paragraphs():
            if p.style.name in available_styles:
                self.validate_font(p, schema['styles'][p.style.name]['font'])
            else:
                msg = "WARNING: Unknown paragraph style: {0}"
                print(msg.format(p.style.name))

    def validate_font(self, paragraph, attributes):
        """Validate font attributes for specified paragraph."""
        fetched_attr = set(self._docx.get_font_attributes(paragraph))
        req_attr = set(attributes)
        if fetched_attr ^ req_attr:
            msg = ("Font with attributes {0} mismatch required {1} in "
                   "paragraph with style '{2}':\n'{3}'")
            raise ValueError(msg.format(fetched_attr, req_attr,
                                        paragraph.style.name, paragraph.text))


def validate(document, schema):
    validator = Validator(document)
    validator.validate_sections(schema)
    validator.validate_styles(schema)

