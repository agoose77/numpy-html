import numpy as np
from .formatter import array_to_html


def register_formatter(ipython, cls):
    html_formatter = ipython.display_formatter.formatters["text/html"]
    html_formatter.for_type(cls, array_to_html)


def unregister_formatter(ipython, cls):
    html_formatter = ipython.display_formatter.formatters["text/html"]
    html_formatter.pop(cls)
            

def load_ipython_extension(ipython):
    register_formatter(ipython, np.ndarray)
    

def unload_ipython_extension(ipython):
    unregister_formatter(ipython, np.ndarray)
