def install_jupyter_hook():
    from .formatter import array_to_html
    import numpy as np

    html_formatter = get_ipython().display_formatter.formatters["text/html"]
    return html_formatter.for_type(np.ndarray, array_to_html)
