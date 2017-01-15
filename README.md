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

### Reverse video

If you use a dark background in your terminal, you can enable "reverse video" mode by adding this to your `.profile`:
```
export ITERMPLOT="rv"
```

### TMUX support

itermplot tries to auto-detect TMUX and behave in a sane way. Vertical split panes do not work well due to a
limitation with iTerm2. Luckily, horizontals do though.

## Installation

### Using pip

Install using `pip` using the command:
```{sh}
pip3 install itermplot
```

itermplot is enabled by setting `MPLBACKEND` in your environment. If you use `bash`, then this can be accomplished using the command:
```{sh}
export MPLBACKEND="module://itermplot"
```
Note: you can add the `export` line above to your `.profile` file so that itermplot is always enabled in your terminal.

### Testing

To test your installation you can do the following in your iTerm2 console:
```
$ echo $MPLBACKEND
module://itermplot
$ python3
Python 3.5.2 (default, Oct 24 2016, 09:14:06)
[GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.38)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import matplotlib.pyplot as plt
>>> plt.plot([1,2,3])
[<matplotlib.lines.Line2D object at 0x1041f2e48>]
>>> plt.show()
```

You should see a plot!

## Uninstall

You can disable this backend by unsetting the `MPLBACKEND` environment variable.
```
$ unset MPLBACKEND
$ echo $MPLBACKEND

$ python3
Python 3.5.2 (default, Oct 24 2016, 09:14:06)
[GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.38)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import matplotlib.pyplot as plt
>>> plt.plot([1,2,3])
[<matplotlib.lines.Line2D object at 0x1106bdcc0>]
>>> plt.show()
```

To remove the package completely, run:
```
pip3 uninstall itermplot
```

## Bugs

This is backend is very alpha, so if you have a problem please raise an Issue on GitHub and I will try to fix it. Thanks.

I also accept (and appreciate!) patches / pull request.

## Other cool things

I encourage you to check-out some of my [other little projects](https://github.com/daleroberts). Lots more coming as I slowly release them...