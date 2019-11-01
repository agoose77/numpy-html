from .formatter import array_to_html
import numpy as np


def install_jupyter_hook(cls=np.ndarray):
    """Install Jupyter display hook for a given array class

    :param cls: numpy-like array which is compatible with np.printoptions and np.array2string
    :return:
    """
    from IPython import get_ipython
    ipython = get_ipython()
    if ipython is None:
        raise RuntimeError("Must be running inside IPython environment")
    html_formatter = ipython.display_formatter.formatters["text/html"]
    return html_formatter.for_type(cls, array_to_html)


try:
    install_jupyter_hook()
except (ImportError, RuntimeError):
    pass
