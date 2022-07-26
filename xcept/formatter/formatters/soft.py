from string import Formatter
from typing import Optional, Set, List, Tuple

from xcept.formatter.helpers import get_field_from_expression


UNKNOWN_FIELD_VALUE = "<UNKNOWN>"


class SoftFormatter(Formatter):

    def __init__(self, fields: Set[str]):
        self._fields = fields

    def parse(
        self,
        format_string: str
    ) -> List[Tuple[str, Optional[str], Optional[str], Optional[str]]]:
        parts = []
        texts = []

        for text, field_expression, format_spec, conversion in super().parse(format_string):
            if field_expression is not None:
                field, separator = get_field_from_expression(field_expression)

                if separator == "=":
                    text += field_expression
                    field_expression = field
                    conversion = "r"

                if field in self._fields:
                    parts.append(("".join(texts) + text, field_expression, format_spec, conversion))
                    texts.clear()
                else:
                    texts.append(text + UNKNOWN_FIELD_VALUE)
            else:
                texts.append(text)

        if texts:
            parts.append(("".join(texts), None, None, None))

        return parts
