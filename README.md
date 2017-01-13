# itermplot

An awesome iTerm2 backend for Matplotlib, so you can plot directly in your terminal.

<img src="https://github.com/daleroberts/itermplot/raw/master/docs/lightdark.png" width="960">

The above is achieved with zero modifications to your Python script. For example, the above 
plots are generated with the following code:
```
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

plt.rcParams["font.size"] = 10

plt.figure(figsize=(8,3))

ax = plt.subplot(121)
x = np.arange(0,10,0.001)
ax.plot(x, np.sin(np.sinc(x)), 'r', lw=2)
ax.set_title('Nice wiggle')

ax = plt.subplot(122)
plt.tick_params(axis='both', left='off', top='off', right='off', bottom='off', labelleft='off', labeltop='off', labelright='off', labelbottom='off')
G = nx.random_geometric_graph(200, 0.125)
pos=nx.spring_layout(G)
nx.draw_networkx_edges(G, pos, alpha=0.2)
nx.draw_networkx_nodes(G, pos, node_color='r', node_size=12)
ax.set_title('Random graph')

plt.show()
```

Note: you need to run `plt.show()` to display the figure.

## Installation

To install, you need to have the `itermplot.py` file in your `PYTHONPATH` and have the `MPLBACKEND` 
environment variable set. One way to do this (permanently) is to add the following two lines to your
`.profile` file in your home directory.
```
export PYTHONPATH=~/itermplot:$PYTHONPATH
export MPLBACKEND="module://itermplot"
```

For reverse video, add the following to your `.profile`:
```
export ITERMPLOT="rv"
```