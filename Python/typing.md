# Typing

## Type inference and annotations

By default, types are usually inferred (type inference), which means that:

```python
i = 1 # inferred type for i will be int
```

By using "annotations", its type can be set explicitly. This can be overridden with:

```python
i: Union[int, str] =  1 # explicit type: int or str
```

Note: Remember the duck compatibility of mypy, by which an int is "contained" inside
float. More compatibilites can be seen [here](https://mypy.readthedocs.io/en/stable/duck_type_compatibility.html)

Links: [Mypy documentation](https://mypy.readthedocs.io/en/stable/type_inference_and_annotations.html)

## Kind of types

Basic types are considered to be known (Union, List, int...). This section explains the
more complex ones.

`Callable(args type, return type)`: Tipycally for functions.

However, there is something with `Any` that needs to be clarified. `Any` tells the static
type checker not to check the type of that variable. As a better approach, we have
`object` type. This class contains all the other Python types, which means that, by
default, you will not be able to perform almost any type of operation with the object.
You will need to first apply narrowing type techniques (see below) before performen
any type of operation. Therefore:

- `Any`: Any object, not checked by static type checkers.
- `object`: Any object, checked by static type checkers.

### Literal and Final types

Used when the code acts differently when the value of a variable acquired a specific value.
For example, a function can be overridden to specify the type of value that it returns based
on not only the type of the input, but also its value:

```python
@overload
def fetch_data(raw: Literal[True]) -> bytes: ...
@overload
def fetch_data(raw: Literal[False]) -> str: ...
```

Literal can be a string, a number, any value.
If you need to specify the Union of a few values, it can be done with `Literal[3, 4]`. This means
that the variable would be either 3 or 4.
When declaring these variables, in order to avoid repeating all the time this syntax, you can do
this with the keyword `Final`:

```python
# These two lines are equivalent
c: Literal[19] = 19
c: Final = 19  # It means that c will take this as its only value (Literal[19])
```

Why is this also useful?

- Useful for defining constants that should not be reassigned, redefined or overridden in
  a subclass.
- This is really helpful for intelligent indexing. When indexing with these types, a
  variable that might contain different types (dictionary, set, tuple...) will return
  the exact type of it. If you use a non-Literal one, it will return the `Union` of
  all the elements present in that variable.

This can be also used to indicate that a method from a class should not be overridden
(althoug it is allowed for type hinting only) or that a class should not be subclassed.

```python
from typing import final

# For methods
class Base:
    @overload
    def method(self) -> None: ...
    @overload
    def method(self, arg: int) -> int: ...
    @final
    def common_name(self) -> None:

# For classes
@final
class Leaf:
    ...

class MyLeaf(Leaf):  # Error: Leaf can't be subclassed
```

### TypedDict

If each dictionary key is associated to a specific type, you can always use TypedDicts.

```python
from typing_extensions import TypedDict
Movie = TypedDict('Movie', {'name': str, 'year': int})
```

All of them will be required. If you need to mix required and non required, you can do this:

```python
class MovieBase(TypedDict):
    name: str
    year: int

class Movie(MovieBase, total=False):
    based_on: str
```


### Aliases

If the annotation gets so long, you can always use type annotations like this one:

```python
AliasType = Union[list[dict[tuple[int, str], set[int]]], tuple[str, list[str]]]

# Now we can use AliasType in place of the full name:

def f() -> AliasType:
    ...
```

Warning: This one does not create a type! It is just about notation, so be careful
when documenting.

### Tuples and Named tuples

Since tuples are static, you can hint over its size like `Tuple[str, ...]` for a
tuple of str that can be different lengths to `Tuple[str, str]` being a tuple of fized
size 2.
By default, tuples are inferred to be `Any`. If you want to specify types for each element,
you can use namedTuples:

```python
from typing import NamedTuple

class Point(NamedTuple):
    x: int
    y: int

p = Point(x=1, y='x')  # Argument has incompatible type "str"; expected "int"
```

### Classes

Its type can be used with `Type[C]` being `C` the name of the class or a subclass of `C`
or just the name of the class itself.

Class attribute annotations:

- Class variables: ClassVar[X]. Defined in the scope of the class, and all instances can
  access to it. Should not be modified from the instances of the object.
  This typing prevents it.
- Instance variables: Defined in `__init__()` method. Annotated as a normal variable. Each
  instance has its own instance variables.

```python
class Dog:

    kind = 'canine'         # class variable shared by all instances

    def __init__(self, name):
        self.name = name    # instance variable unique to each instance
```



## Stubs

Stubs are .fyi files that contain information relative to the input-output
types of all the functions belonging to a module. These can be generated
with mypy or stubgen. It can be generated by:

- Path: It will recursively search the path and generate the stub files.
- Reference to specific module: For example, the module B, located at A.B.
  However, it will also be necessary to build the previous one so that the
  type checkers can find the reference to B. In this case the previous one is A.
- Package: If I have A.B.C and I build he stubs for the package A, all
  the contained modules will be processed as well.


## Conflict between types at runtime vs at type checking

When running at runtime, types are checked in real time through the module.
However, type checkers use the information and types from the generated stubs.
Due to this, some classes might be defined as generic (`pd.Series`) but the type
checkers might require a type (`pd.Series[float]`). This last one will make the
Python script crash at runtime. How to solve this issue?

- From Python 3.7 to 3.10, use from __future__ import annotations
- Installed Python 3.11
- Use of `typing.TYPE_CHECKING`: By importing it, you can do an `if-else` statement
  based on this variable. TYPE\_CHECKING will be 1 when the type checkers run,
  and 0 during runtime. Knowing this, I can define two different types that will
  deal with this issue.
- Use of string literal types: These are not checked during runtime.
  It is literally writting the type annotation as a string. See [example](https://stackoverflow.com/questions/56218842/how-do-i-use-string-literal-type-annotations-for-multiple-possible-argument-type).

Links: [Mypy type checkers vs runtime](https://mypy.readthedocs.io/en/stable/runtime_troubles.html)

## Better definition of relationship between input-output types

There will be situations where, depending on the input type, the output type
will be completely different. For example, a function that creates a list
duplicating the input element (either str or float), it will be written like this:

```python
def duplicate(value: Union[float, str]) - Union[List[float], List[str]]:
```

However, to improve the type annotation, the @overload keyword can be used to
define a different behaviour of the function (or only different input-output types)
depending on the input type:

```python
from typing import overload

# Note: Overload methods MUST be above the non-overload method.
# These are ignored at runtime. Checked by the type checker.
@overload
def duplicate(value: float) -> List[float]: ...

@overload
def duplicate(value: str) -> List[str]: ...

# Contains runtime logic. It might or might not contain type hints
# However, mypy --strict will give an error if no type hints are defined
def duplicate(value):
    return [value, value]

```

See [Overlading and type hints in mypy](https://mypy.readthedocs.io/en/stable/more_types.html)
Three dots indicate that the content of this function is not modified.
However, what happens when I cannot modify the module?

See [Own question](https://stackoverflow.com/questions/70419778/incompatible-union-assignment-python)

Links:

- [Stack overflow question](https://stackoverflow.com/questions/48127642/incompatible-types-in-assignment-on-union)
- [Overload decorator](https://stackoverflow.com/questions/8654666/decorator-for-overloading-in-python)

## Narrowing types

This technique consists of going from a broader tpye to a specific one. For example, from Any to int.

- `isinstance()` like in `isinstance(obj, float)` will narrow `obj` to have `float` type.
   This can be used either with `if-else` or with `assert`.
- `issubclass()` like in `issubclass(cls, MyClass)` will narrow `cls` to be `Type[MyClass]`
- `type()` like in `type(obj)` is int will narrow `obj` to have `int` type
- `callable()` like in `callable(obj)` will narrow object to callable type

```python
def function(arg: object):
    if isinstance(arg, int):
        # Type is narrowed within the ``if`` branch only
        reveal_type(arg)  # Revealed type: "builtins.int"
    elif isinstance(arg, str) or isinstance(arg, bool):
        # Type is narrowed differently within this ``elif`` branch:
        reveal_type(arg)  # Revealed type: "builtins.str | builtins.bool"

        # Subsequent narrowing operations will narrow the type further
        if isinstance(arg, bool):
            reveal_type(arg)  # Revealed type: "builtins.bool"

    # Back outside of the ``if`` statement, the type isn't narrowed:
    reveal_type(arg)  # Revealed type: "builtins.object"
```

### TypeGuards

What happens when we need to verify more complex type such as `List[str]`?
You can either create a function that returns a boolean if this object is a list and all
its items are str, or you can implement a TypeGuard, which it is almost the same, and it
can be more human-readable.

```python
from typing import TypeGuard  # use `typing_extensions` for Python 3.9 and below

def is_str_list(val: list[object]) -> TypeGuard[list[str]]:
    """Determines whether all objects in the list are strings"""
    return all(isinstance(x, str) for x in val)

def func1(val: list[object]) -> None:
    if is_str_list(val):
        reveal_type(val)  # list[str]
        print(" ".join(val)) # ok
```

This example can be seen as `is_str_list` is narrowing from `List[object]` to `List[str]`.
Otherwise, with the boolean function we would not see this direct relationships.

### Narrowing TypedDicts 

If you want to narrow a Union of two TypedDicts into one, as you cannot do
`isinstance(var, TypeDict_name)`, it is recommended to add a tag in each one of them
(technique called `tagged unionsp`). Then, by checking the name of the tag in runtime,
you can perform the type narrowing

```python
from typing import Literal, TypedDict, Union

class NewJobEvent(TypedDict):
    tag: Literal["new-job"]
    job_name: str
    config_file_path: str

class CancelJobEvent(TypedDict):
    tag: Literal["cancel-job"]
    job_id: int

Event = Union[NewJobEvent, CancelJobEvent]

def process_event(event: Event) -> None:
    # Since we made sure both TypedDicts have a key named 'tag', it's
    # safe to do 'event["tag"]'. This expression normally has the type
    # Literal["new-job", "cancel-job"], but the check below will narrow
    # the type to either Literal["new-job"] or Literal["cancel-job"].
    #
    # This in turns narrows the type of 'event' to either NewJobEvent
    # or CancelJobEvent.
    if event["tag"] == "new-job":
        print(event["job_name"])
    else:
        print(event["job_id"])
```

Links:

- [Mypy documentation](https://mypy.readthedocs.io/en/stable/type_narrowing.html)