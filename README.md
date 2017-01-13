# itermplot

An awesome iTerm2 backend for Matplotlib, so you can plot directly in your terminal.

<img src="https://github.com/daleroberts/itermplot/raw/master/docs/lightdark.png" width="960">

## IPython support

<img src="https://github.com/daleroberts/itermplot/raw/master/docs/subplots.png" width="700">

Note: you need to run `plt.show()` to display the figure.

## Installation

To install, you need to have the `itermplot.py` file in your `PYTHONPATH` and have the `MPLBACKEND` 
environment variable set. One way to do this (permanently) is to add the following two lines to your
`.profile` file in your home directory.
```
export PYTHONPATH=~/itermplot:$PYTHONPATH
export MPLBACKEND="module://itermplot"
```