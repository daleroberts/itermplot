# -*- coding: utf-8 -*-
"""
An iTerm2 matplotlib backend.

Author: Dale Roberts <dale.o.roberts@gmail.com>
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import six

import numpy as np
import matplotlib
import sys
import os
import io

from matplotlib._pylab_helpers import Gcf
from matplotlib.colors import ColorConverter
from matplotlib.backend_bases import FigureManagerBase, TimerBase
from matplotlib.backends.backend_mixed import MixedModeRenderer
from matplotlib.backends.backend_pdf import FigureCanvasPdf, PdfPages, PdfFile, RendererPdf
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.animation import ImageMagickWriter
from matplotlib.figure import Figure
from base64 import b64encode

to_rgba = ColorConverter().to_rgba
rcParams = matplotlib.rcParams

try:
    TMUX = os.getenv('TERM', '').startswith('screen')
    LINES = int(os.getenv('ITERMPLOT_LINES', '-1'))
    THEME = os.getenv('ITERMPLOT', '') # perhaps rename this now
    OUTFILE = os.getenv('ITERMPLOT_OUTFILE', 'out.gif')
    FRAMES = int(os.getenv('ITERMPLOT_FRAMES', '0'))
    COLORS = ColorConverter.colors
except ValueError:
    print('Error: problems with itermplot configuration.')
    sys.exit(1)

if sys.version_info < (3,):
    # Supporting Python 2 makes me want to cry :_(
    def B(x):
        return bytes(x)
else:
    def B(x):
        return bytes(x, 'utf-8')


def revvideo(x):
    """Try to 'reverse video' the color. Otherwise,
    return the object unchanged if it can't."""
    def rev(c):
        if isinstance(c, six.string_types):
            c = to_rgba(c)

        if len(c) == 4:
            r, g, b, a = c
            return (1.0 - r, 1.0 - g, 1.0 - b, a)
        else:
            r, g, b = c
            return (1.0 - r, 1.0 - g, 1.0 - b, 1.0)

    try:
        if isinstance(x, str) and x == 'none':
            return x
        if isinstance(x, np.ndarray):
            return np.array([rev(el) for el in x])
        return rev(x)
    except (ValueError, KeyError) as e:
        print('bad', x, e)
        return x


def imgcat(data):
    """Output the image data to the iTerm2 console. If `lines` is greater
    than zero then advance the console `lines` number of blank lines, move
    back, and then output the image. This is the default behaviour if TMUX
    is detected (lines set to 10)."""

    lines = LINES

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
        buf += lines * b'\n' + csi + b'?25l' + csi + B('%dF' % lines) + osc
        dims = 'width=auto;height=%d;preserveAspectRatio=1' % lines
    else:
        buf += osc
        dims = 'width=auto;height=auto'

    buf += B('1337;File=;size=%d;inline=1;' % len(data) + dims + ':')
    buf += b64encode(data) + st

    if lines > 0:
        buf += csi + B('%dE' % lines) + csi + b'?25h'

    if hasattr(sys.stdout, 'buffer'):
        sys.stdout.buffer.write(buf)
    else:
        sys.stdout.write(buf)
    sys.stdout.flush()

    print()


def draw_if_interactive():
    if matplotlib.is_interactive():
        figmanager = Gcf.get_active()
        if figmanager is not None:
            figmanager.show()


def show():
    figmanager = Gcf.get_active()
    if figmanager is not None:
        figmanager.show()
    else:
        for manager in Gcf.get_all_fig_managers():
            manager.show()


def new_figure_manager(num, *args, **kwargs):
    FigureClass = kwargs.pop('FigureClass', Figure)
    thisFig = FigureClass(*args, **kwargs)
    return new_figure_manager_given_figure(num, thisFig)


def new_figure_manager_given_figure(num, figure):
    canvas = FigureCanvasItermplot(figure)
    manager = FigureManager(canvas, num)
    return manager


class FigureCanvasItermplot(FigureCanvasPdf):

    def __init__(self, figure):
        FigureCanvasPdf.__init__(self, figure)
        self.reversed = False
        self.supports_blit = False
        self.timer = None

    def reverse(self, **kwargs):
        if self.reversed:
            return

        def modify(c):
            fcset = False

            try:
                ec = obj.get_edgecolor()
                obj.set_edgecolor(revvideo(ec))
            except AttributeError as e:
                pass

            try:
                fc = obj.get_facecolor()
                obj.set_facecolor(revvideo(fc))
                fcset = True
            except AttributeError as e:
                pass

            try:
                if not fcset:
                    c = obj.get_color()
                    obj.set_color(revvideo(c))
            except AttributeError as e:
                pass

        seen = set()
        for obj in self.figure.findobj():
            if not obj in seen:
                modify(obj)
            seen.add(obj)

        self.reversed = True

    def new_timer(self, *args, **kwargs):
        self.timer = TimerBase(*args, **kwargs)
        return self.timer

    def print_pdf(self, filename, **kwargs):
        transparent = kwargs.pop('transparent',
                                 rcParams['savefig.transparent'])

        if transparent:
            kwargs.setdefault('facecolor', 'none')
            kwargs.setdefault('edgecolor', 'none')
            original_axes_colors = []

            for ax in self.figure.axes:
                patch = ax.patch
                original_axes_colors.append((patch.get_facecolor(),
                                             patch.get_edgecolor()))
                patch.set_facecolor('none')
                patch.set_edgecolor('none')
        else:
            kwargs.setdefault('facecolor', rcParams['savefig.facecolor'])
            kwargs.setdefault('edgecolor', rcParams['savefig.edgecolor'])

        if 'rv' in THEME:
            self.reverse()

        FigureCanvasPdf.print_pdf(self, filename, **kwargs)


class ItermplotImageMagickWriter(ImageMagickWriter):

    def cleanup(self):
        # ImageMagickWriter perhaps can expose out and err, PR to Matplotlib
        # someday
        out, err = self._proc.communicate()
        self.data = io.BytesIO(out)
        self._frame_sink().close()


class ItermplotFigureManager(FigureManagerBase):

    def __init__(self, canvas, num):
        FigureManagerBase.__init__(self, canvas, num)

    def animate(self, loops, outfile=None, dpi=80):
        if outfile is None:
            outfile = 'gif:-'

        self.canvas.draw_event(None)
        
        writer = ItermplotImageMagickWriter()
        with writer.saving(self.canvas.figure, outfile, dpi):
            for _ in range(loops):
                self.canvas.timer._on_timer()
                writer.grab_frame()

        if outfile != 'gif:-':
            with open(outfile, 'rb') as f:
                data = io.BytesIO(f.read())
        else:
            data = writer.data

        return data

    def show(self):
        data = io.BytesIO()

        loops = FRAMES
        try:
            loops = int(loops)
        except ValueError:
            loops = 0
        if not loops or self.canvas.timer is None:
            self.canvas.print_figure(data, facecolor='none',
                                     edgecolor='none',
                                     transparent=True)
        else:
            outfile = OUTFILE
            data = self.animate(loops, outfile)

        if hasattr(data, 'getbuffer'):
            imgcat(data.getbuffer())
        else: # Python 2
            imgcat(data.getvalue())


FigureCanvas = FigureCanvasItermplot
FigureManager = ItermplotFigureManager
