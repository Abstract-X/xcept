from dataclasses import dataclass

import pytest

from xcept import BaseException_
from xcept import errors


@pytest.mark.parametrize(
    ("template",),
    (
        ("err!",),
        ("error!",)
    )
)
def test(template):

    @dataclass(frozen=True)
    class Error(BaseException_):
        pass

    with pytest.raises(Error, match="error!"):
        raise Error("error!")


def test_keyword_arguments():

    @dataclass(frozen=True)
    class Error(BaseException_):
        foo: str
        bar: int

    with pytest.raises(Error, match="error 'test' 123!"):
        raise Error("error {foo!r} {bar!s}!", foo="test", bar=123)


@pytest.mark.parametrize(
    ("template",),
    (
        ("{}",),
        ("{0}",),
        ("{}{0}",)
    )
)
def test_positional_argument_specified(template):

    @dataclass(frozen=True)
    class Error(BaseException_):
        pass

    with pytest.raises(errors.UsedPositionalArgumentError):
        Error(template)


def test_keyword_argument_not_specified():

    @dataclass(frozen=True)
    class Error(BaseException_):
        foo: str
        bar: int

    with pytest.raises(errors.UnusedKeywordArgumentError):
        Error("{foo}", foo="test", bar=123)
