# General

## Classes

About the instance vs class attributes:

- Class attributes: Defined at a class level (shared by all objects). When you modify
  them in an instance, this one will be looked up at a class level, and stored as an
  instance attribute of that object. See this [question/answer](https://stackoverflow.com/questions/63436006/why-can-i-change-class-attributes-for-an-instance-without-changing-the-class-val)
- Instance attributes: Assigned with the keyword `self`. Each instance will have its
  own values.

It is important to know that if there exists class and instance attributes with the
same name, Python will first look at the instance level. If there are not, it will go
to the class attribute.
To document these classes, I think it is recommended to use the keyword `attribute` for
both instance and class attributes.

## Decorators

Can be seen as wrappers of a class or functions to modify its behaviour. You can define
yours with:

```python
def split_string(function):
    def wrapper():
        func = function()
        splitted_string = func.split()
        return splitted_string

    return wrapper

@split_string
def say_hi():
    return 'hello there'
say_hi()
```

Performance and safety related:

- `@cache`: Performs automatic memoization (used to store previously calculated
  states in recursion, to avoid recalculating them.
- `@lru_cache`: Similar to `@cache` but you can indicate the maximum number of
  elements to store with `(maxsize=X)`
- `@register`: Executes a function at the end of the execution

### Decorators for data classes

Decorators for classes:

- `@dataclass`: Structures purely made to store data. It automatically implements
  methods as `__init__`, `__repr__` or other functions depending on the flags that are
  passed to this structure, as `Frozen = true` to make it hashable (for a dictionary).

```python
from dataclasses import dataclass

@dataclass
class T:
    n: int
    f: float
    s: str

    # Although it cannot be seen, the decorator will be creating a __init__ method of
    # type:
    # self.n = n (being n the first argument)
    # self.f = f (being n the second argument)
    # See conclusions at the end about the consequences of this.

x = T(42, 4.5, 'hello')
x = T(24, f=4.5, s='hello')
y = x.n
x.n = 0
```

- `@attr.s` or `@attrs.define`: More verbose than the previous one, but it also implements
  procedures to verify in runtime that the parameters passed to the class have the
  correct types (and much else). It also implements a `__repr__` method and other
  dunder methods.

  - Inside this same module, if we use `@frozen` instead, immutability of the
  attributes is guaranteed.

```python
import attr

@attr.s # or (@attrs.define)
class T:
    n: int = attr.ib(converter=int)
    f: float = attr.ib(validator=attr.validator.instance_of(float))
    s: str = attr.ib(default="")
    l: list = attr.ib(default_factory=list)

    # Although it cannot be seen, the decorator will be creating a __init__ method of
    # type:
    # self.n = n (being n the first argument)
    # self.f = f (being n the second argument)
    # See conclusions at the end about the consequences of this.

x = T(42, 4.5, 'hello')
x = T(42, f=4.5, s='hello')
y = x.n
x.n = 0
```

**Conclusions**: Therefore, although these attributes are defined at a class level, these
same variables will be defined per each instance with the keyword `self`, which means it
will be setting these attributes as instance attributes (reminder: since both are
defined, the instance attribute has more priority)

[More info about attrs here](https://www.attrs.org/en/stable/how-does-it-work.html)
and [examples here](https://www.attrs.org/en/stable/examples.html). Check
[validators!](https://www.attrs.org/en/stable/examples.html#validators) that can be
used for checking not only types but also values when creating the class.


Decorators for methods belonging to a class:

- `@classmethod`: To declare a method in the class as a class method. Can only access
  class attributes. The first parameter must be `cls`. Therefore, using
  `return cls(1,2)` will return an instantiate of the object where the parameters 1
  and 2 were sent to the `__init__` method. 
  [This link](https://www.attrs.org/en/stable/init.html?highlight=__init__) might be
  useful. You can see that the method `from_row` contains the necessary logic to build
  the class depending on the type of object sent. Thanks to it, it is not necessary to
  change the logic of __init__ every time we want to initialize and object in a
  different way (Remember that `@define` currently creates the `__init__` method).
- `@staticmethod`: Same as classmethod but do not have cls, so it cannot access any
  internal value of the class.
- `@property`: Methods from a class that return values and attributes. Cannot have
  parameters and they must be called after instantiation.
- `@abstractmethod`: Class with this decorator cannot be instantiated.


## Tips and tricks

- Remember that in Python, the for statement is implemented in C. This includes the
  comparison and the increment of the variable. The rest in Python. The while loop
  is implemented in C, but only the comparison. Therefore, use for loop whenever
  you can, as it is faster.
- Math module is much quicker. If I want to perform a repetitive action, the
  performance is for loop < numpy or builtin < math module.
- Use the method all to functions related to check all the elements from a structure
  without the need of a `for` loop. Example: `all(isinstance(x, str) for x in val)`
  returns a `True` if all elements returned are `True`.

## Mutable vs inmutable objects

Mutable objects can be modified in runtime. Immutable not:

- Immutable: int, float, bool, str, tuple and unicode.
- Mutable: list, set and dict.

**Caution:** When setting the default arguments of a function, remember that these are not
assigned every time the function is called, but when the function is defined. Due to
this, doing:

```python
# This will create a list "to" that will be shared among all the calls of the function. 
# Therefore, the first call to append_to will have no elements, but the second call
# will have the first that was appended in the first call
def append_to(element, to=[]):
    to.append(element)
    return to
```

To solve it, you can either use inmutable objects (although these are also defined once,
you are guaranteed that no other calls will modify the object) or defining these
default values in the body of the function:

```python
# If we define the default value of the object in the body, we will have one per
# each call.
def append_to(element, to=None):
    if to is None:
        to = []
    to.append(element)
    return to
```

However, this behaviour might be intended to perform some memoizaiton or other techniques.

## Performance

### Yield

Used to return a generator of an iterable object (such as list) to avoid loading the
entire list in memory at once. Since the list is not generated, only the first
iteration of the loop will be executed. Then, when those elements are needed (in
another for loop for example) they will be generated one by one. Used with long
lists or elements that are ideally inifnite.

```python
# This code executes once and it will stop when reaching the first yield. Then, each
iteration of the generator in another loop will continue the execution
def infinite_sequence():
    num = 0
    while True:
        yield num
        num += 1
```

You also have generator comprehensions:

```python
(item for item in my_list if item > 3)
```

### C-Python

Functions and modules can be implemented and optimized with C/C++. To do so, you have
some alternatives. These are ordered from quicker to slower (but more optimized)
implementations:

- `mypyc`: Module automatically and directly converted to C just by using the type hints.
- `Cython`: You have to write a setup module to compile the `.pyx` that you create. These
  are a mix between python and C. You can copy and paste your Python function there and
  the more static code you define, the more it will be converted to C/C++ (you can use
  `cython -a file.pyx`) to profile the proportion used between C and Python.
- `CPython`: Directly written in low C.

## Profiling

One package that includes a decorator (`@memprof`) for profiling the memory usage in
Python scripts for variables and functions:

[memprof repository](https://github.com/jmdana/memprof)
