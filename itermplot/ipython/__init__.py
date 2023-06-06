"""
ipython extensions for image output handling.
e.g.

```ipython
%load_ext itermplot.ipython
```

implemented based on https://ipython.readthedocs.io/en/stable/config/shell_mimerenderer.html
"""

from .. import imgcat


def register_mimerenderer(ipython, mime, handler):
    ipython.display_formatter.active_types.append(mime)
    ipython.display_formatter.formatters[mime].enabled = True
    ipython.mime_renderers[mime] = handler


def imgcat_factory(fn):
    def _wrapper(img, _):
        if isinstance(img, bytes):
            return imgcat(img, fn=fn)
        elif hasattr(img, "read"):
            return imgcat(img.read(), fn=fn)
        elif isinstance(img, str):
            return imgcat(img.encode(), fn=fn)
        else:
            raise ValueError(
                "imgcat only accepts bytes, file-like objects, and strings"
            )

    return _wrapper


def load_ipython_extension(ipython):
    register_mimerenderer(ipython, "image/png", imgcat_factory(fn="img.png"))
    register_mimerenderer(ipython, "image/jpeg", imgcat_factory(fn="img.jpg"))
