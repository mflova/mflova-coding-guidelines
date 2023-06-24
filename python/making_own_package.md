# Making your own package

Typically, `poetry` is recommended. This one handles dependencies and python environments.

## Recommended set up

Since IDEs work only within your project scope, it is recommended to generate the `.venv`
inside your repository. By doing this, IDEs will automatically find the generated virtual
environment. This can be done by calling once the following command:

```shell
poetry config virtualenvs.in-project true
```

## Adding dependencies

These can be added from:

- `PyPi` repositories
- `git` repositories (azure, github...). You can provide `branch`, `rev` or `tag`
- `local` with `my_package = {path = "path/to/pkg_with_pyproject.toml, develop = True}`
  with `develop` flag being the equivalent of editable installation (`pip install -e `)

## Source files for your package

By default, `poetry` will search from the root directory the folders `src` and the folders
with same name as your package. If it cannot find it, you need to explicitly indicate it.
THis can be done as:

```toml
[tool.poetry]
package = {include = "my_package", from = "lib/random/"}
```

Where `include` is the name of the package (i.e folder) and `from` is the path where this
package can be located.

## What happens when you do poetry install?

A new virtual environment will be created (`.venv`) folder. This one contains a reference
to the python interpreter and all the packages. Packages are typically installed in `lib`.
However, all those package that were installed with `develop = True` and the current
package (the one being installed) will keep a reference to original source code through a
`.pth` file. This is a plain text file that contains the path where the package can be
located.