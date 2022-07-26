from dataclasses import dataclass
from typing import Any

from xcept import Exception_
from tests.tests.exception.helpers import pytest_message_parametrize


@pytest_message_parametrize
def test_behavior(template: str, test_field_value: str, expected_result: str) -> None:
    @dataclass
    class TestException(Exception_):
        test_field: Any

    exception = TestException(template, test_field=test_field_value)

    assert exception.get_message() == expected_result
