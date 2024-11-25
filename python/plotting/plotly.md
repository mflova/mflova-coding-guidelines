# Plotly

`plotly` follows a similar API compared to `seaborn`.

## API

One of the most useful modules is `express`, which can be found in
`import plotly.express as px`. This one provides a set of tools that will allow you to
generate quick and predefined plots. Similar to `seaborn` overall API.

## Main keywords

Some keywords are repeated among the different function calls. These are:

- `marginal_x`/`marginal_y`: Plot the marginal distribution of a bivariate distribution in
  one of the axis. This will lead to similar results as of `sns.jointplot`.
- `size` and `size_max`: Code the ifnormation on the size of the markers. `size_max` can
  be used to fix the maximum size that we will see within the plot.
- `facet_col` and `facet_row` to create subplots based on a value from the dataframe.
