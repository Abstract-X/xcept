from string import Formatter
from typing import Set

from xcept.formatter.helpers import get_field_from_expression


class HardFormatter(Formatter):

    def get_keyword_fields(self, string: str) -> Set[str]:
        fields = set()

        for i in self.parse(string):
            expression = i[1]

            if expression:
                field = get_field_from_expression(expression)

                if not field.isdigit():
                    fields.add(field)

        return fields

    def check_positional_fields(self, string: str) -> bool:
        for i in self.parse(string):
            expression = i[1]

            if expression is not None:
                field = get_field_from_expression(expression)

                if (field == "") or field.isdigit():
                    return True

        return False
