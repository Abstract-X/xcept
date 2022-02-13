from dataclasses import dataclass

import pytest

from xcept import Exception_
from xcept import errors


@pytest.mark.parametrize(
    ("template",),
    (
        ("err!",),
        ("error!",)
    )
)
def test_behavior(template):
    with pytest.raises(Exception_, match=template):
        raise Exception_(template)


def test_with_args():
    @dataclass
    class TestException(Exception_):
        foo: str
        bar: int

    with pytest.raises(TestException, match="error 'test' 123!"):
        raise TestException(
            "error {foo!r} {bar!s}!",
            foo="test", bar=123
        )


@pytest.mark.parametrize(
    ("template",),
    (
        ("{}",),
        ("{0}",),
        ("{}{0}",)
    )
)
def test_positional_arg_specified(template):
    with pytest.raises(errors.UsedPositionalArgError):
        Exception_(template)


def test_keyword_arg_not_specified():
    @dataclass
    class TestException(Exception_):
        foo: str
        bar: int

    with pytest.raises(errors.UnusedKeywordArgError):
        TestException("{foo}", foo="test", bar=123)


def test_args_matching():
    @dataclass
    class TestException(Exception_):
        foo: str

    with pytest.raises(errors.ArgMatchingError):
        raise TestException("error {foo} {unknown_arg}!", foo="test")


def test_unused_args_allowed():
    @dataclass
    class TestException(Exception_):
        ALLOW_UNUSED_ARGS = True
        foo: str
        bar: int

    with pytest.raises(TestException, match="error test!"):
        raise TestException("error {foo}!", foo="test", bar=123)
