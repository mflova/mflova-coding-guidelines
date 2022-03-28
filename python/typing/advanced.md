# Advanced

## typing.type_check_only

Decorator to indicate that a class or function is not available on runtime.

## typing.Annotated

To define types with fixed-context through metadata. For example

```python
T1 = Annotated[int, ValueRange(10,5)]
```

Compatible with runtime checks, but added in Python 3.9.

## typing.NoReturn

For functions that does not return anything (i.e always raised exceptions)

## typing.NewType

To create a new type derived from a already defined type. This can be, for example, from an `int`:

```python
UserId = NewType(`UserId`, int)
some_id = UserId(524313) # Used same as int()
```

## typing.TypeVar and typing.Generic

TypeVar is used to create "templated" (concept from C++) classes or functions by:

- Being used in function signature

```python
T = Typevar('T') # Can be anything
A = Typevar('A', str, bytes) # Must be str or bytes

def repeat (x: T, n: int) -> Sequence[T]:
    return [x]*n

def longest (x: A,  y:A) -> A:
    return x if len(x) >= len(y) else y
```

- Being used as input parameter to Generic

```Python
T = TypeVar('T')

class LoggedVar(Generic[T]):
    def __init__(self, value: T, name: str, logger: Logger) -> None:
        self.name = name
        self.logger = logger
        self.value = value
```

In these examples, the `TypeVar` can be any variable, but you can limit it with:

```python
T = TypeVar('T', float, int)  # Either float or int
T = TypeVar('T', upper_bound=XXX)
```

An upper bound means that, supposing that we have a few class derived such as:
`object -> AbstractA -> A -> B` an upper bound of A would mean that the variable can be
either A or B. You can also select if the variable is covariant, contravariant or
invariant. See [this link](https://stackoverflow.com/questions/61568462/python-typing-what-does-typevara-b-covariant-true-mean)

There are some predefined `TypeVar` that can be imported from the `typing` module:

```python
# Some unconstrained type variables. These are used by the container types.
# (These are not for export.)
T = TypeVar('T')  # Any type.
KT = TypeVar('KT')  # Key type.
VT = TypeVar('VT')  # Value type.
T_co = TypeVar('T_co', covariant=True)  # Any type covariant containers.
V_co = TypeVar('V_co', covariant=True)  # Any type covariant containers.
VT_co = TypeVar('VT_co', covariant=True)  # Value type covariant containers.
T_contra = TypeVar('T_contra', contravariant=True)  # Ditto contravariant.
# Internal type variable used for Type[].
CT_co = TypeVar('CT_co', covariant=True, bound=type)

# A useful type variable with constraints. This represents string types.
# (This one is for export!)
AnyStr = TypeVar('AnyStr', bytes, str)
```

## typing.Protocol

To hint classes that MUST have a given structure (instance attributes, methods...). In
the example below we say that the input parameter to `func` must have the method `meth`

```python
class Proto(Protocol):
    def meth(self) -> int:
        ...

class C:
    def meth(self) -> int:
        return 0

def func(x: Proto) -> int:
    return x.meth()

func(C())  # Passes static type check
```

It can be also used as an improved version of `Callable`. `Callable` just define
something minimal, so most of the metadata of the function is lost (keyword names,
docstring...). This metadata helps when developping code and also helps the LSP
features and autocomplete from the IDE. In addition, with `Protocol` you can define
default arguments, such in this example `y`. In `Callable` you cannot.`python`

```python
class Foo(Protocol):
    def __call__(self, x: int, y: Optional[float] = None) -> float:
        """Docstring"""
```

If `self` is not necessary, just tag the method as `@staticmethod`. You can use
@runtime_checkable from `typing/typing_extensions` so that you can check the protocol
in runtime with `isinstance(variable, my_protocol)`. Take into account that this one
does not check the signature of the methods.

## Decorators

One common application of type variable upper bounds is in declaring a decorator that
preserves the signature of the function it decorates, regardless of that signature.

```python
from typing import Any, Callable, TypeVar, cast

F = TypeVar('F', bound=Callable[..., Any])

# A decorator that preserves the signature.
def my_decorator(func: F) -> F:
    def wrapper(*args, **kwds):
        print("Calling", func)
        return func(*args, **kwds)
    return cast(F, wrapper)

# A decorated function.
@my_decorator
def foo(a: int) -> str:
    return str(a)

a = foo(12)
reveal_type(a)  # str
foo('x')    # Type check error: incompatible type "str"; expected "int"
```

More info about decorators in [Mypy docs](https://mypy.readthedocs.io/en/stable/generics.html#declaring-decorators)

## Inheritances

### Overriding types in methods

Remember that, when creating a class from a base one, the arguments tends to be
contarvariant while the return type is covariant.
For example, code below is ok because the return type of func (in B) is subtype of
`float`, while the argument is a supertype.
Doing `val: int` in `B`, mypy raises an error saying that the liskov principle is
violated.

```python
class A(ABC):

    @abstractmethod
    def func(self, val: float) -> float:
        pass

class B(A):
    def func(self, val: object) -> int:
        return 2

```
WARNING: However, this does not happen in normal functions. If you expect to receive a
float, you cannot pass an object. The code above is ONLY for overriding methods and
abstract methods.

### Overriding instance attributes

It can be done by means of `Generic`. Example [here](https://stackoverflow.com/questions/58089300/python-how-to-override-type-hint-on-an-instance-attribute-in-a-subclass)
Another solution (also in that URL) is to manually override in the class scope.
