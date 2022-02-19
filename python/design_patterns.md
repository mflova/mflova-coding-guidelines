# Design patterns

For the dependency inversion and injection, you can use [this link](https://www.youtube.com/watch?v=2ejbLVkCndI). Current categories I know:

## Dependency injection

Consists of isolating the creation of an object and its use. When you create a class B
inside A, this makes it harder to test and debug. As any change in B will also change A.
This pattern usually requires to create the instance of B outside of A, and pass it as
input parameter to A to the function that actually uses or needs it. It allows to create
simpler functions to test that do not depend on this class.

## Dependency inversion

Add one more layer of abstraction between the creation of the class and its use. In
this pattern, the class that is passed as argument is an abstract one that includes the
sub-class I want to pass. Ths way, I can create different classes and respect the
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

## Singleton pattern

Made to create one unique instance of a class by modifying the init method to return
the same object. However, these seems to be not recommending, as they break OOP
paradigm and testing is harder.

## Composite pattern

Used to establish a modular multi-level hierarchy of classes. The idea is that each
level has a main class that groups the behaviour of the current level and acts as a
container for these. For example:

- `class IDepartment` (main abstract class)

    - `class ParentDepartment(IDepartment)`: Apart from the abstract methods, it has
      generic methods to retrieve different data such as a list with the current
      departments added (such as `Accounting` or `Development` instances) or for
      example, in this case, the total number of employees by taking into account this
      list.
    - `class Accounting(IDeparment)`
    - `class Development(IDepartment)`

## Proxy design

Used to provide greater abstraction of a class. For example, we can use a class to
instanciate its main behaviour and this wrapper to provide security layers, logging...
etc. Usually, by convention, the name of these wrappers is the name of the class but
prepending the word `Proxy`
