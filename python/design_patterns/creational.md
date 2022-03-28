# Creational design patterns

Allows to instantiate complex objects.

## Builder

Allows you to build in a piecewise way.

```python
class Person:
    pass

class PersonBuilder:
    def __init__(self) -> None:
        self._person = Person()

    def add_address(self, address):
        self._person.address = address
        return self

    def add_age(self, age):
        self._person.age = age
        return self

    @property
    def person(self):
        return self._person

person_builder = PersonBuilder()
person_builder.add_address("A").add_age(12)
person = person_builder.person
```

Returning the self instance is not mandatory, but it is useful to create fluent
interfaces. This is the fact you can concatenate multiple methods from the builder, as
it can be seen in the last line of the code snippet.

## Factories

They instantiate the entire object at once (not piecewise like builder)

### Factory method

All logic implemented in a method o function

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def from_polar_coordinates(cls, radius, theta):
        # Maps radius and theta to x and y 
        return cls(x, y)
```

### Factory class

If we have too many of these methods, we can just group them into a class.

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class PointFactory:
    @staticmethod
    def from_polar_coordinates(radius, theta):
        # Maps radius and theta to x and y 
        return Point(x, y)
```

#### Abstract factory

What happens if the class to create has its own hierarchy (abstract class, derived
classes)...? We can just replicate the same hierarchy but by adding `Factory` at the
end of the class.

## Prottotype

Prototypes are tipically partially initialized objects that can be used as a starting
point to build an object. Due to its nature, they are typically implemented with the
factory pattern.

```python
@dataclass
class Address:
    street: str
    suite: int
    country: str

@dataclass
class Employee:
    name: str
    address: Address

class EmployeeFactory:
    main_office_employee = Employee("", Address("123 East Dr", 0, "London"))
    aux_office_employee = Employee("", Address("123B East Dr", 0, "London"))

    @staticmethod
    def __new_employee(proto, name, suite):
        result = copy.deepcopy(proto)
        result.name = name
        result.address.suite = suite

    @classmethod
    def new_main_office_employee(cls, name, suite):
        return cls.__new_employee(cls.main_office_employee, name, suite)

    @classmethod
    def new_aux_office_employee(cls, name, suite):
        return cls.__new_employee(cls.aux_office_employee, name, suite)
```

In this example, we defined different prototypes with pre-defined values and some empty
fields. Then, these empty fields can be re-assigned later. Take into account that the
`deepcopy` is used to avoid all objects created from pointing the same memory address.
