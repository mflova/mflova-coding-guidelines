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
