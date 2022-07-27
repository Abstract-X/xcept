from typing import Set

from xcept.formatter.formatters.hard import HardFormatter
from xcept.formatter.formatters.soft import SoftFormatter


class Formatter:

    def __init__(self):
        self._hard_formatter = HardFormatter()

    # noinspection PyMethodMayBeStatic
    def get_string(self, template: str, **kwargs) -> str:
        return SoftFormatter(set(kwargs)).format(template, **kwargs)

    def get_fields(self, template: str) -> Set[str]:
        return self._hard_formatter.get_fields(template)
