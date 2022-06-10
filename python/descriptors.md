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

Be aware that these descriptors are assigned in the class scope, meaning that these
cannot be found in the `__dict__` of the instance, but in the `__dict__` of the class:

```python
class MyClass:
    foo = MyDescriptor()
```

As a consequence, if we do `MyClass` a slot-based class, the descriptors will be still
stored in the class dictionary.
This means that all `foo` attributes from `MyClass` will be sharing the same instance
of `MyDescriptor`. Due to this, this descriptor will have to keep track in a
dictionary-like of all the instances changes so that they are not mixed.

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
- Values stored in a normal dictionary, using the `id` of the instance as key -> All
  instance can be saved regardless if they are hashable or not.
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

## Misc

### Set name

From Python 3.6, you can also define `__set_name__` to get the name of the property. This is:

```python
class MyClass:
    my_name = MyDescriptor()

class MyDescriptor:
    def __set_name__(self, owner, property_name):
        self.property_name = property_name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.property_name, None)

    def set(self, instance, value):
        instance.__dict__[self.property_name] = value
```

`self.property_name` will be equal to `my_name` string.
Why this is useful? Now this can be used to store the data in the dictionary of
the `MyClass` instance instead of the descriptor dictionary. Therefore, it is not
necessary that the class has to be hashable, but cannot be slot-based one then.
As examples, we can either store it in:

  - `instance.__dict__[self.property_name]`
  - `instance.__dict__[_ + self.property_name]`

Being `instance` an instance of `MyClass`.

### Property lookup resolution

Given the previous example, there are different ways a variable can be accessed when we
do `instance.my_name`. These are:

  - `__getattribute__` of the instance: It will look first in the dictionary of the
    instance and then in the one from the class if this is not available.
  - `__get__` of the descriptor: Since `my_name` was assigned to a descriptor, this
    one also defines its own `__get__` method which differs from `__getattribute__`.

This means that, if we have `my_name` attribute in both `__dict__` of the instance and
as a property (descriptor), what's the preference when accessing and writting it?
In order to solve these conflicts, the way these conflicts are solved for both
`__get__` and `__set__` is different depending on the descriptor protocol defined:

  - Non data based descriptor protocol: It will first look in `__dict__` of the
    instance. If this is not there, it will search if there's a defined
    descriptor/Property.
  - Data based descriptor protocol: It will look for a property with the name of the
    attribute. If there is one, it will use these `__get__` and `__set__` methods.
    Otherwise it will look in the `__dict__` of the instance.

As an example, `@property` decorator always creates both methods `__get__` and
`__set__` even if the setter is not defined. This is done to create a data descriptor
protocol whose methods have preference over the `__dict__` of the instance. Due to
this, `__set__` will always raise an exception unless the `setter` is defined. This
avoids that variables in `__dict__` instance shadow the properties with the same
name!

### Modifying instance attributes from the data descriptor

Now that the lookup resolution is clear, you have to be really careful when
implementing `__get__` and `__set__` methods. Why? Given the following code:

```python
class MyClass:
    my_name = MyDescriptor()

class MyDescriptor:
    def __set_name__(self, owner, property_name):
        self.property_name = property_name

    def __get__(self, instance, owner):
        value = getattr(instance, self.property_name)  # ERROR
        value = instance.__dict__[self.property_name]  # OK
        return value

    def __set__(self, instance, value):
        setattr(instance, self.property_name, value)   # ERROR
        instance.__dict__[self.property_name] = value  # OK

my_class = MyClass()
```

In this example of a data-based descriptor protocol, `my_name` is a property. Therefore,
when we do something `my_class.my_name` it will look first if there is a data
descriptor defined for this attribute before checking the `__dict__` of `my_class`.
Since there is one, it will go to the `__get__` method. If we use `getattr` of the
`instance` with name `self.property_name`, we will be calling again the `__get__`
method (since this is a property), creating an infinite recursion. Due to this, we need
to directly bypass this effect by directly accessing the `__dict__` of the instance
`my_class` and read/write data from there.

This happens because we store the values with the same name in `__dict__` of the
instance and as a property. For this example, we have `my_name` being stored in
`__dict__` but also with the same name as a property. Since this is data based
descriptor, when we do `my_class.my_name` or `getattr(instance, self.property_name)` it
will call the `__get__` method of the descriptor. This can be solved by modifying
`__set_name__` as:

```python
    def __set_name__(self, owner, property_name):
        self.property_name = "_" + property_name
```

This way we have two things: `my_name` as a property and `_my_name` as a key in the
instance `__dict__`. Therefore, when you do `getattr(instance, self.property_name)`
being `self.property_name = _my_name`, there is not any descriptor with this name,
meaning that will directly go to `__dict__` to avoid this infinite recursion.

### Accessing descriptor variables from the class that makes se of it

Imagine that we have some input arguments to the a descriptor that validates the data
type. In the code below, we assigned this to a `num`. After the execution, how can he
know in `MyClass` the type that `num` has associated? This can be done by
returning `self` in the `__get__` method when the attribute is retrieved from the class
and (`MyCLass`) not from the instance. Thanks to this, we can just do
`type(self).num.type_`. This is equivalent of doinf `MyCLass.num.type_`

```python
class MyClass:
    num = TypeValidator(int)

    def print_details(self):
        # How can we know the type that the TypeValidor that is using `num`?
        string = type(self).num.type_
        print(f"Type used {string}")

class TypeValidator:
    def __init__(self, type_: Type[object])
        self.type_ = type_

    def __set_name__(self, owner, property_name):
        self.property_name = property_name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = instance.__dict__[self.property_name]  # OK
        return value
```


### Easier implementations or less verbose ones

Although these have some advantages, they can be used in many cases. Last method is the
most recommended and used:

- Instead of the above implementation, you can just create a `WeakRefDictionary` being
  the key the instance and the value the value. The only problem is that the class has
  to be hashable. This means that `__hash__` has to be defined (by default this is the
  id of the instance in custom classes) and that `__eq__` operator has to be equal
  if `hash(a) == hash(b)`. For custom classes, by default, everything is ok. However,
  if we modify any of these methods, it might break.
- Using `__set_name__` in the descriptor to store the values in the `__dict__` of the
  instance that makes use of the attribute. Compatible with non-hashable classes but
  incompatible with slot based classes. See code snippet in `set name` section above.
