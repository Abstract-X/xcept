# xcept

[![PyPI version](https://badge.fury.io/py/xcept.svg)](https://badge.fury.io/py/xcept)
[![GitHub license](https://img.shields.io/github/license/Abstract-X/xcept)](https://github.com/Abstract-X/xcept/blob/main/LICENSE)

**xcept** is a package for the convenience of creating exceptions.

---

### Installation

```commandline
pip install xcept
```

---

### Usage

To create a new exception class, you need to inherit from `BaseException_` from the `xcept` package and specify a `dataclass` decorator:
```python3
from dataclasses import dataclass

from xcept import BaseException_


@dataclass
class ExampleException(BaseException_):
    foo: str
    bar: int
```

To create an exception object, you need to pass a message template and keyword arguments:
```python3
try:
    raise ExampleException("error {foo} {bar}!", foo="test", bar=12345)
except ExampleException as exception:
    print(exception)  # error test 12345!
    print(repr(exception))  # ExampleException(foo='test', bar=12345)
    raise


# Traceback (most recent call last):
#   raise ExampleException("error {foo} {bar}!", foo="test", bar=12345)
# ExampleException: error test 12345!
```

By default, all arguments are required to be inserted into the template. If there are no arguments in the template, this will lead to an error:
```python3
ExampleException("error {bar}!", foo="test", bar=12345)


# Traceback (most recent call last):
#   ExampleException("error {bar}!", foo="test", bar=12345)
# xcept.errors.UnusedKeywordArgumentError: keyword argument 'foo' is not used!
```

If you don't want to have a detailed message, you can define `ALLOW_UNUSED_ARGS = True`:
```python3
from dataclasses import dataclass

from xcept import BaseException_


@dataclass
class ExampleException(BaseException_):    
    ALLOW_UNUSED_ARGS = True
    foo: str
    bar: int


raise ExampleException("error {bar}!", foo="test", bar=12345)


# Traceback (most recent call last):
#   raise ExampleException("error {bar}!", foo="test", bar=12345)
# ExampleException: error 12345!
```