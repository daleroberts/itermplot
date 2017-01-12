# -*- coding: utf-8 -*-
"""
An iTerm2 matplotlib backend

Author: Dale Roberts <dale.o.roberts@gmail.com>
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import six

import matplotlib
import sys
import os
import io 

from matplotlib._pylab_helpers import Gcf
from matplotlib.backend_bases import FigureManagerBase
from matplotlib.backends.backend_pdf import FigureCanvasPdf
from matplotlib.figure import Figure
from base64 import b64encode

TMUX = os.getenv('TERM','').startswith('screen')

def imgcat(data, lines=-1):
    if TMUX:
        if lines == -1:
            lines = 10
        osc = b'\033Ptmux;\033\033]'
        st = b'\a\033\\'
    else:
        osc = b'\033]'
        st = b'\a'
    csi = b'\033['
    buf = bytes()
    if lines > 0:
        buf += lines*b'\n' + csi + b'?25l' + csi + b'%dF' % lines + osc
        dims = b'width=auto;height=%d;preserveAspectRatio=1' % lines
    else:
        buf += osc
        dims = b'width=auto;height=auto'
    buf += b'1337;File=;size=%d;inline=1;' % len(data) + dims + b':'
    buf += b64encode(data) + st
    if lines > 0:
        buf += csi + b'%dE' % lines + csi + b'?25h'
    sys.stdout.buffer.write(buf)
    sys.stdout.flush()
    print()

def draw_if_interactive():
    if matplotlib.is_interactive():
        figmanager = Gcf.get_active()
        if figmanager is not None:
            figmanager.show()

def show():
    for manager in Gcf.get_all_fig_managers():
        manager.show()


def new_figure_manager(num, *args, **kwargs):
    FigureClass = kwargs.pop('FigureClass', Figure)
    thisFig = FigureClass(*args, **kwargs)
    return new_figure_manager_given_figure(num, thisFig)


def new_figure_manager_given_figure(num, figure):
    canvas = MyFigureCanvas(figure)
    manager = FigureManager(canvas, num)
    return manager


class MyFigureCanvas(FigureCanvasPdf):

    def __init__(self, figure):
        FigureCanvasPdf.__init__(self, figure)


class MyFigureManager(FigureManagerBase):

    def __init__(self, canvas, num):
        FigureManagerBase.__init__(self, canvas, num)

    def show(self):
        data = io.BytesIO()
        self.canvas.print_figure(data, bbox_inches='tight')
        imgcat(data.getbuffer())

FigureCanvas = MyFigureCanvas
FigureManager = MyFigureManager