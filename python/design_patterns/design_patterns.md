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

## Template pattern

When you need to follow a specific metholodgy with some key-variants that need to be separately implemented.
Keypoints implementation:

- Abstract class: Methods represent each step of the methodology. Three types of methods:

  - `template_method` special method that defines the order of the steps. This is
    using all the functions defined in its own class in a specific order.
  - Other normal methods: Used to implement common steps that are always the same
  - Abstract methods: Used to implement steps that slightly change depending on some
    circumstances. These will be defined in the subclasses of this abstract class.
- Derived class: Implements ONLY abstract methods that were not defined in the abstract
  class, leaving the other ones untouched.

See example [here](https://refactoring.guru/design-patterns/template-method/python/example)

## Strategy pattern

Used when a method/function follows a different strategy depending on what it receives
as input argument. Note that an intermediate solution is to create separate methods
inside a class.
Instead of implementing if/else based on that input argument (drawback: you need
to edit the class all the time, dependendy issues, testing...), better implement an
abstract class `Strategy` for example and create the other strategies derivated from
this class. Then, use this one as input to my function. Variants:

- Create strategies as functions instead of classes to simplify the code. Drawback: if
  the strategies receive different arguments, all of them will need to implement
  `**kwargs`. You will need to check for the arguments at the start of every
  function associated to a strategy.
- Create strategies as classes (see below).
- Create strategies as classes. If input parameters to each strategy are different, you
  can instantiate the configuration as instantiate attributes and access them inside each
  strategy with self. To reduce the amount of code, you can instantiate them as
  `@dataclasses`. However, you will first need to instantiate the strategy outside of
  the class where it will be used and then pass the class as input argument as the
  previous example.

```python
def strategy(self, strategy: Strategy) -> None:
    strategy.do_algorithm()
    ...

class ConcreteStrategyA(Strategy):
    def do_algorithm(self, data: List) -> List:
        return sorted(data)

class ConcreteStrategyB(Strategy):
    def do_algorithm(self, data: List) -> List:
        return reversed(sorted(data))
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

Advantages: Flexibility. While in inheratance you have to create multiple abstract
class for each combination of classes, composition allows to create general and
separate blocks and then pass them as parameter to the classes that needed to cover
multiple cases without duplicating code.

## Proxy design

Used to provide greater abstraction of a class. For example, we can use a class to
instantiate its main behaviour and this wrapper to provide security layers, logging...
etc. Usually, by convention, the name of these wrappers is the name of the class but
prepending the word `Proxy`. Example:

```python

class IPerson(ABCMeta):

    @abstractmethod
    def person_method():
        """Interface method"""

class Person(IPerson):

    def person_method(self):
        print("I am a person")

class ProxyPerson(IPerson):

    def __init__(self):
        self.person = Person()

    def person_method(self):
        print("I am the proxy functionality")
        self.person.person_method()
```
