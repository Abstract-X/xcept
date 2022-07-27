from string import Formatter
from typing import Set

from xcept.formatter.helpers import get_field_from_expression


class HardFormatter(Formatter):

    def get_fields(self, string: str) -> Set[str]:
        fields = set()

        for i in self.parse(string):
            expression = i[1]

            if expression is not None:
                field, _ = get_field_from_expression(expression)
                fields.add(field)

        return fields
