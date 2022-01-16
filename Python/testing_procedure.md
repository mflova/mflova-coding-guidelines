# Testing guidelines

## Test anatomy or structure

1. Arrange: (fixture) Set up the context in the fixtures
2. Act: (test) The test itself. Must contain the less. Behaviour we want to test.
3. Assert: (test)
4. Cleanup: Teardown sections

## Conftest.py

File used to stoe all the configuration that will be applied to the tests contained
in the same directory or subsequent folders.

## Parametrizing

Consists of changing the behaviour of a test or fixture based on other variables
or previously defined constants.

### Fixtures

Fixtures are predefined objects that can be initialized for each class, test... etc.
After being created, you can use them as argument to any function and these can be
freely used.

You can parametrize a fixture with a list of params. The fixture will be executed
once per each para defined in the list.

```python
@pytest.fixture(params = [a, b, c])
def fixture_example(request):
    request.param
```

If you want to conditionally parametrize a fixture from a test:

```python
@pytest.fixture
def fixt(request):
    marker = request.node.get_closest_marker("fixt_data")
    if marker is None:
        data = None
    else
        data = market.args[0]
    return data

@pytest.mark.fixt_data(42)
def test_example(fixt):
    assert fixt == 42
```

### Tests

In order to make cleaner tests, one possibility is to parametrize the input-output
relationship as follows. A test will be executed once per each parameter:

```python
@pytest.mark.parametrize("a, b, c", [(10,20, 31), (20,40,60), (11,22,33)])
def test_add(a, b, c):
    res = add(a, b)
    assert res == c
```

There are also marks to mark the test as expected to fail (xfail) if a given condition
is met. With the strict option set as True, the exitcode will be FAILED if this happens.
What's the difference then? Then the test will be not executed and directly checked as
failed if the condition is met.

```python
@pytest.mark.xfail(condition, reason="ROS core not launched", strict=True)
```

## Ensure teardowns are always executed

Fixtures with setup and teardown sections are always recommended to have a small setup
(and non dependent setup can be done in another fixture). This way, if the setup
produces a change in the state you can better ensure that the teardown is executed.

## Fixture scopes

It can be changed to execute the fixture once per class, test, session...

## Overriding fixtures

A fixture can be overridden to use the original wone but with some modifications. In
this case, the fixture `pyramid_request` is overridden inside the class
`TestUserSearchController`

```python
class TestUserSearchController(object):

    ...

    @pytest.fixture
    def pyramid_request(self, pyramid_request, user):
        pyramid_request.matchdict['username'] = user.username
        pyramid_request.authenticated_user = user
        return pyramid_request
```

## Yields

This can be used to set up a fixture, modify in a test, and execute a teardown
method with it if necessary. If there are no teardowns, a return is more than enough.

```python
@pytest.fixture()
def test_save():
    # Setup here of test_object
    yield test_object
    # Teardown here

test_function(test_object)
    # Modify here the test_object. It will be automatically sent to the teardown
    # after finishing with this test (if the scope is per each function)

```

## Asserting

### Assertion of expected exceptions

Done with:

```python
with pytest.raises(exception)
```

### Specify custom assertion messages

Done with:

```python
assert x == y, "Message"
```

### Pass arguments to fixtures

See parametrizing/fixtures (above)

### Parametrizing tests

See parametrizing/tests (above)

### Printing and displaying information

By using `pytest-info-collector`(needs to be installed), you can use a fixture to
always print a message regardless the status of the test.

## Mocking

Used when the output of a function we need to use for the setup is unpredictable. This
way we can directly force it to retrieve the values we want. Not only the return values,
but also its inner components (variables)


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

# Mre complex functions that we modify its inside
@mock.patch("myapp.sample.requests.get")
def test_get_ip(mock_request_get):
    mock_requests_get.return_value = mock.Mock(name"mock response", **{"status_code": 200, [...]})
    assert get_ip == "0.0.0.0"
```

Both examples are explained in this [full video](https://www.youtube.com/watch?v=dw2eNCzwBkk).


