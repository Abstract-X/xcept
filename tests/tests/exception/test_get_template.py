from dataclasses import dataclass

import pytest

from xcept import Exception_


TEMPLATE_TEST_DATA = (
    ("template",),
    (
        ("foo_template",),
        ("bar_template",),
    )
)
DEFAULT_TEMPLATE_TEST_DATA = TEMPLATE_TEST_DATA


@pytest.mark.parametrize(*TEMPLATE_TEST_DATA)
def test_template(template: str) -> None:
    @dataclass
    class TestException(Exception_):
        pass

    exception = TestException(template)

    assert exception.get_template() == template


@pytest.mark.parametrize(*DEFAULT_TEMPLATE_TEST_DATA)
def test_default_template(template: str) -> None:
    @dataclass
    class TestException(Exception_):
        DEFAULT_TEMPLATE = template

    exception = TestException(None)

    assert exception.get_template() == template


def test_missing_template() -> None:
    @dataclass
    class TestException(Exception_):
        pass

    exception = TestException(None)

    assert exception.get_template() is None
