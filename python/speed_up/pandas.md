# Pandas

This document gathers everything related to speed up `Pandas` workflow.

## Built in Pandas

Specific tips for `pandas`:

### Avoid `iterrows`

Always avoid `iterrows`. This one creates a `Series` object for each row and has huge
overhead. Use `itertuples` instead. However, avoid iterating over rows when possible.
Give much more priority to vectorization and masking based techniques (see below).

### Avoid data type inference when possible

Make sure that when saving a pandas, it is done by preserving the `dtype` of each
column. Otherwise, inferring types might be slow the more rows you have.

### Use vectorized operations

`Pandas` is implemented on top of `numpy`. Since it is its backend all its data is coded
as a numpy array (which you can check with `df.values`). Therefore, think about applying
operations in a vectorized way (see `vectorization_and_numba.md` for more info about it).
You can use mask to select specific rows based on a given criteria:

```python
df[df["age"]> 20]  # This will take only those rows whose age is higher than 20
```

When working with dataframes as `numpy`, be aware that there are two main ways to get the
same array:

- Using `values`: Returns a VIEW of the underlying structure. Therefore is not
  recommended.
- Using `to_numpy()`: Is slightly slower (us order) but returns a `numpy` shallow copy.


#### More masking examples:

An alternative to apply following function to all rows:

```python
def func(a,b,c,d,e):
  if e == 10:
    return c*d
  elif (e < 10) and (e>=5):
    return c+d
  elif e < 5:
    return a+b
```

Is this one with masking and vectorized operations:

```python
df["new"] = df["c"] * df["d"]  # Default case e == 10
mask = df["e"] < 10
df.loc[mask, "new"] = df["c"] + df["d"]
mask = df["e"] < 5:
df.loc[mask, "new"] = df["a"] + df["b"]
```

### Indexing

#### Indexing multiple columns

You can index by column label mainly in two ways:

- `df["column"]` is extremley fast. When it is only a string, it typically returns
  a `pd.Series` which represents a view (reference) to that dataframe.
- `df[["column"]]` this is extremely slow. Although you can index multiple columns, this
  one will create a copy of type `Dataframe`.

In addition, these are the indexing speeds (quickest to slowest) in case you want to know:

  1. Python list
  2. Pandas Series: More logic than python built-in list.
  3. Pandas Dataframe: Much more inner logic.

To avoid creating a whole new dataframe when indexing with a list, you can directly
index one by one and work with `numpy` arrays after it.
The quickest approach found was the following one:

```python
lst: list[pd.Series] = []
for column in ("column1", "column2"):
  lst.append(df[column])  # Quickest indexing
arr = np.vstack(lst).T  # Build a numpy array. It takes 99% of the time but still really fast.
```

Note that here the column indices are lost!

If you want to preserve the column names, another solution could be storing the data
temporary in a dictionary:

```python
lst: dict[str, pd.Series] = []
for column in ("column1", "column2"):
  dict[column] = df[column]  # Quickext indexing
```

#### Indexing by column and indices

If you also want to filter by indices and column name, you can use `.loc` like:

```python
df.loc[range(1,100), "column"]
```

## Swifter

If you want to speed up `.apply` method when applying a function to all data, you can
install `swifter`. This package implements optimized techniques (like parallel
processing) coming from `dask` and it will apply always the quickest one. This way,
you would apply the method like this:

```python
import swifter

df.swifter.apply(my_func)
```

## GPU related

See `gpu_related.md`