import dataclasses
from dataclasses import dataclass, field
from typing import Set, Optional
import warnings

from xcept.formatter.formatter import Formatter
from xcept.warnings import MissingTemplateWarning, MissingFieldWarning, UnknownFieldWarning


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

    If you want to have a default template, define DEFAULT_TEMPLATE.
    """
    ALL_REPLACEMENT_FIELDS_IS_REQUIRED = True
    DEFAULT_TEMPLATE = None
    _template: Optional[str] = field(repr=False, metadata={"is_template": True})

    def __post_init__(self):
        """Initialize an object.

        If there is no a template and all replacement fields is
        required, the xcept.warnings.MissingTemplateWarning occurs.

        If there is a template and it does not contain all replacement
        fields, but all replacement fields is required, the
        xcept.warnings.MissingFieldWarning occurs.

        If there is a template and it contains unknown replacement
        fields, the xcept.warnings.UnknownFieldWarning occurs.
        """
        self._fields = {
            i.name
            for i in dataclasses.fields(self)
            if not i.metadata.get("is_template")
        }
        self._formatter = Formatter()
        template = self.get_template()
        class_name = type(self).__name__

        if template is not None:
            replacement_fields = self._formatter.get_fields(template)

            if self.ALL_REPLACEMENT_FIELDS_IS_REQUIRED:
                _warn_about_missing_replacement_fields(
                    fields={i for i in self._fields if i not in replacement_fields},
                    template=template,
                    class_name=class_name
                )

            _warn_about_unknown_replacement_fields(
                fields={i for i in replacement_fields if i not in self._fields},
                template=template,
                class_name=class_name
            )
        else:
            if self.ALL_REPLACEMENT_FIELDS_IS_REQUIRED:
                _warn_about_missing_template(class_name=class_name)

    def __str__(self):
        """Return an exception message."""
        return self.get_message()

    def get_message(self) -> str:
        """Return an exception message."""
        template = self.get_template()

        if template is not None:
            arguments = {
                name: value
                for name, value in vars(self).items()
                if name in self._fields
            }

            return self._formatter.get_string(template, **arguments)

        return str()

    def get_template(self) -> Optional[str]:
        """Return an exception message template."""
        if self._template is not None:
            return self._template
        elif self.DEFAULT_TEMPLATE is not None:
            return self.DEFAULT_TEMPLATE


def _warn_about_missing_template(class_name: str) -> None:
    warnings.warn(
        message=MissingTemplateWarning(f"No a template ({class_name})!"),
        stacklevel=4
    )


def _warn_about_missing_replacement_fields(
    fields: Set[str],
    template: str,
    class_name: str
) -> None:
    if fields:
        warnings.warn(
            message=MissingFieldWarning(
                f"No the replacement {_get_field_message_part(fields)} "
                f"in the template {template!r} ({class_name})!"
            ),
            stacklevel=4
        )


def _warn_about_unknown_replacement_fields(
    fields: Set[str],
    template: str,
    class_name: str
) -> None:
    if fields:
        warnings.warn(
            message=UnknownFieldWarning(
                f"Unknown the replacement {_get_field_message_part(fields)} "
                f"in the template {template!r} ({class_name})!"
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
