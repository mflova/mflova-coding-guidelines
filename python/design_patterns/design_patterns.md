# Design patterns

Note that in general, code should follow SOLID principles:

- Single responsibility principle: Avoiding complex classes with many different
  purposes or responsibilities.
- Open-closed principle: Code opened to extension but the already implemented one
  closed for modifications.
- Liskov substitution principle: Functions that use pointers or references to base
  classes must be able to use objects of derived classes without knowing it
- Interface segregation principle: Many different interfaces preferred over single big
  interface.
- Dependency inversion principle: Depend upon abstractions, not concrete classes.
  (Explained below)

Good reference to all patterns [here](https://refactoring.guru/design-patterns/python)

## Dependency injection

Consists of isolating the creation of an object and its use. When you create a class B
inside A, this makes it harder to test and debug. As any change in B will also change A.
This pattern usually requires to create the instance of B outside of A, and pass it as
input parameter to A to the function that actually uses or needs it. It allows to create
simpler functions to test that do not depend on this class.

## Dependency inversion

Summary: Make the code depends on abstract classes and not concrete classes.
It adds one more layer of abstraction between the creation of the class and its use. In
this pattern, the class that is passed as argument is an abstract one that includes the
sub-class I want to pass. This way, I can create different classes and respect the
modularity. Example: A class `Car` that can take different `Engines`. It is better to,
instead of having:

```python
class Car:
    def install_engine(engine: Union[MotorA, MotorB]):
        if isinstance(engine, MotorA):
            ...
        else:
            ...
```

Is better to define an abstract class Engine, with a given set of common methods and
attributes, and then:

```python
class Car:
    def install_engine(engine: Engine):
        ...
```
