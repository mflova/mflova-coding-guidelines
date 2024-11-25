# HoloViz

`HoloViz` is a whole group of tools made to represent, render and dashboard images or
interactive plots. The most interesting tools are:

- `panel`: Dashboard oriented. It allows to use many backends such as `plotly`, `bokeh` or
  `matplotlib`. This is something hard to find in other dashboard based tools.
- `holoviews`: Creates a uniform API regardless the backend used.
- `hvplot`: Built on top of `holoviews`. It provides extra functionalities such as
  interactive, visual plot generation (using hvplot.explorer)

## HvPlot

### Philosphy

Its main workflow is to integrate a new pandas dataframe accessor by doing this import:

```py
import hvplot.pandas  # noqa
```

After it you would use it similar to `df.plot` but with `df.hvplot` instead:

```py
df.hvplot.line(x='Year', y=['Art and Performance', 'Business', 'Biology', 'Education', 'Computer Science'], 
                value_label='% of Degrees Earned by Women', legend='top', height=500, width=620)
```

However, this will work well with interactive notebooks but the IDE will not autocomplete
this functionality. Therefore, an alternative is: py

```py
from hvplot import hvPlot

hvPlot(df).line(x="a", y="b")
```

### Main keywords

- `kind`: Kind of plot to use
- `by`: Split the data according to the column name given.
- `subplots`: If set to `True`, the `by` will be used to split the data into multiple
  plots.