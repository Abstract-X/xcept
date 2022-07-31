# xcept

[![PyPI version](https://badge.fury.io/py/xcept.svg)](https://badge.fury.io/py/xcept)
[![Python](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org)
[![GitHub license](https://img.shields.io/github/license/Abstract-X/xcept)](https://github.com/Abstract-X/xcept/blob/main/LICENSE)

`xcept` is a Python package for the convenience of creating exceptions.

---

### Installation

```commandline
pip install xcept
```

---

### Usage

#### Built-in `Exception`

Usually exceptions are created like this:

```python3
class Error(Exception):  # Base error class of your application or library
    pass


class FooError(Error):  # Concrete error class
    pass


class BarError(Error):  # Concrete error class
    pass
```

It looks pretty simple.
Let's try to create exceptions with arguments:

```python3
class Error(Exception):

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


class FooError(Error):

    def __init__(self, message: str, a: str):
        super().__init__(message=message)
        self.a = a


class BarError(Error):

    def __init__(self, message: str, b: str, c: int):
        super().__init__(message=message)
        self.b = b
        self.c = c
```

In the simplest case we have to use `super` each time to initialize a new exception. And we also pass an already prepared message.  
This does not allow us from getting a modified message when the attributes change:

```python3
>>> a = "value"
>>> error = FooError(f"Error (a='{a}')!", a)
>>> raise error
Traceback (most recent call last):
  File "<input>", line 1
__main__.FooError: Error (a='value')!
>>> 
>>> error.a = "new_value"
>>> raise error
Traceback (most recent call last):
  File "<input>", line 1
__main__.FooError: Error (a='value')!
```

#### xcept `Exception_`

The idea of `xcept` is based on use of `dataclasses`:

```python3
from dataclasses import dataclass

from xcept import Exception_


@dataclass
class Error(Exception_):
    pass


@dataclass
class FooError(Error):
    a: str


@dataclass
class BarError(Error):
    b: str
    c: int
```

The first argument is always a message template with replacement fields:

```python3
>>> error = FooError("Error ({a=})!", a="value")
>>> raise error
Traceback (most recent call last):
  File "<input>", line 1
__main__.FooError: Error (a='value')!
>>>
>>> error.a = "new_value"
>>> raise error
Traceback (most recent call last):
  File "<input>", line 1
__main__.FooError: Error (a='new_value')!
```

Format syntax is presented here:  
https://docs.python.org/3.7/library/string.html#format-string-syntax  
**Note:** Only keyword replacement fields are supported.  
**Note:** Additionally, there is an expression with the `=`. It allows you to set a value along with a name:
```python3
>>> error = FooError("{a}", a="a_value")
>>> print(error)
a_value
>>>
>>> error = FooError("{a=}", a="a_value")
>>> print(error)
a='a_value'
```

If a message template does not contain all replacement fields and all replacement fields is required, the `MissingFieldWarning` occurs:

```python3
>>> error = FooError("Error!", a="value")
<input>:1: MissingFieldWarning: No the replacement field 'a' in the template 'Error!' (FooError)!
>>>
>>> error = BarError("Error ({b=})!", b="value", c="value")
<input>:1: MissingFieldWarning: No the replacement field 'c' in the template 'Error ({b=})!' (BarError)!
>>>
>>> error = BarError("Error!", b="value", c="value")
<input>:1: MissingFieldWarning: No the replacement fields 'b', 'c' in the template 'Error!' (BarError)!
```

If for some reason you don't need to include all attributes in a message, define `ALL_REPLACEMENT_FIELDS_IS_REQUIRED = False` (default `True`) to disable checks and warnings:

```python3
>>> @dataclass
... class SomeError(Exception_):
...     ALL_REPLACEMENT_FIELDS_IS_REQUIRED = False
...     a: str
...     b: str
...
>>> error = SomeError("Error ({a=})!", a="a_value", b="b_value")
>>> raise error
Traceback (most recent call last):
  File "<input>", line 1
__main__.SomeError: Error (a='a_value')!
```

If a message template contains unknown replacement fields, the `UnknownFieldWarning` occurs and the value is set to `<UNKNOWN>`:

```python3
>>> error = FooError("Error ({a=}, {b=}, {c=})!", a="a_value")
<input>:1: UnknownFieldWarning: Unknown the replacement fields 'b', 'c' in the template 'Error ({a=}, {b=}, {c=})!' (FooError)!
>>> raise error
Traceback (most recent call last):
  File "<input>", line 1
__main__.FooError: Error (a='a_value', b=<UNKNOWN>, c=<UNKNOWN>)!
```

If there is no a message template and all replacement fields is required, the `MissingTemplateWarning` occurs:

```python3
>>> @dataclass
... class SomeError(Exception_):
...     pass
...
>>> error = SomeError(None)  # Message template is None
<input>:1: MissingTemplateWarning: No a template (SomeError)!
```

You can set a default message template:

```python3
>>> @dataclass
... class SomeError(Exception_):
...     DEFAULT_TEMPLATE = "Default message template ({a=})!"
...     a: str
...
>>> raise SomeError(None, a="a_value")  # Message template is None
Traceback (most recent call last):
  File "<input>", line 1
__main__.SomeError: Default message template (a='a_value')!
```
