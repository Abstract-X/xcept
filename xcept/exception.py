from dataclasses import dataclass, field

from xcept.formatter import Formatter


@dataclass(frozen=True)
class BaseException_(Exception):

    _NON_FORMATTING_ATTRS = {"template_", "_formatter"}

    template_: str = field(repr=False)
    _formatter: Formatter = field(default_factory=Formatter, init=False, repr=False)

    def __post_init__(self):

        try:
            self._get_message()
        except KeyError as error:
            attr = error.args[0]
            raise KeyError(f"attribute {attr!r} specified in template "
                           "was not found among the attributes!") from None

    def __str__(self):

        return self._get_message()

    @property
    def _formatting_attrs(self) -> dict:

        attrs = vars(self).copy()
        for attr in self._NON_FORMATTING_ATTRS:
            del attrs[attr]

        return attrs

    def _get_message(self) -> str:

        return self._formatter.format(self.template_, **self._formatting_attrs)
