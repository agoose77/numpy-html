import typing
from contextlib import contextmanager

import numpy as np

from .renderer import render_table, ITEM_TYPE, INDEX_TYPE, TemplateItem

# Type of elements or templates
ITEMS_TYPE = typing.Iterable[ITEM_TYPE]


def format_index(index: INDEX_TYPE) -> typing.Union[INDEX_TYPE, int]:
    """Format the index tuple corresponding to a particular array element. Return the

    :param index: tuple of integers representing the array index
    :return: sole entry of `index` if a tuple of length 1, otherwise `index`
    """
    if len(index) == 1:
        return index[0]
    return index


def format_items(items: ITEMS_TYPE, format_element: typing.Callable[..., str], **format_kwargs) -> typing.Iterator[str]:
    """Yield the formatted strings for the given items. Those items which are not templates are yielded directly.

    :param items: iterable of templates or strings
    :param format_element: array element formatter
    :param format_kwargs: additional keyword arguments for element formatter
    :return: Iterator of formatted strings
    """
    for item in items:
        if isinstance(item, str):
            yield item
        else:
            # We have a string template element, yield formatted string (using formatter and template)
            template, index, element = item
            yield template.format(format_index(index), format_element(element, **format_kwargs))


def fixed_format_element_npy(x, max_width: int = None) -> str:
    """Fixed with formatter using numpy.array2string. If `max_width` is None, then return the formatted element
    directly, otherwise left pad such that the final string has length `max_width`.

    :param x: element to render
    :param max_width: width of maximum element (predetermined)
    :return: formatted string
    """
    # Use numpy to format element
    x_str = np.array2string(x)
    if max_width is None:
        return x_str

    # Return padded left-aligned string
    return f"{x_str:{max_width}}"


def fixed_format_items(items: ITEMS_TYPE) -> typing.List[str]:
    """Format items using a fixed with formatter.

    :param items: iterable of templates or strings
    :return: formatted string
    """
    items = list(items)

    with np.printoptions(floatmode="maxprec"):
        template_lengths = [len(fixed_format_element_npy(t.item)) for t in items if isinstance(t, TemplateItem)]
        try:
            max_width = max(template_lengths)
        except ValueError:
            max_width = None
        return [*format_items(items, fixed_format_element_npy, max_width=max_width)]


def array_to_html(
    array: np.ndarray, formatter: typing.Callable[..., typing.List[str]] = fixed_format_items, **formatter_kwargs
) -> str:
    """Render NumPy array as an HTML table.

    :param array: ndarray object
    :param formatter: items formatter
    :param formatter_kwargs: keyword arguments for items formatter
    :return: HTML string
    """
    print_options = np.get_printoptions()
    edge_items = print_options["edgeitems"]
    threshold = print_options["threshold"]

    if array.size < threshold:
        edge_items = 0

    items = render_table((), array, edge_items)
    return "\n".join(formatter(items, **formatter_kwargs))
