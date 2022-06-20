from dataclasses import dataclass

from xcept import Exception_


def test_behavior():
    @dataclass
    class TestException(Exception_):
        pass

    exception = TestException("error!")

    assert exception.get_template() == "error!"


def test_arg_matching():
    @dataclass
    class TestException(Exception_):
        foo: int
        bar: int

        def get_template(self) -> str:
            return super().get_template() + "{bar}"

    exception = TestException("{foo}", foo=1, bar=2)

    assert exception.get_template() == "{foo}{bar}"
