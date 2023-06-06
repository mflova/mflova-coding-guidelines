# numpy

This document comments specific things about how to speed up `numpy`.

## Avoid for loops

Instead, use `numpy`  built-in operations to entire vectors or arrays when possible.
Why? There are two main reasons:

- `numpy` is built in `C`. Using `Python` for loops to call `numpy` methods alternate
  all the time between `Python` interpreter and `C`, what makes it much slower.
- `numpy` is compiled with optimization flags from `C` compiler. Among them, it
  includes vectorized operations. These are `SIMD` nature (Single Input Multiple Data)
  where the `CPU` can apply a single operation to multiple data. It is like parallelism
  inside the own `CPU`. When you implement a for loop in `Python` to operate value by
  value, you are killing the advantage of this feature.

## Creating a new numpy array from multiple sub arrays

There are many ways to do so. However, the quickest one found is about storing all
sub-arrays in a `Python` built-in `list` and then passing it to functions that create
a `numpy` array from an iterable with multiple `numpy` arrays. Why? Because when you
do so, again, it will take advantage of vectorization based techniques. On the other
hand, if you build or expand the numpy array on each iteration, this feature will not
shine.

## Indexing

There are different ways of indexing in `numpy`:

- `arr[1]`: Using a integer
- `arr[1:3]`: Using a slice. This will return a subset of the array. View based
  (changes on this element will affect the original)
- `arr[[1,2]]`: Using a list. This will return a copy of the array.
- `arr[range(1,3)]`: Equivalent to indexing by list.

Although the three last ones return the same array, there is a huge difference in
performance, being the 2 last one the slowest ones, as it needs to create a copy
from the original object.