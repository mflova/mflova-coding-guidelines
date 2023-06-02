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

## hypothesis

[Link](https://github.com/HypothesisWorks/hypothesis)

It can be used to cover a wide range of example inputs into your function or classes in
unit testing:

```python
@given(text())
def test_decode_inverts_encode(s):
    assert decode(encode(s)) == s
```

But it can also instantiate multiple of the class you want with `st.builds()`. This API
will create them based on a combination of its input arguments.

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

## pytest-find-dependencies

[Link](https://pypi.org/project/pytest-find-dependencies/)

It allows to find tests that, when combined together, trigger a FAIL.

## pyinstrument

[Link](https://github.com/joerick/pyinstrument)

Python profiler that can be used for both scripts and tests. Profile tests with:

```bash
pyinstrument -m pytest [pytest-args]
```

## strictyaml

[Link](https://github.com/crdoconnor/strictyaml)

StrictYAML is a type-safe YAML parser that parses and validates a restricted subset of
the YAML specification.

## Schema

[Link](https://github.com/keleshev/schema)

Validate any kind of structure by providing schema. These structure might be
dictionaries, callables, classes, int...

## pytest-fixture-typecheck

[Link](https://pypi.org/project/pytest-fixture-typecheck/)

Mypy cannot infere if type hints for fixtures are ok or not. This plugin will verify
during runtime that they are ok. If not, the test itself will fail.

It seems that it is no longer working.

## pytest-clarity

[Link](https://github.com/darrenburns/pytest-clarity)

Improves much more the diff in the assertions for built-in Python types

## numba

[Link](https://numba.pydata.org/)

More in `speed-up-md`

Perform just in time compilation for specific functions. This means that the code is
no longer fed into the Python interpreter, but compiled once and cached whenever it
is called. It works well with `numpy` and `for` loops
This library mainly uses one decorator:

```python
import numba

@numba.jit
def my_func():
    ...
```

Interesting flags:
 - `nopython`: Forces all the code to be compiled. If there is a problem, a exception
    is raised. Recommended to alwyas have it set to `True`
 - `parallel`: It will analyze the code and parallelize (multithread) if possible.
    You can also use  `prange` to explicitely indicate parallel loops.
 - `fastmath`: Sacrifice accuracy in exchange of speed

Note this module optionally works with CUDA.

Another decorator is `vectorize`. It allows to vectorize a function. THis is "grouping"
input data as vectors in order to use specific vector-based instructions inside the CPU.
It requires defining the signature of the function like in the example below. This
decorator can be also combined with `nopython` for greater improvement.

```python
from numba import vectorize, float64

@vectorize([float64(float64, float64)])
def f(x, y):
    return x + y
```

Vectorize tends to be much quicker than `jit`, as it provides more information to the
compiler.

## cupy

[Link](https://cupy.dev/)

More in `speed-up-md`

This library brings the GPU usage into Python. It implements has equivalent numpy and scipy
libraries but to work with GPU. The problem is that it needs to have CUDA and therefore a
NVIDIA GPU.
