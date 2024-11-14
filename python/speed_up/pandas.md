# Pandas

This document gathers everything related to speed up `Pandas` workflow.

## Built in Pandas

Specific tips for `pandas`:

### Methods

#### Reshape

- `pivot` represent data by giving the intersection of the index, columns and the
  aggregation values that you want to represent. Opposite of `melt`. (See images online to
  understand it better)
  - `pivot_table` is supposed to eb more powerful as it can handle repeated values by
    adding a `aggfunc`. However, it can be also considered more dangerous as more
    operations might be applied
- `pd.crosstab`: Build a table to see how two variables are correlated. It takes
  array-like or series as index, columns and values. By default, this will compute the
  count of the values, but I can provide any aggregation function
- `melt`: Opposite as `pivot`. It allows to move some columns as values (see images online
  to understand it better).
- `groupby`: Meant to group the information acccording to some criteria, apply an
  aggregation function, and then comnbine it into a new dataframe or series
- `stack/unstack`: With `unstack` the values from an index will be put as columns. `stack`
  will transform the data to a long-format while `unstack` will do it into a wide-format.
- `explode`: If we have a column whose associated values are lists, we can use `explode`
  to unpack these lists into multiple rows within the same dataframe.

#### Merge based

- `merge` merge two dataframes by providing matching values within a specific column that
  must be present in both dataframes.
  - Different modes (see more in the website):
    -  `left` saying that we are interested in perform the merge on the left dataframe
    - `inner` saying that we are interested in perform the merge on the dataframe only if
       both values exist in the columns
  - If the column is named different in both df, I can use the arguments `left_on` and
    `right_on`. If these values are in the index, I can indicate `left_index` or
    `right_index` (or both) as true. If both are set to true, I have the `join` method for
    that. It is an alias.
- `merge_asof`: Same as with `merge` but with not exact matches
- `concat`: Append all rows within an iterable of dataframes. It can also be changed to be
  column as the axis. `key` kwarg can be used to also create a new level in the axis where
  the data is appended.


### Advanced indexing

It is way more comfortable to use queries instead of masks. Easier to read:

```py
df = df.query("age > 20")
df = df.query("age > @min_age")  # Use variables
```

There are 2 main ways to index multiindex data:
  - Using `pd.IndexSlice`:
      ```py
      idx = pd.IndexSlice
      dfmi.loc[idx[:, :, ["C1", "C3"]], idx[:, "foo"]]
      ```
  - Using `.xs` to directly filter by a specific value within a specific level:
      ```py
      df.xs("one", level="second", drop_level=False/True)
      ```

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

## Interesting tools

- `pandas-profiling`: It generates HTML based reports to inspect a dataset. It can be also
  used to compare how a dataset changes over time.