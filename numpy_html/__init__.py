from .formatter import array_to_html
import numpy as np


def install_jupyter_hook(cls=np.ndarray):
    """Install Jupyter display hook for a given array class

    :param cls: numpy-like array which is compatible with np.printoptions and np.array2string
    :return:
    """
    html_formatter = get_ipython().display_formatter.formatters["text/html"]
    return html_formatter.for_type(cls, array_to_html)


try:
    from IPython import get_ipython
except ImportError:
    pass
else:
    if get_ipython() is not None:
        install_jupyter_hook()
