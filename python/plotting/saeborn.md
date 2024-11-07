# Seaborn

The most interesting type of plots:

- `sns.scatterplot`: Scatter plot
- `sns.lmplot`: Similar to scatterplot but this one includes linear regression
- `sns.lineplot`: Typical lineplot
- `sns.jointplot`: Plots the information as a scatter and, on top of that, on the side, a
  histogram that represents each of the two variables. If you are looking for a more
  specific representation, be aware that these are created via `sns.JointGrid`. Take a
  look at it.
- `sns.violinplot`: Similar to boxplot but this one also plotting the distribution of the
  data. Its dicretized version can be seen as the `sns.swarmplot`.
- `sns.Facegrid`: This one, combined with `map` or `map_dataframe` allows you to define a
  grid where each column or row can be represented by a different variable. After it,
  `map_dataframe` will only need to indicate the type of plot you need `sns.lineplot`,
  `sns.scatterplot`... And corresponding kwargs. I can also pass a custom function that
  makes use of different functions of `sns` to repesent data as well.
- `sns.pairplot`: It will generate a grid that shows the correlation between variables
  given. Example: `sns.pairplot(iris, hue="species")`. Created under the hood with
  `sns.PairGrid`.
- `sns.heatmap` when the dataframe represents a table, heatmap will generate its
  corresponding heatmap

## Interesting features

### Hue

Most of the plots will have the keyword argument `hue` that allows you to group the data
of the plot according to a variable given (species, reflector...). Each kind of plot
will split it in a different way. For example, `lineplot` will just create multiple
series in different colors and then all of them will be overlapped. However, `boxplot`
will group all the boxes according to this `hue`.

### Subplots

When we cannot make use of `map_dataframe` from `FacetGrid` because we need to plot such
different things in both subplots, we can just rely on matplotlib to create our grid:

```py
#define dimensions of subplots (rows, columns)
fig, axes = plt.subplots(2, 2)

#create chart in each subplot
sns.boxplot(data=df, x='team', y='points', ax=axes[0,0])
sns.boxplot(data=df, x='team', y='assists', ax=axes[0,1])
```