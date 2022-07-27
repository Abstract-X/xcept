import dataclasses
from dataclasses import dataclass, field
from typing import Set
import warnings

from xcept.formatter.formatter import Formatter
from xcept.warnings import MissingFieldWarning, UnknownFieldWarning


@dataclass
class Exception_(Exception):  # noqa
    """Base class for custom non-exit exceptions.

    The behavior is mostly inherited from the built-in Exception class.
    The difference is that this class provides more convenience when
    working with custom exception attributes, and also allows you to
    create verbose messages using standard formatting syntax.

    If for some reason you don't need to include all attributes
    in a message, define ALL_REPLACEMENT_FIELDS_IS_REQUIRED = False
    to disable checks and warnings.
    """
    ALL_REPLACEMENT_FIELDS_IS_REQUIRED = True
    _template: str = field(repr=False, metadata={"is_template": True})

    def __post_init__(self):
        """Initialize an object.

        If a template does not contain all replacement fields and
        attribute ALL_REPLACEMENT_FIELDS_IS_REQUIRED is True, the
        xcept.warnings.MissingFieldWarning occurs.
        If a template contains unknown replacement fields, the
        xcept.warnings.UnknownFieldWarning occurs.
        """
        self._fields = {
            i.name
            for i in dataclasses.fields(self)
            if not i.metadata.get("is_template")
        }
        self._formatter = Formatter()
        replacement_fields = self._formatter.get_fields(self._template)

        if self.ALL_REPLACEMENT_FIELDS_IS_REQUIRED:
            _warn_about_missing_replacement_fields(
                fields={i for i in self._fields if i not in replacement_fields},
                template=self._template
            )

        _warn_about_unknown_replacement_fields(
            fields={i for i in replacement_fields if i not in self._fields},
            template=self._template
        )

    def __str__(self):
        """Return an exception message."""
        return self.get_message()

    def get_message(self) -> str:
        """Return an exception message."""
        arguments = {
            name: value
            for name, value in vars(self).items()
            if name in self._fields
        }

        return self._formatter.get_string(self._template, **arguments)


def _warn_about_missing_replacement_fields(fields: Set[str], template: str) -> None:
    if fields:
        warnings.warn(
            message=MissingFieldWarning(
                f"No the replacement {_get_field_message_part(fields)} "
                f"in the template {template!r}!"
            ),
            stacklevel=4
        )


def _warn_about_unknown_replacement_fields(fields: Set[str], template: str) -> None:
    if fields:
        warnings.warn(
            message=UnknownFieldWarning(
                f"Unknown the replacement {_get_field_message_part(fields)} "
                f"in the template {template!r}!"
            ),
            stacklevel=4
        )


def _get_field_message_part(fields: Set[str]) -> str:
    if len(fields) == 1:
        message_part = f"field {''.join(fields)!r}"
    elif len(fields) > 1:
        message_part = f"fields {', '.join(repr(i) for i in fields)}"
    else:
        raise ValueError("No fields!")

    return message_part
