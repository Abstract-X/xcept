from dataclasses import dataclass

import pytest

from xcept import Exception_
from xcept.warnings import MissingTemplateWarning, MissingFieldWarning, UnknownFieldWarning


MISSING_REPLACEMENT_FIELD_TEST_DATA = (
    ("template",),
    (
        ("",),
        ("test_field",),
        ("{{test_field}}",),
        ("message",)
    )
)
UNKNOWN_REPLACEMENT_FIELD_TEST_DATA = (
    ("template",),
    (
        # Positional field without index
        ("{}",),
        ("{!r}",),
        ("{:.2f}",),

        # Positional field with index
        ("{0}",),
        ("{0!r}",),
        ("{0:.2f}",),
        ("{0[0]}",),
        ("{0.attribute}",),

        # Keyword field
        ("{test_field} {unknown_field}",),
        ("{test_field} {unknown_field!r}",),
        ("{test_field} {unknown_field:.2f}",),
        ("{test_field} {unknown_field[0]}",),
        ("{test_field} {unknown_field.attribute}",),
    )
)


def test_missing_template() -> None:
    @dataclass
    class TestException(Exception_):
        pass

    with pytest.warns(MissingTemplateWarning):
        TestException(None)


@pytest.mark.parametrize(*MISSING_REPLACEMENT_FIELD_TEST_DATA)
def test_missing_replacement_fields(template: str) -> None:
    @dataclass
    class TestException(Exception_):
        test_field: str

    with pytest.warns(MissingFieldWarning):
        TestException(template, test_field="test_value")


@pytest.mark.parametrize(*UNKNOWN_REPLACEMENT_FIELD_TEST_DATA)
def test_unknown_replacement_fields(template: str) -> None:
    @dataclass
    class TestException(Exception_):
        test_field: str

    with pytest.warns(UnknownFieldWarning):
        TestException(template, test_field="test_value")
