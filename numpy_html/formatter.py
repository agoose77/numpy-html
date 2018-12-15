from .renderer import _render_table
import numpy as np
from contextlib import contextmanager


@contextmanager
def printoptions(**opts):
    old_options = np.get_printoptions()
    np.set_printoptions(**opts)
    yield
    np.set_printoptions(**old_options)


def format_index(index):
    if len(index) == 1:
        return index[0]
    return index


def format_items(items, format_element, **format_kwargs):
    for item in items:
        if isinstance(item, str):
            yield item
        else:
            template, index, element = item
            yield template.format(
                format_index(index), format_element(element, **format_kwargs)
            )


def fixed_format_element_npy(x, max_width=None):
    x_str = np.array2string(x)
    if max_width is None:
        return x_str
    return f"{x_str:{max_width}}"


def fixed_format_items(items):
    items = list(items)
    with printoptions(floatmode="maxprec"):
        max_width = max(
            len(fixed_format_element_npy(e))
            for (_, _, e) in (t for t in items if isinstance(t, tuple))
        )
        return [*format_items(items, fixed_format_element_npy, max_width=max_width)]


def array_to_html(array, formatter=fixed_format_items, **formatter_kwargs):
    # Get print options
    print_options = np.get_printoptions()
    edge_items = print_options["edgeitems"]
    threshold = print_options["threshold"]
    if array.size < threshold:
        edge_items = 0

    items = _render_table((), array, edge_items)
    return "\n".join(formatter(items, **formatter_kwargs))
