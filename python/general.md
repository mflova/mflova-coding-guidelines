# General

## Classes

About the instance vs class attributes:

- Class attributes: Defined at a class level (shared by all objects). When you modify
  them in an instance by mistake, an instance parameter with the same name will be
  created. If an attribute with the same name already exists (as class and instance
  attributes) the priority is always the instance attribute. See this
  [question/answer](https://stackoverflow.com/questions/63436006/why-can-i-change-class-attributes-for-an-instance-without-changing-the-class-val)
- Instance attributes: Assigned with the keyword `self`. Each instance will have its
  own values.

It is important to know that if there exists class and instance attributes with the
same name, Python will first look at the instance level. If there are not, it will go
to the class attribute.
To document these classes, I think it is recommended to use the keyword `attribute` for
both instance and class attributes.
As a useful tip, you can use `dir()` to inspect all the attributes within a class.

## Packing/Unpacking

In general, commas create tuples (`2, 3, 4` is an example). You can unpack these values
by assigning them in the left hand side (LHS) like `a, b = 3, 4`. In the RHS, you
create a tuple with two numbers, while in the LFHS you unpack them into these two values.
This happens in the foor loop while iterating iterable objects:

```python
for idx, value in enumerate(lst):
    ...
```

Here `enumerate` takes one by one each eelement from an iterable and creates a tuple
with the idx and value. Then, you unpack them with `idx, value`.
You can use `*args` to indicate "the rest" of the elements (ex: `a, *args = 1, 2, 3`)
in which a will be 1 and args a list of `[2, 3]`.
If you want to iterate element-wise between 2 or more iterables, you can pack the
values with `zip()`

```python
nums = [1,2,3]
letters = ['a', 'b', 'c']

# The zip will create: [(1,'a'), (2, 'b'), (3, 'c')] that you can then upack as below
for num, letter in zip(nums, letters):
    ...
```

### Using them in the arguments of a function

This can also be applied in functions:

```python
def my_func(a, *args):
    ...

my_func(1,2,3) # a = 1, args = (2,3)
```

The only difference is that args will be a tuple and not a list. You can use `*` to
exhaust the positional arguments:

```python
# Function that receives one positional argument (a) and one mandatory keyword argument
# (b).
def my_func(a, *, b):
    ...
```

### Using them when calling a function

Similarly:

```python
lst = [1,2,3]
my_func(*lst)  # Will call my_func(1,2,3)

dct = {"a": 2, "b":3}
my_func(**dct)  # Will call my_func(a=2, b=3)
```

As a general note, `*args` is related to lists-tuples (arguments with no keywords)
while `**kwargs` is related to dictionaries (keyword-related arguments)

## Scopes

Main keywords: `nonlocal` and `global`

```python
a = 2

# This functions does not modify the global variable a
def func():
    a = 3

# This function does modify the global variable a, as we are telling Python that a will
# be referencing the one from the global scope.
def func2():
    global a = 3
```

`nonlocal` is used when you need to search in a broeader scope but NOT in the global one.
For example:

```python

# Calling outer_func() will end up with a = 2
def outer_func():
    a = 2
    def inner_func():
        a = 3

# Calling outer_func() will end up with a = 3
# nonlocal tells that we are looking for variable a in a broader scope.
def outer_func():
    a = 2
    def inner_func():
        nonlocal a = 3
```

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

- `@cache`: Performs automatic memoization by storing the input arguments of a function
  and its output. Useful for recursion and functions with expensive IO operations or
  calculations. Important note below: in summary, use both only with functions and
  class/static methods. Not normal methods.
- `@lru_cache`: Similar to `@cache` but you can indicate the maximum number of
  elements to store with `(maxsize=X)`. Its variant `lfu_cache` keeps the most frequent
  calls in the cache, while `lru_cache` is based on a queue. Be aware that all keys
  must be hashable (99% immutables ), as they are stored in a dictionary. Be aware that
  this decorator creates a strogn reference to all the input arguments, meaning that it
  can cause memory leaks.
- `@functools.cached_property`: Creates a cached property where the property is
  computed once and then stored into `__dict__` as a normal instance attribute. If you
  want to re-calculate it, the only option is `del` the variable.
- `@register`: Executes a function at the end of the execution

Important note about cache-bsaed decorators: It is not recommended to use them with
methods. These decorators create a strong reference to all the input arguments. Among the
input arguments there is awlays a reference to the instance of a class (`self`).
Therefore, if this instance is removed, there will be references to this object, as the
decorator scope is global. Due to this, the garbage collector will not release the
memory associated to this object, resulting in memory leaks. The solution is to
implement a weak reference that allows to create cache container local to the class.

About the cache stored, you can clean it by executing `function_name.cache_clear()`.

### Decorators for data classes

Decorators for classes:

- `@dataclass`: Structures purely made to store data. It automatically implements
  methods as `__init__`, `__repr__` or other functions depending on the flags that are
  passed to this structure, as `Frozen = true` to make it hashable (for a dictionary).
  You can use the keyword `field` to pass more parameters to each variable. For example,
  to avoid a specific parameter to be part of the `__init__` method.

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
  class attributes. These are called instead from the object, from the class:

  ```python
  class Person:
    @classmethod
    def from_string():
        ...

  # Calling this method from the class instead of the instance
  Person.from_string()
  ```

  The first parameter must be `cls`. Therefore, using
  `return cls(1,2)` will return an instantiate of the object where the parameters 1
  and 2 were sent to the `__init__` method. Typycally used to create custom or optional
  initalizers of the object. For example, an object that can be isntanciated from an
  encoded string would be:

  ```python
  @classmethod
  def from_string(cls, str):
      # Logic to parse the string to the parameters retrieved by the __init__ method
      return cls(param1, param2...) # This returns the object created from
                                    # the from_string method
  ```

  [This link](https://www.attrs.org/en/stable/init.html?highlight=__init__) might be
  useful. You can see that the method `from_row` contains the necessary logic to build
  the class depending on the type of object sent. Thanks to it, it is not necessary to
  change the logic of __init__ every time we want to initialize and object in a
  different way (Remember that `@define` currently creates the `__init__` method).
- `@staticmethod`: Same as `classmethod` but do not have cls, so it cannot access any
  internal value of the class.
- `@property`: Methods from a class that return values and attributes. Cannot have
  parameters and they must be called after instantiation. Typically used when a
  parameter is calculated from instance attributes, to avoid re-updating this property,
  this getter will calculate the value whenever is requested. So no need to update the
  property once its dependent value changes.
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
- Instead of installing a package with `pip3 install .`, add the flag `-e` from
  editable so that every time you modify the Python code you do not have to reinstall
  the package.

## Python Memory Management

As a note, you can check the memoery addres with `id()`

Variables are always pointers to the address of an object. Everything in Python is
pointing an object so all values are passed by reference. When the reference counter of
an object is zero, the object is released from memory. When you do `a = 2`, since ints
are immutable objects (you cannot change its internal state), if you follow with
`a = a + 2` you will create a new `int` object with value `a + 2` and now `a` will be
pointing to this one. However, for mutable objects like `lists`, when you `.append` and
object, you are directly modidfying the interla state of the list (same memory address
but different content). But when you do something like `lst = lst + ['a']`, you will be
creating again a new object and assigning `lst` the new address of that object. In
Python, whenever there is an assignment (`=`), the right side is first evaluated and
then the left side. When I do:

```python
lst = [1,2,3]
lst2 = lst
```

Any change on the list (either from `lst2` or `lst`) will produce changes in the
content of the list, since both are pointing at the same variable and this variable can
be mutable. If you have a `Tuple` (immutable) of `Lists` (mutable) the memory address
of the tuple is not going to change. But each element of the tuple is a variable that
is pointing to a lists, and the content of this can change, so be careful with it.
Knowing this, you have to take into account the two main operators when comparing objects:

- `is`: Checks that two objects point to the same address. Since `None` object is a
  singleton, that's why you use it with `None`, as all variables that were assigned to
  it will point to the same direction.
- `=`: Checks the CONTENT of the variable. Nothing to do with the memory address.

### Interning

Some `int` and `str` are pre-cached in the memory to otpimize access times. This is
done for the range [-5, 256] for the int or any snake case string (lower case with
underscore) as these are typically use as dictionary keys. What does it mean? That
these are singletons. All variables pointing this values will be pointing the same
address. Due to this, it is faster to compare them with `is` rather than `==`. For
example, in a string, you need to compare char by char. However, if you know that that
string is a singleton, you can just compare if two variables are pointing the same
memory address, regardless the number of chars.

### Storing constants

Some variables (such as `40 * 60` or `if var == [1, 2, 3]`) are stored as constants to
access them faster. In case of the list, this is stored as its equivalent immutable
object (`tuple`). For the `set`, there is the `frozenset`.

### Garbage collector

Those objects that are not pointed by any of the variables will call the `__del__`
method to release them from memory. This is done in a few cycles, so it is not
instantaneous.
More complex case:

```python
lst = []
lst.append(1)
a = [0, 1, 2]
lst.append(a)
lst = None
```
In this case, `lst` will be released from memory despite the presence of a pointer to
`a`. At the end, `lst` is not more than a list of stored pointers, so it is safe for
the garbage collector to remove it.

### Weak vs strong references

Gaarbage collector will collect those objects whose strong references count is 0. If
this object has weak references pointer to it, they will be deleted as well. These are used to avoid memory leaks. You can create a new weakref as:

```
weakref.ref(object)
```

In case you need to store this object as a key in a dictionary, being this one a weak reference, this `weakref` module also implements a special dictionary for it:

```
dct = WeakKeyDictionary()
dct[object] = value
```

If all strong references to `ibject` are removed, this key will be removed as well, as
this is a weak reference.

## Mutable vs inmutable objects

Mutable objects can be modified in runtime. Immutable not:

- Immutable: int, float, bool, str, tuple and unicode, views.
- Mutable: list, set and dict.

**Caution:** When setting the default arguments of a function, remember that these are not
assigned every time the function is called, but when the function is defined (module imported). Due to
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
More cases as an example:

```python
# to_append takes the memory address of list and changes its internal state to add the
# int 4 element. Therefore, whenever it is called it adds one more.
def to_append(lst = [1,2,3]):
    lst.append(4)
    print(lst)
to_append()  # [1, 2, 3, 4]
to_append()  # [1, 2, 3, 4, 4]


# Here, in contrast, does not happen. lst + [4] creates a NEW object in another memory
# address, and then lst (the left hand side) is pointing to this new memory address.
def to_append(lst = [1,2,3]):
    lst = lst + [4]
    print(lst)
to_append()  # [1, 2, 3, 4]
to_append()  # [1, 2, 3, 4]
```

For all these cases, it would be the same if you create a list and send that memory
address as input argument to the `to_append()` function.

For the `views` (keys, values of a dictionary), these are dynamic references to the
key/values of a dictionary. They behave as a set, meaning that all set operations can
be performed. Exception: values view when values are repeated.

### Immutable alternatives

For `Set`, you can use `FrozenSet` for its equivalent immutable object. For `Dict` you
can use `MappingProxyType`, which is a proxy (wrapper) around the dict implementation
to remove its writting methods. However, take into account that this works as a `view`
item (immutable dynamic reference to the original dictionary). Therefore, if we modify
the original dictionary the `MappingProxyType` will also be changed.

## Copies

Two main approaches when coppying an object:

- Shallow copy: It only copies the 1st level of an object.
- Deep copy: It will copy ALL levels of an object. For example if different lists are
  nested inside a list, it will also copy them.

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

### Slots

Instead of storing the instance attributes in a mutable dictionary, you can chooose to
store them in a more opzimied memory that avoids hashing and indexing the dictionary.

- It is about 20% faster
- Multiple inheritance with both slot-based classes throws an error. Atributes cannot
  be defined dynamically.

Example:

```python
# For normal classes
class MyClass:

    __slots__ = ["a", "b"]
    def __init__(self, a, b) -> None:
        self.a = a
        self.b = b

# For dataclasses
@dataclass(slots=True)
class MyClass
    a: int
    b: int
```

If I subclass from `MyClass` I only need to define the new slots that will be included. `Python` will take the other ones from the super classes as well.

### Abstract classes

Just as a reminder, you can create them with:

```python
from abc import ABC, abstractmethod
 
class Polygon(ABC):
 
    @abstractmethod
    def noofsides(self):
        """Description.""" # You can also use the keyword pass, but test coverage APIs
                          # will always say that this statement is never reached.
 
class Triangle(Polygon):
 
    # overriding abstract method
    def noofsides(self):
        print("I have 3 sides")
 
class Pentagon(Polygon):
 
    # overriding abstract method
    def noofsides(self):
        print("I have 5 sides")
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

## Closures and decorators

What's its use? They are used to create parametrized functions whose parameters go
beyond the scope of the function. Imagine a function whose behaviours depend on a
global variable.

Closure is just a function that references a free variable (a.k.a non local variable).
This free variable has memory outside of the scope.
Example:

```python
def outer():
    count = 0
    def inner():
        nonlocal count
        count = count + 1
        print(count)
        return count
    return inner
```

In this case, calling `outer()` will return the closure (which is the function `inner`
and this `count` variable). Then:

```python
func = outer()
func()  # 1
func()  # 2
```

When you call `outer`, a `Cell` is created, which means that the `count` from `inner`
and the `counter` from `outer` are pointing the same varible.
If the outer functions receives a function, this is a decorator.

```python
def outer(func):
    # args and kwargs to read all possible arguments from the function
    def inner(*args, **kwargs):
        inner.calls += 1
        print(inner.calls)
        return func(*args, **kwargs)
    inner.calls = 0
    return helper
```

A free variable can be instantiated in the outer function. This one would have its own
value (persistent memory) per each function.
As a tip: 2 nested functions means that you will need to call the outer function twice
to get the desired effect. In this case, calling `call_counter(my_func)` will create a
similar version of `my_func` but substituted by `inner`. Due to this substitution, all
the metadata form my original function will be also substituted by the `inner` one. Use
the `@wraps(func)` decorator over `inner` to avoid this.

Decorators with arguments will need one more outer func. This one is also called
factory decorator, as it is in charge of creating new decorators based on my input
arguments. In the example below, calling `decorator_factory(X)` with my arguments, will
return a decorator that can be used as the above code blocks.

```python
def decorator_factory(argument):
    def decorator(function):
        def wrapper(*args, **kwargs):
            funny_stuff()
            something_with_argument(argument)
            result = function(*args, **kwargs)
            more_funny_stuff()
            return result
        return wrapper
    return decorator

# Ex (total of 3 calls):
my_decorator = decorator_factory(X)
wrapped_func = my_decorator(func)
wrapped_func()
```

Important note: Be careful because cmprehensions and lambda functions might create a
closure with free variables and it is not so easy to see.

## Single dispatch (pseudo function overload)

As an example, in the following code the function `fun` defines a default behaviour.
Then, with `@fun.regier(type)` you define specific behaviours. The function name can be
anything.

```python
from functools import singledispatch

@singledispatch
def fun(s):
        print(s)

@fun.register(int)
def _(s):
        print(s * 2)

@fun.register(list)
def _(s):
        for i, e in enumerate(s):print(i, e)

fun('GeeksforGeeks')
fun(10)
fun(['g', 'e', 'e', 'k', 's'])
```

## Iterables and Context Managers

In order to do an iterable class, this must implement the `__iter__` method. This
usually returns the `self` object. However, once this one is iterated till the end,
there is no way to reset it. The solution is usually creating separate class that
handle this. Then, in our `__iter__` class of the class to be iterable, we just return
a new object of iterator class.

```python
class MyClassIterator:
    def __init__(self, object: MyClass):
        ...

    def __next__():
        # Return elements index by index
        # Raise StopIteration if reach the end

class MyClass:
    def __iter__(self):
        return MyClassIterator(self)
```

If we want to make our class iterable, the other option is to have the method
`__getitem__` implemented. Python first looks at `__iter__`. If this is not defined, it
will look at `__getitem__`. If not, it will raise an exception saying the class is not
iterable. Remember that iterators can be exhausted while iterables not.

### Itertools

Module that provides tools to better iterate:

- `islice()`:  To do slicing over an iterator (for example, slicing a generator). There
  is not magic inside. It will call `next()` until it gets the values of interest.
  Output is lazy, which means that they are loaded on demand.
- `chain`: Used to "flatten" nested structures. It has `from_iterable()` method to
  flatten nested iterables.

### Context Managers

Quick notes:

- You can return  `True` or `False` in `__exit__` to ignore or not any exception
- The `@contextmanager` decorator allows you to create a contexst manager from a
  function. This allows you to do so without the previous creation of any class with
  the `__enter__` and `__exit__` methods.

## Hash, dicts

### Ordered dict

From Python 3.6 dicts are ordered by default. However, this class `OrderedDict` offers
a few extra advantages. The main one is that you can pop first and last items from the
dictionary. This means that it can work as a `queue` (`dequeue` object in Python).
However, be aware that it is much slower. The advantage of using this one is that
checking if an object is in the container is much quicker for `OrderedDict` than
in `dequeue`. Why? Because the queue needs to iterate over all its elements.
The `OrderedDict` just needs to perform a single lookup.

### Counter

Dictionary-type that keep tracks of the count of different elementso.

### UserDict

Class intended to be used as super class of user-defined dictionaries. Recommended to
do it from this one and not from `dict` as this one guarantees that the dunder methods
are correctly called if I override them.

### Serializing and deserializing

Pickling is a way of serializing, but be aware that it executed code snippets, so only use it with safe files.
You can also use `JSON` or `PyYaml`:

- `JSON`: You can define your own `default` serializer, that serialized unknown data
  types in the way you want to.
- `PyYaml`: Use `safe_dump` to avoid executing code. However, this will prevent
  `Python` to save custom classes. For this, you can create "safe" classes like this:
```python
class User(yaml.YAMLObject):
    yaml_loader = yaml.SafeLoader  # Mark it as safe 
    yaml_tag = u'!User'  # Add a tag to be used to identify the class in the .yaml file

    def __init__(self, name, surname):
       self.name= name
       self.surname= surname
```

#### Extra tools

- `JsonSchema` to validate `JSON` files (like types, range of an integer and so on).
- `Matshmallow` to define schemas that define how different custom classes must be
  converted into simpler types that can be serialized and deserialized

## Enums

For enums, take into account that any method defined in the class scope will act as a
bound-method (as any other method inside a class). The difference is that each enum you
defined is an instance of the enum. In the example below, `Foo.FOO1` and `Foo.FOO2` are
instances of `Foo`. Meaning that doing `Foo.FOO1.func()` will be a bound method
being `self` this same instance.

```python
class Foo(Enum):  
    # you could comma separate any combination for a given state
    FOO1 = "foo1"   
    FOO2 = "foo2"

    def func(self):
        print("This is my func")
```
