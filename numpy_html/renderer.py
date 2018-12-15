import numpy as np


ELLIPSIS_STR_HORIZONTAL = "<td><center>⋯</center></td>"
ELLIPSIS_STR_VERTICAL = "<td><center>⋮</center></td>"
ELLPISIS_STR_DIAGONAL = "<td><center>⋱</center></td>"


def ellipsis_renderer(ellipsis):
    def wrapper(index: int, array: np.ndindex, edge_items: int):
        yield ellipsis

    return wrapper


def ellipsis_renderer_2D(index: int, array: np.ndindex, edge_items: int):
    n, m = array.shape
    if m > 2 * edge_items:
        for i in range(edge_items):
            yield ELLIPSIS_STR_VERTICAL

        yield ELLPISIS_STR_DIAGONAL

        for i in range(edge_items):
            yield ELLIPSIS_STR_VERTICAL
    else:
        for i in range(m):
            yield ELLIPSIS_STR_VERTICAL


def extend_index(head, value):
    return (*head, value)


def render_array_summarized(
    render_item, render_summary, index: tuple, array: np.ndarray, edge_items: int
):
    for i, item in enumerate(array[:edge_items]):
        yield from render_item(extend_index(index, i), item, edge_items)

    yield from render_summary(index, array, edge_items)

    for i, item in enumerate(array[-edge_items:], start=len(array) - edge_items):
        yield from render_item(extend_index(index, i), item, edge_items)


def _render_array_generic(
    render_item, render_summary, index: tuple, array: np.ndarray, edge_items: int
):
    if edge_items and len(array) > 2 * edge_items:
        yield from render_array_summarized(
            render_item, render_summary, index, array, edge_items
        )
    else:
        for i, item in enumerate(array):
            yield from render_item(extend_index(index, i), item, edge_items)


def _render_row_1D(index: tuple, row, edge_items: int):
    yield (
        "<tr><td style='font-family:monospace;white-space: pre;' title='{}'>{}</td></tr>",
        index,
        row,
    )


def _render_array_1D(index: tuple, array: np.ndarray, edge_items: int):
    return _render_array_generic(
        _render_row_1D,
        ellipsis_renderer(f"<tr>{ELLIPSIS_STR_VERTICAL}</tr>"),
        index,
        array,
        edge_items,
    )


def _render_elem_2D(index: tuple, item, edge_items: int):
    yield (
        "<td style='font-family:monospace;white-space: pre;' title='{}'>{}</td>",
        index,
        item,
    )


def _render_row_2D(index: tuple, row: np.ndarray, edge_items: int):
    yield "<tr>"
    yield from _render_array_generic(
        _render_elem_2D,
        ellipsis_renderer(ELLIPSIS_STR_HORIZONTAL),
        index,
        row,
        edge_items,
    )
    yield "</tr>"


def _render_array_2D(index: tuple, array: np.ndarray, edge_items: int):
    yield from _render_array_generic(
        _render_row_2D, ellipsis_renderer_2D, index, array, edge_items
    )


def _render_row_ND(index: tuple, row: np.ndarray, edge_items: int):
    yield "<tr><td>"
    yield from _render_table(index, row, edge_items)
    yield "</td></tr>"


def _render_array_ND(index: tuple, array: np.ndarray, edge_items: int):
    yield from _render_array_generic(
        _render_row_ND,
        ellipsis_renderer(ELLIPSIS_STR_VERTICAL),
        index,
        array,
        edge_items,
    )


def _render_array(index: int, array: np.ndarray, edge_items: int):
    if len(array.shape) == 1:
        renderer = _render_array_1D
    elif len(array.shape) == 2:
        renderer = _render_array_2D
    else:
        renderer = _render_array_ND
    return renderer(index, array, edge_items)


def _render_table(index: tuple, array, edge_items: int):
    yield "<table style='border-style:solid;border-width:1px;'>"
    yield from _render_array(index, array, edge_items)
    yield "</table>"
