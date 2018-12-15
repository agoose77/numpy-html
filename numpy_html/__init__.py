from .formatter import array_to_html


def install_jupyter_hook():
    import numpy as np

    html_formatter = get_ipython().display_formatter.formatters["text/html"]
    return html_formatter.for_type(np.ndarray, array_to_html)


try:
    ipython = get_ipython()
except NameError:
    pass
else:
    install_jupyter_hook()