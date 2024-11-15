# Matplotlib


## Animations

You can generate an animation and export it as a GIF. 

Here there is a simple example:

```py
# libraries
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# initiate figure
fig, ax = plt.subplots(figsize=(10, 8), dpi=120)

def update(frame):
    ax.clear()
    ax.scatter(
      1+frame, 10+frame*10,
      s=600, alpha=0.5,
      edgecolors="black"
    )
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 100)
    return fig, ax

ani = FuncAnimation(fig, update, frames=range(10))
ani.save("my_animation.gif", fps=5)
``` 

If applied properly, these can also be done with `seaborn` as these are also built on top
of `matplotlib`.

More info and examples here: https://python-graph-gallery.com/animation/