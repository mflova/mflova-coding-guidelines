# Distribution

After creating your own code with own type hints, it is time to distribute the package.
Usually, type hints can be implemented in 3 ways:

- Type information inline (`.py`): This is in the same python files
- Type information via stubs (`.pyi`) in same package: Since Python 2 does not have type
  hints, this method would allow for backwards compatibility.
- Type information via stubs (`.pyi`) in different package: In case author does not want
  to include stubs into original repo, a different package that only contains stubs can
  also implement it.

I will focus only on the first case, as it will be the most common one.

## How types were distributed?

When you distribute a package with type information inline, it might look obvious where
the type hints are located (where the source code is). So, if `Python` interpreter can
import your package (i.e the path to source code is located), will static type checkers
will do it as well? Although the answer might be confusing: no.

Users and developers have been discussing for the best approach. Before having a standard
way, developers started adding `site-packages` folder to `MPYYPATH` so that the static
type checkers can find the source code. But why this was not directly implemented on the
static type checkers side? This is because in this same environment there might be
packages that are highly dynamic, causing type checkers to fail. Therefore, as a default
behaviour, static type checkers will ignore `site-packages`, even if your package has type
hints

## How can it be solved?

In [PEP561](https://peps.python.org/pep-0561/) a standard for type distribution in Python
was defined. This defines a new file called `py.typed`. This explicitly tells static type
checkers to use the type hints that can be found in that package. This is an empty file
that, when placed in a package, it will be applied in a recursive way to all sub-packages.

## How do I define the public interface of my package?

With the above approach, everything will work. However, there is one exception. This is
when we define our imports inside `__init__.py`. For example:

```python
# my_package.my_subpackage.__init__.py
from my_package.my_subpackage.tool import A
# Adding this line allows: from my_package.my_subpackage import A through implicit import.
```

When we do this, two new errors will be introduced for static tools:

- First, for our current package, linters or static type checkers will say that `A` is
  imported but unused. As it is the only line in `__init__.py`, the tools cannot know if
  this import is done to allow a implicit import.
- Secondly, in another repository, when we import this `A` by doing
  `my_package.my_subpackage import A`, static type checkers will raise an error saying
  "`my_package` does not explicitly export `A` attribute. This is because by default,
  implicit imports are forbidden.

What solutions do we have?

- First, defined by (PEP484)[https://peps.python.org/pep-0484/#stub-files], a new way of
  importing package is implemented to tell linters and static type checkers that this
  import is meant to be implicitly imported from another repository. This is
  `from ... import X as X`. Where `X` and `X` have to match.
- Secondoption is adding one more line with `__all__ = ["X"]` with the name of all modules
  or packages that will be implictely exported from another packages.
- Lastly, you can allow implicit reexports with `--implicit-reexport = True` for `Mypy`.
  Be aware that this might shadow some non intended implicit exports, so first two options
  are better recommended.