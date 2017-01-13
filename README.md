# itermplot

An awesome iTerm2 backend for Matplotlib, so you can plot directly in your terminal.

<img src="https://github.com/daleroberts/itermplot/raw/master/docs/lightdark.png" width="960">

The above is achieved with zero modifications to your Python script. For example, the above 
plots are generated with the following code:
```{python}
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

## Reverse video

If you use a dark background in your terminal, you can enable "reverse video" mode by adding this to your `.profile`:
```
export ITERMPLOT="rv"
```

## Installation

### Using pip

Install using `pip` using the command:
```{sh}
pip3 install git+https://github.com/daleroberts/itermplot.git
```

Add `MPLBACKEND` to your environment. If you use `bash`, then this can be accomplished using the command:  
```{sh}
export MPLBACKEND="module://itermplot"
```
You can add the `export` line above to your `.profile` file so that itermplot is always enabled in your terminal.

### Manually

To install manually, you need to have the `itermplot.py` file in your `PYTHONPATH` and have the `MPLBACKEND` 
environment variable set. One way to do this (permanently) is to add the following two lines to your
`.profile` file in your home directory.
```{sh}
export PYTHONPATH=~/itermplot:$PYTHONPATH
export MPLBACKEND="module://itermplot"
```

## Bugs

This is backend is very alpha, so if you have a problem please raise an Issue on GitHub and I will try to fix it. Thanks.