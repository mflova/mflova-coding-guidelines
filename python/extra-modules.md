# Extra-modules

## pyfakefs

[Link](https://github.com/jmcgeheeiv/pyfakefs)

Install with `pip install pyfakefs`

It simplifies a lot faking a filesystem, created by Google. You can easily create files,
folders or links with the desired content just by doing fs.create_file("/pc/file.txt",
content="This is a faked file"). You can also set the privileges, size of the faked
filesystem, size of the file... It works by mocking all the IO-based Python built-in
modules to trick them into this fake filesystem, so you can "create" any file you want
in any path you want. The, by using modules such as os or shutil  you can open, edit
them, remove them...

## pytest-cov

[Link](https://github.com/pytest-dev/pytest-cov)

Install with `pip install pytest-cov`

Generate reports based on the test coverage.

## pytest-xdist

[Link](https://github.com/pytest-dev/pytest-xdist)

Install with `pip install pytest-xdist`

Run tests in parallel with `pytest -nauto [...]`

## hypothesis-auto

[Link](https://github.com/timothycrosley/hypothesis-auto)

Install with `pip install hypothesis-auto`

In a single function call, it generates dozen or hundreds of random tests for our
function based on its type hints, including corner cases. You can set up verifiers to
check that the output is the correct one. Useful to discover new bugs by covering
scenarios that you cannot manually check

```python
from hypothesis_auto import auto_pytest
from hypothesis_auto.tester import TestCase


def add(number_1: int, number_2: int = 1) -> int:
    return number_1 + number_2


@auto_pytest(add)
def test_add(test_case: TestCase, tmpdir):
    test_case.parameters  # Input parameters used
    output = test_case()  # Output of the function
```

This test generates many input combinations based on `int`.

## dataclass json

## yamldataclassconfig
