#
#    Copyright 2017 Vitalii Kulanov
#


class RequirementsSchema(object):

    @property
    def requirements_schema(self):
        return {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "type": "object",
            "properties": {
                "styles": self.styles_schema,
                "sections": self.sections_schema
            },
            "required": ["styles", "sections"]
        }

    @property
    def styles_schema(self):
        return {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "properties": {
                    "font": self.font_schema,
                    "paragraph": {
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
                "required": ["font", "paragraph"],
            }
        }

    @property
    def sections_schema(self):
        return {
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

    @property
    def font_schema(self):
        return {
            "type": "array",
            "uniqueItems": True
        }
