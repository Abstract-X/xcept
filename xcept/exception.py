from dataclasses import dataclass, field

from xcept.formatter import Formatter
from xcept import errors


_NON_FORMATTING_ATTRS = {"template_", "_formatter"}


@dataclass
class BaseException_(Exception):
    """Base class for exceptions."""

    ALLOW_UNUSED_ARGS = False

    template_: str = field(repr=False)

    def __post_init__(self):

        self._formatter = Formatter(allow_unused_args=self.ALLOW_UNUSED_ARGS)
        self._check_args_matching()

    def __str__(self):

        return self._get_message()

    @property
    def _formatting_attrs(self) -> dict:
        """Get attributes for formatting."""

        attrs = {}
        for key, value in vars(self).items():
            if key not in _NON_FORMATTING_ATTRS:
                attrs[key] = value

        return attrs

    def _get_message(self) -> str:
        """Get exception message."""

        return self._formatter.format(self.template_, **self._formatting_attrs)

    def _check_args_matching(self) -> None:
        """Check template arguments match attributes."""

        try:
            self._get_message()
        except KeyError as error:
            attr = error.args[0]
            raise errors.ArgsMatchingError(f"attribute {attr!r} specified in template "
                                           "was not found among the attributes!", arg=attr) from None
