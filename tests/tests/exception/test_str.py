from dataclasses import dataclass
from typing import Any

import pytest

from xcept import Exception_
from tests.tests.exception.test_get_message import (
    BEHAVIOR_TEST_DATA,
    DEFAULT_TEMPLATE_TEST_DATA
)


@pytest.mark.parametrize(*BEHAVIOR_TEST_DATA)
def test_behavior(template: str, test_field_value: str, expected_result: str) -> None:
    @dataclass
    class TestException(Exception_):
        test_field: Any

    exception = TestException(template, test_field=test_field_value)

    assert str(exception) == expected_result


@pytest.mark.parametrize(*DEFAULT_TEMPLATE_TEST_DATA)
def test_default_template(template: str, test_field_value: str, expected_result: str) -> None:
    @dataclass
    class TestException(Exception_):
        DEFAULT_TEMPLATE = template
        test_field: Any

    exception = TestException(None, test_field=test_field_value)

    assert str(exception) == expected_result


def test_missing_template() -> None:
    @dataclass
    class TestException(Exception_):
        pass

    exception = TestException(None)

    assert str(exception) == str()
