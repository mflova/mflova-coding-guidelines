# Descriptors

The descriptor protocol defines how an attribute is set, get or deleted. For this,
there are a few different approaches or alternatives:

- Using `__getattribute__`: This affects all attributes unlesss you start defining
  corner cases.
- Using `@property`. Implemented with descriptors. The problem is, if we want to apply
  a given code to a few attributes, we would need to create one property per attribute
  and duplicate the code.
- Using descriptors.

There are two types of desciptors:

- Non data-based: Only defines `__get__`
- Data-based: Can also define `__set__` and `__delete__`.

## Non data based descriptors

Following example will return a random number everytime we access `y` instance
attribute.

```python
# This is the descriptor
class RandomChoice:
    def __init__(self, *random)
        self._random = random

    def __get__(self, instance, instance_owner):
        if instance is None:
            return self
        return choice(self._random)

class A:
    x = 5                              # Regular class attribute
    y = RandomChoice(1, 2, 3)          # Descriptor instance
```

Be aware that the reference to the instance descriptor will be shared among all `A`
instances, as this is defined in the class scope.

`__get__` receives:
- `self`: Reference to the instance descriptor (same as any other class).
- `instance`: Reference to the instance that called the method. In case the descriptor
  was called from the class (i.e `A.y`) `instance` will be `None`. In this cases
  the `__get__` method usually returns `self`. This is done so that you can access all
  attributes of the descrptor from the class that contains it. FOr example by doing
  something like `MyClass.x.values`, being `x` an attribute from `MyClass` that was
  assigned a descriptor and `values` the dictionary in the descriptor instance that
  contains the values.
- `instance_owner`: Class that created `instance`. In this case it will be `A`.

## Data based descriptors

These also define the `__set__` method. This one receives:

`__set__(self, instance, value)`

Typically, this set method has a dictionary-based structure whose key is the instance
and the value is `value`. This is stored in the descriptor `__dict__` (i.e instance
attribute of the descriptor) as there are no guarantees that the class will have
a `__dict__`, as it might be using slots. However, there are a few considerations about
this. If we store it in a normal dictionary:

- This creates a strong reference to `instance`, meaning that the instance will not be
  release from the memory as this dictionary still has one reference to it.
- `instance` has to be hashable

For more info about weak vs strong references, see `general.md`

Then, how can a data descriptor be implemented without memory leaks and for classes that are not hashable?

```
class IntegerValue:
    def __init__(self):
        self.value = {}

    def __set__(self, instance, value):
        self.values[id(instance)] = (weakreaf.ref(instance, self._remove_object), int(value))

    def __get__(self, instance, owner_class):
        if instance is None:
            return self
        else:
            return self.values[id(instance)][1]

    def _remove_object(self, weak_ref):
        for key, value in self.values.items():
            if value[0] is weak_ref:
                del self.values[key]
                break
```

Keys of this implementation:
- Values stored in a normal dictionary, using the `id` of the instance as key -> All instance can be saved regardless if they are hashable or not.
- The value is a tuple of two elements:
  - Weak reference to the instance. If the instance has no longer any strong reference,
    this element will call its associated callback function (`self._remove_object`).
    This function will make sure that the key is removed from the dictionary.
  - The normal value to store.
- The callback function `_remove_object` called when it is necessary to remove an
  object from the dictionary of the descriptor that holds all the values. This performs
  a reverse lookup to remove the key in the dictionary given its value.

However, why it is not used this weak reference dictionary that will remove the objects
automatically? Because if we use it, the key has to be the instance of the object (not
its id). Because of this, the object has to be hashable, which is not always the case.

Important note: For this to work, if `instance` is slot-based class, this will have to
define `__weakref__` as a slot. `__dict__` creates it dynamically but not the slots.
Therefore:

```python
class MyClass:
    slots = ("__weakref__",)
```
