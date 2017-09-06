#
#    Copyright 2017 Vitalii Kulanov
#

import jsonschema
import logging
import math
from validocx.wrapper import DocumentWrapper

logger = logging.getLogger(__name__)

_REQUIREMENTS_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "styles": {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "properties": {
                    "font": {
                        "type": "array",
                        "uniqueItems": True
                    },
                    "paragraph_format": {
                        "type": "object",
                        "properties": {
                            "first_line_indent": {"type": "number"},
                            "keep_together": {"type": "number"},
                            "keep_with_next": {"type": "number"},
                            "left_indent": {"type": "number"},
                            "line_spacing": {"type": "number"},
                            "line_spacing_rule": {"type": "number"},
                            "page_break_before": {"type": "number"},
                            "right_indent": {"type": "number"},
                            "space_after": {"type": "number"},
                            "space_before": {"type": "number"}
                        }
                    }
                },
                "required": ["font", "paragraph_format"],
            }
        },
        "sections": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "right_margin": {"type": "number"},
                    "start_type": {"type": "number"},
                    "top_margin": {"type": "number"},
                    "footer_distance": {"type": "number"},
                    "header_distance": {"type": "number"},
                    "left_margin": {"type": "number"},
                    "bottom_margin": {"type": "number"},
                    "orientation": {"type": "number"},
                    "page_height": {"type": "number"},
                    "page_width": {"type": "number"}
                },
                "additionalProperties": False
            }
        }
    },
    "required": ["styles", "sections"]
}


class Validator(object):
    """Class for validating docx documents."""

    def __init__(self, document):
        """
        :param document: docx.Document
        """
        self._docx = DocumentWrapper(document)

    def validate_sections(self, section_schema):
        """Validate sections of documents."""

        logger.info("Start validating sections.")
        for item, section in enumerate(self._docx.iter_sections()):
            fetched_attr = self._docx.get_section_attributes(section)
            for attr, value in section_schema['sections'][item].items():
                if not math.isclose(fetched_attr[attr], value, rel_tol=1e-03):
                    msg = ("Section '{0}': attribute '{1}' with value {2} "
                           "does not meet required value "
                           "{3}".format(item, attr, fetched_attr[attr], value))
                    logger.error(msg)
                    raise ValueError(msg)

    def validate_styles(self, style_schema):
        """Validate styles of documents."""

        logger.info("Start validating styles.")
        available_styles = [style for style in style_schema['styles']]
        for paragraph in self._docx.iter_paragraphs():
            if paragraph.style.name in available_styles:
                self.validate_font(
                    paragraph,
                    style_schema['styles'][paragraph.style.name]['font']
                )
            else:
                msg = "Undefined paragraph style: {0}"
                logger.warning(msg.format(paragraph.style.name))

    def validate_font(self, paragraph, font_schema):
        """Validate font for specified paragraph."""

        fetched_attr = set(self._docx.get_font_attributes(paragraph))
        req_attr = set(font_schema)
        if fetched_attr ^ req_attr:
            msg = (
                "Font with attributes {0} mismatch required {1} in "
                "paragraph with style '{2}':\n'{3}'".format(
                    fetched_attr, req_attr,
                    paragraph.style.name, paragraph.text))
            logger.error(msg)
            raise ValueError(msg)

    def validate(self, requirements):
        try:
            jsonschema.validate(requirements, _REQUIREMENTS_SCHEMA)
        except jsonschema.exceptions.ValidationError as exc:
            logger.exception(exc)
            raise
        self.validate_sections(requirements)


def validate(document, requirements):
    validator = Validator(document)
    validator.validate(requirements)
