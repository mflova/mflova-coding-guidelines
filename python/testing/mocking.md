# Mocking

Used in different scenarios:

- When testing depends on network-related functions
- When computation is so high
- When output is unpredictable (random behaviour)

This way we can directly force it to retrieve the values we want. These can be:

- Values returned from a function
- Global variables
- Environment variables
- Exception raised
- Classes and its attributes

Be aware that there are 2 different types:

- Mocking: Create an object with `mock` library.
- Stub: Same calls than the original object but less complex than a fake. Usually created
  as a separate class.
- Fake: Complex object and very functional. Usually created as a separate class.

## Theoretical concepts

Briefly, `mock` from `unittest` is Python built-in. There are tyipically two main
classes to create these mocked functions: `Mock` and `MagicMock`. The second one is the
same as second one but with some magic methods already implemented (underscore method
). Therefore, we have a main set of arguments that we can use:

```python
func = Mock() # Creates a callable function
func = Mock(return_value=2) # Callable function that returns 2
func = Mock(side_effect=aux) # Calls aux whenever the mock is called. It can be a function or exception
func = Mock(return_value=2) # Callable function that returns 2
```

Why would we want to use a function for side effect? It can be used to have a dynamic
`return_value`, since the return value of the functiona ttach in side effect will be
the returned value of the `Mock`. If we want to verify that the mock has been called to
verify that the pipeline flow is correct (imagine the scenario where we mock a really
deep function inside a deep and nested class/function), you can usethese methods from 
`Mock` (and of course `MagicMock`):

```python
func.assert_called()
func.assert_called_once()
func.assert_called_with()
func.assert_called_once_with()
```

This technique about verifying whether our objects was called and how, it is called "spy"
or "spying". If you want to create a whole class base objects and inspect any of its
attributes, you can use `wraps` flag, available in `mock.path` or `Mock`.

You can use `mock.patch` to substitute the behaviour of currently defined objects/classes/attributes...

```python
# Usable as decorator, class decorator or context manager
# Target can be a string representation of the import or the object already initialized
mock.patch(target, return_value=return_value, side_effec=side_effect)
mock.patch(target, return_value=return_value, side_effec=side_effect)
```

However, there are specific ways to mock specific objects. These are detailed below.

Important note: It is not recommended to use plain Mock() objects to replace an existing
one. If we do, Mock will dynamically "create" any attribute that our function to test
might access. Therefore, it is not realistic, as Mock will not raise an exception but
the real object might do it. To solve this issue, it is recommended using the keyword
argument "spec" that will create our mock object with same attributes as the object
to replicate. However, the function `create_autospec` implemnts a more in deep
replication. This same feature is available when doing `patch`. There is a keyword
only argument called `autospec` where we can use either `True` to have same
specifications as the object being replaced or we can pass another object. It also
admits the keyword argument `instance=True/False`. It indicates whether if it instantiates
an object or the class itself.

For more information read: https://blog.thea.codes/my-python-testing-style-guide/

### Mocking specific objects

#### Non-callable objects (variables, attributes)

```python
# Non callable versions (used to mock variables or non-callable objects)
func = NonCallableMock(args)
func = NonCallableMagicMock(args)
```

#### Dictionaries

Patch a dictionary, or dictionary like object, and restore the dictionary to its original state after the test.

```python
patch.dict(in_dict, values=(), clear=False, **kwargs)¶
```

#### Objects or multiple variables

You can use `patch.object` and `patch.multiple`. See more info in the documentation of mock (end of this readme)

## Practical concepts I learnt while programming

Note: Remember that, when setting the path to the object to patch, you must provide the
patch from where it is called, NOT where it is defined. If doubts, see
[this](https://medium.com/@durgaswaroop/writing-better-tests-in-python-with-pytest-mock-part-2-92b828e1453c)

```python
from unittest import mock
import pytest

from myapp.sample import guess_number, get_ip

# Simple example with only changing the return value
@mock.patch("myapp.sample.roll_dice")
def test_guess_number(mock_roll_dice, _input, expected):
    mock_roll_dice.return_value = 3
    assert guess_number(_input) == expected
    mock_roll_dice.assert_called_once()

# More complex functions that we modify its inside
@mock.patch("myapp.sample.requests.get")
def test_get_ip(mock_request_get):
    mock_requests_get.return_value = mock.Mock(name="mock response", **{"status_code": 200, [...]})
    assert get_ip == "0.0.0.0"
```

What possibilities do we have to implement these mocks?

- Decorators
- Context managers [(ref)](https://stackoverflow.com/questions/43941015/mocking-method-calls-in-python)
- Inline

Both examples are explained in this [full video](https://www.youtube.com/watch?v=dw2eNCzwBkk).

### Decorators more in detail

If I want to patch a function with all the content inside the decorator, I can do:

```python
@mock.patch("myapp.sample.roll_dice", return_value = 2)
```

If the function to patch belongs to a class (method) I will need to do:

```python
@mock.patch("myapp.sample.roll_dice", mock.MagicMock(return_value = 2))
```

## Refs

Main one: [Official](https://docs.python.org/3/library/unittest.mock.html)
