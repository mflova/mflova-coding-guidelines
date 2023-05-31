# Pandas

## Speed up notes

[SOURCE](https://medium.com/geekculture/simple-tricks-to-speed-up-pandas-by-100x-3b7e705783a8)

### Avoid iterrows

If you want to iterate over all rows in a pandas dataframe, use `itertuples` instead. It cna speed up around x30.

### Vectorization

Think same as in numpy. Think about vectors instead of for loop iterating over specific elements. `Pandas` also implements vectorization techniques.
