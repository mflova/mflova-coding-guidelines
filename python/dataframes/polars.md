# Polars

It mainly relies on the Expresions API. This one allows to concatenate multiple
expressions that can later be parallelized, optimized, sent to a GPU...
It relies either on eager dataframes or lazy dataframes.

## Selecting data

- For eager dataframes, you can use [] same as with `.loc` in pandas. Just remember that
  the indeces of a polars dataframe are ALWAYS numerical ones. There does not exist the
  concept of other "index"
- Most of the times is just recommended to use `select` along with an expression.
  Typically built with `pl.col()` for a column.

Another useful keyword is `pl.len()` which gives the current size of the dataframe on the
current context (this can be inside a groupby for example.)

## Filtering data

For this, you always have to use `.filter`. This one allows many expressions. Some examples are:

- Column names via `pl.col(name)`
- Regex expressions (starting with `^` and ending up with `$`): `pl.col("^*Example$")`
- `pl.exclude()` to select all but the excluded ones
- `pl.all()` to select all.
- `pl.col(pl.Int64)` to select all `Int64` columns
- `pl.col(pl.NUMERIC_DTYPES)` to select all numeric dtypes.
- Using the `selectors` API for more complex operations. This can be done with
  `import polars.selectors as cs` and allow things like: `cs.starts_with`, `cs.ends_with`,
  `cs.float`...

You can also use `.slice` to obtain a specific slice of the dataframe. Including one single row.

## Creating new columns

In general, `df.with_columns`  helps me to access already existing columns. Therefore I can:

- Edit a column `(pl.col("age")*2)`
- Create a new column based on an existing one `((pl.col("age")*2).alias("new_age"))`
- You can also use `.suffix` instead of `.alias` to preserve the original name and add a
  new suffix. It is also useful when I am operating with multiple columns.
- I can also create them based on a condition:

```py
# All arguments but first are the columns involved in `when`
# Last argument is the when itself that will create my new column
df.select([pl.col("Pclass"), pl.when(pl.col("PClass") == 1).then(1).otherwise(0).alias("firstClass")])
# I can also do .when().then().when().then().otherwise() as an example
```

I can also use `df.with_columns(pl.lit(2).alias("age"))` to create a new column with a
constant value.

Difference between `select` and `with_columns`? Select returns a set of subset of columns.
with_columns returns the whole dataframe.

## Sorting

- Sorting given column: `df.sort("Age")`
- Sorting given multiple column: `df.sort(["Age", "Gender"])`
- Sorting all: `df.sort(pl.all())`

I can set `set_sorted(ascending=True/False)` in order to indicate the framework that the
column is sorted. This will optimize even more the performance.

## Basic transformations

- I can rename columns with `.rename` I can sort columns with
  `df.select(sorted(df.columns))`
- I also have similar accessors compared to pandas (i.e `.str`):
  `pl.col("name").str.to_uppercase()`

## Missing values

They are all represented by `null`

Methods:

- `null_count()`
- `drop_nulls()`
- `is_null()`: Used for filtering
- `is_not_null()`: Used for filtering
- `fill_null()`: Replace nulls by the given value. Multiple strategies available.

Examples:

```py
# Drop all rows where the full rows is full of nulls
df.filter(pl.any_horizontal(pl.all().is_not_null()))
# Drop all rows where there is at least 1 null value
df.filter(pl.all_horizontal(pl.all().is_not_null()))
# Fill null values with the median
df.with_columns(pl.col("A").fill_null(pl.median(pl.col("A")).alias("B")))
# Interpolate missing values
df.with_columns(pl.all().interpolate().suffix("_new"))
```

## Categorical

In general, the optimize memory but add a bit of extra complexity.
I can cast a Categorical one with:

```py
pl.col("A").cast(pl.Categorical)
```

This will create a underlying representation for each label. Be aware that when I sort the
values, this will be done based on the physical representation (integers assocaited) and
not the lexical ordering. To operate better with categorical, I have `.cat` accessor.
There I can do operations such as: `.cat.set_ordering("lexical)`

If I create a context manager with `with pl.StringCache` this will generate inside this
context manager a string-based cache for all these categories. Thanks to this, I can
operate with them as if they were strings. I can also enable it globally with
`pl.enable_string_cache()`. This will perform interning of my strings, improving
performance.

Note: Pay also attention to `pl.Enum` type. It works similar to categorical but it is more
strict. It requires known all possible types and this will allow for extra performance and
validation.


## List dtype

I can also store lists inside each cell. If all lists are the same size, it is recommended
to cast it to `pl.Array` dtype. In general, I have similar methods comapred to `pandas`
such as `.explode`. In general, be aware that `.list` accessor is available. Most
important ones are `get`, `len`, `mean`...

## Statistics

Similar to pandas one. Note that there are some new ones like `max_horizontal`,
`min_horizontal` that will help you to compute metrics in a horizontal manner.

Groupby works quite similar to `pandas`. There is `map_groups` which is the equivalent to `apply`
.`pivot` requires an eager dataframe, so you will have to temporary collect.

In addition, there is also `.over` as an expresion. Differently to `groupby`, its output
is meant to be the same size of the dataframe, although the purpose is similar: computing
metrics based on a criteria that groups the data.

## Merging

There is mainly `pl.concat` and `pl.join` (equivalent to `pd.merge`). The first one has an
argument called `rechunk=True` by default that will reallocate the dataframes in adjacent
zones in memory.

## Low memory usage tricks

There are multiple tricks that can be done to lower done the memory usage:

- Using `scan_` based methods instead of `read_`. This will allow to use Lazy dataframes
  that optimize how the data is read
- Use of `streaming=True` in `collect` will process the data in batches. Useful to not
  overflow RAM memory. Not all expressions are supported. You can use
  `explain(streaming=True)` to verify this
- If you want to save a file from a `LazyFrame`, it is recommended to use the methods
  `sink_` instead of `write_`. The first one will not load the whole LazyFrame into
  memory.
- If the program is still collapsing when it comes to processing data, something you can
  do is either of these two:
  - Read an `ipc` based file (or `parquet`) and keep it in memory. Then, just before the
    processing, batch the data on your own. This will create multiple output batches that
    you can later concatenate with `pl.concat`.
  - If you need even more, scan the file and before processing it, create the batches.
    This way you are not storing the whole dataframe in memory.
