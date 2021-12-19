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

    @dataclass
    class Exception_(BaseException_):
        pass

    with pytest.raises(Exception_, match=template):
        raise Exception_(template)


def test_with_args():

    @dataclass
    class Exception_(BaseException_):
        foo: str
        bar: int

    with pytest.raises(Exception_, match="error 'test' 123!"):
        raise Exception_("error {foo!r} {bar!s}!", foo="test", bar=123)


@pytest.mark.parametrize(
    ("template",),
    (
        ("{}",),
        ("{0}",),
        ("{}{0}",)
    )
)
def test_positional_arg_specified(template):

    @dataclass
    class Exception_(BaseException_):
        pass

    with pytest.raises(errors.UsedPositionalArgumentError):
        Exception_(template)


def test_keyword_arg_not_specified():

    @dataclass
    class Exception_(BaseException_):
        foo: str
        bar: int

    with pytest.raises(errors.UnusedKeywordArgumentError):
        Exception_("{foo}", foo="test", bar=123)


def test_args_matching():

    @dataclass
    class Exception_(BaseException_):
        foo: str

    with pytest.raises(errors.ArgsMatchingError):
        raise Exception_("error {foo} {unknown_arg}!", foo="test")


def test_unused_args_allowed():

    @dataclass
    class Exception_(BaseException_):
        ALLOW_UNUSED_ARGS = True
        foo: str
        bar: int

    with pytest.raises(Exception_, match="error test!"):
        raise Exception_("error {foo}!", foo="test", bar=123)
