# Testing

## Fixtures

Fixtures are predefined objects that can be initialized for each class, test... etc.
After being created, you can use them as argument to any function and these can be
freely used.

## Conftest.py

File used to stoe all the configuration that will be applied to the tests contained
in the same directory or subsequent folders.

## Yields

This can be used to set up a fixture, modifiy in a test, and execute a teardown
method with it if necessary.

```
@pytest.fixture()
def test_save():
    # Setup here of test_object
    yield test_object
    # Teardown here

test_function(test_object)
    # Modify here the test_object. It will be automatically sent to the teardown
    # after finishing with this test (if the scope is per each function)

```
