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
        last_field = None

        for text, field_expression, format_spec, conversion in super().parse(format_string):
            texts.append(text)

            if field_expression is not None:
                field = get_field_from_expression(field_expression)
                last_field = field

                if field in self._fields:
                    parts.append(
                        (UNKNOWN_FIELD_VALUE.join(texts), field_expression, format_spec, conversion)
                    )
                    texts.clear()

        if texts:
            text = UNKNOWN_FIELD_VALUE.join(texts)

            if last_field is not None:
                text += UNKNOWN_FIELD_VALUE

            parts.append((text, None, None, None))

        return parts
