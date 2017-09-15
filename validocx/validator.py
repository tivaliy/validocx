#
#    Copyright 2017 Vitalii Kulanov
#

__all__ = ['Validator', 'validate']

import jsonschema
import logging
import math

from docx import Document

from .wrapper import DocumentWrapper
from .schema import RequirementsSchema

logger = logging.getLogger(__name__)


class Validator(object):
    """Class for validating docx document."""

    schema = RequirementsSchema()

    def __init__(self, document):
        """
        :param document: docx.Document
        """
        self._docx = DocumentWrapper(document)

    def validate_sections(self, section_requirements):
        """Validate sections of a document."""

        for i, section in enumerate(self._docx.iter_sections()):
            unit = section_requirements[i]['unit']
            fetched_attr = self._docx.get_section_attributes(section,
                                                             unit=unit)
            for attr, value in section_requirements[i]['attributes'].items():
                if not math.isclose(fetched_attr[attr], value, rel_tol=1e-02):
                    msg = ("Section '{0}': attribute '{1}' with value {2} "
                           "does not match required value "
                           "{3}".format(i, attr, fetched_attr[attr], value))
                    logger.error(msg)

    def validate_styles(self, style_requirements):
        """Validate styles of a document, i.e. font and paragraph."""

        for paragraph in self._docx.iter_paragraphs():
            if paragraph.style.name in style_requirements:
                self.validate_paragraph(
                    paragraph,
                    style_requirements[paragraph.style.name]['paragraph']
                )
                self.validate_font(
                    paragraph,
                    style_requirements[paragraph.style.name]['font'])
            else:
                msg = "Undefined style: '{0}'."
                logger.warning(msg.format(paragraph.style.name))

    def validate_font(self, paragraph, font_requirements):
        """Validate font in a specified paragraph."""

        unit = font_requirements['unit']
        requirements = font_requirements['attributes']
        fetched_attr = self._docx.get_font_attributes(paragraph, unit=unit)
        for i, attr in enumerate(fetched_attr):
            if set(attr) ^ set(requirements):
                msg = ("Font attributes ({0}) mismatch required ({1}) in "
                       "paragraph with style '{2}':\n'{3}'".format(
                        ', '.join(str(a) for a in attr),
                        ', '.join(str(r) for r in requirements),
                        paragraph.style.name, paragraph.runs[i].text))
                logger.error(msg)

    def validate_paragraph(self, paragraph, paragraph_requirements):
        """Validate paragraph."""

        unit = paragraph_requirements['unit']
        fetched_attr = self._docx.get_paragraph_attributes(paragraph,
                                                           unit=unit)
        for attr, value in paragraph_requirements['attributes'].items():
            if fetched_attr[attr] is not None:
                if not math.isclose(fetched_attr[attr], value, rel_tol=1e-02):
                    msg = ("The attribute of paragraph '{0}' ({1}) with value "
                           "{2} does not match required value {3}: "
                           "\n'{4}'".format(attr, paragraph.style.name,
                                            fetched_attr[attr], value,
                                            paragraph.text))
                    logger.error(msg)
            else:
                logger.error("The attribute of paragraph '{0}' is not "
                             "defined. The required value is {1}: "
                             "\n'{2}'".format(attr, value, paragraph.text))

    def validate(self, document_requirements):
        """Validate the whole document."""

        self._validate_schema(document_requirements,
                              self.schema.requirements_schema)
        logger.info("Start validating sections.")
        self.validate_sections(document_requirements['sections'])
        logger.info("Start validating styles.")
        self.validate_styles(document_requirements['styles'])
        logger.info("Validation process completed.\n")

    @staticmethod
    def _validate_schema(requirements, schema):
        """Validate requirements schema."""

        logger.info("Start validating requirements schema.")
        try:
            jsonschema.validate(requirements, schema)
        except jsonschema.exceptions.ValidationError as e:
            logger.exception(e)
            raise


def validate(docx_path, requirements):
    """Validates docx document.

    :param docx_path: path to docx file to be validated
    :param requirements: document requirements as a dict (see examples)
    """
    document = Document(docx_path)
    validator = Validator(document)
    validator.validate(requirements)
