# Structural design patterns

These examples can be found [here](https://refactoring.guru/design-patterns/structural-patterns)

## Adapter

Implements a `Adapter` class that adapts the interface of our API to other API. Main classes:

- `Client interface`: Abstract class with a single method `method` that describes the
  that describes the input of our own data that will be converted. Then, derived
  classes will convert that data depending on the aimed API.input of our own data that
  will be converted. Then, derived classes will convert that data depending on the
  aimed API.
- `Adapter`: Subclass of client interface. This one implements the content of `method`
  so that it works with the aimed API.

## Bridge

Used to avoid the exponential increase in inheritance. For example, if we have:

```python
class Shape:
    pass

class Circle(Shape):
    pass

class Square(Shape):
    pass
```

And now we want to add them color, one first option could be to create `RedCircle` and
`BlueCircle`. However, with this you exponentially increase the classes. To solve it,
the `Bridge` connects these two entities.

The idea here, would be to define `Color` as a separate class and contain this one in
`Shape`.

## Composite

Useful when you need to execute an operation that needs to be recursively applied to
all the other objects in a tree hierarchical structure. For example, calculating the
price of all the objects belonging to the hierarchy. This hierarchiy might be a box,
composed of different small objects and boxes. Calculating its price might recursively
go to each object adding up all the values. You do not have to care about the concrete
classes that are below in the tree.

## Facade

It is about building a class that hides the inner implementation of the code. This can
be done by adding public methods that make use of these complex calls. For example,
converting a video involves many different conversion (audio, codec, video...). We can
create a higher level class that with a single method `convert` performs this in the
inside.

## Flyweight

Used when the class usually stores repeated data from a big database. For example, many names.
Instead of having an attribute of the class to save the name, this pattern stores the
possible name in the cache and then each instance of the class references the saved one.

## Proxy

Interface that works on top of another one, with the same function calls but with some extra-additions.
Different types:

- Protective Proxy: To add an extra protective layer.
- Logging Proxy: To add logging capabilities
- Virtual Proxy: Not loading an object in memoery until it is going to be used.
