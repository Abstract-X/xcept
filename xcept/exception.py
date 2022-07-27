import dataclasses
from dataclasses import dataclass, field
from typing import Set
import warnings

from xcept.formatter.formatter import Formatter
from xcept.warnings import MissingFieldWarning, UnknownFieldWarning


@dataclass
class Exception_(Exception):  # noqa
    ALL_REPLACEMENT_FIELDS_IS_REQUIRED = True
    _template: str = field(repr=False, metadata={"is_template": True})

    def __post_init__(self):
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
        return self.get_message()

    def get_message(self) -> str:
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
