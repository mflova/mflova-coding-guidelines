# Testing

## Fixtures

Fixtures are predefined objects that can be initialized for each class, test... etc.
After being created, you can use them as argument to any function and these can be
freely used.

## Conftest.py

File used to stoe all the configuration that will be applied to the tests contained
in the same directory or subsequent folders.

## Parametrrizing tests

In order to make cleaner tests, one possibility is to parametrize the input-output
relationship as follows:

```python
@pytest.mark.parametrize("a, b, c", [(10,20, 31), (20,40,60), (11,22,33)])
def test_add(a, b, c):
    res = add(a, b)
    assert res == c
```

## Overriding fixtures

A fixture can be overriden to use the original wone but with some modifications. In
this case, the fixture `pyramid_request` is overriden inside the class
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

This can be used to set up a fixture, modifiy in a test, and execute a teardown
method with it if necessary. If there are no teardown, a return is more than enough.

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
