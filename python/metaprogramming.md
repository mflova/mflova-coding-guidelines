# Metaprogramming

Metaprogramming is about creating code using code.

## Classes

As a reminder, `__new__` creates the instance of the class and it needs to take the
same arguments as `__init__`. Only when `__new__` returns the expected class `__init__`
will be called. Usually you can add new things and delegate the instance creation to
the super class.

```python
class MyClass:
    def __new__(cls):
        super().__new__(cls)
```

Although it cannot be seen, `__new__` is not bound to any instance, meaning that it is
a static method (`@staticmethod` has no effect).
When is it necessary to override it? Usually when we inherit from Python built-in type,
as a high amount of instantiation occurs here.


## Class creation

But what's the class that create the classes? These are called metaclasses. The built-in
one is `type`. Instances of `type` will be the same as when we do `class MyClass`,
meaning that classes are created by calling `type.__new__`. As a reminder, `type` is
not only use to check the type of an object. It can also be used to create new classes
by receiving three arguments:

    - Name of the class
    - Bases (from where it inherits)
    - Namespace (dictionary with all the methods and attributes at the class level).

However, we can create our own custom `type` to create classes in a different way and
provide them as `metaclass=MyType` when creating my custom class:

```python
class MyType(type):
    def __new__(mcls, name, bases, cls_dict):
        # Note: mcls is the metaclass, `MyType` in this case
        # tweak things
        # Note: You can use __prepare__ to start from a non empty `cls_dict`. By default,
        # if not overridden, this attribute returns an empty dict that will be filled
        # with all the methods and variables that will make the dictionary of the class
        # to be created.

        # create the class itself via delegation
        new_class = super().__new__(mcls, name, bases, cls_dict)

        # tweak some more

        # return the new class
        return new_class

class Person(metaclass=MyType):
    def __init__(self, name):
        self.name = name
```

This can be helpful to remove code duplications between different classes. It can be
seen as a common template to create new classes. However, although this is much more
flexible than inheritance, it is much more complex and not so easy to read.

## Alternatives

Most of the times, metaprograming techniques are applied as a way to initialize a class.
Let say, as an example, that you want to ensure that all methods within a class follow a
specific naming convention. Or that all methods are decorated with a given decorator.
Technically, these are done with metaclasses. However, in Python +3.6 a new approach was
implemented for these cases. This is called the `__init_subclass__` method. This one is
attached to a superclass and it will serve as a way to initialize any subclass deriving
from it. This way we can apply all those advantages but without using metaclasses.
Metclasses should avoided when possible, as they introduce complexity and problems: you
can only use one metaclass, harder to maintain and read... This was approved in
[PEP487](https://peps.python.org/pep-0487/). In this PEP, they write two examples: 1)
using `__init_subclass__` with an input parameter to customize the creation of our class
(see image) and 2) a superclass that keeps in a list the references to all of its
subclasses.


```python
class QuestBase:
   # this is implicitly a @classmethod (see below for motivation)
   def __init_subclass__(cls, swallow, **kwargs):
       cls.swallow = swallow
       super().__init_subclass__(**kwargs)

# Here we are customing our class creation in a very simple way
class Quest(QuestBase, swallow="african"):
   pass
```
