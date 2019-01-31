import typing

import numpy as np

ELLIPSIS_STR_HORIZONTAL = "<td><center>⋯</center></td>"
ELLIPSIS_STR_VERTICAL = "<td><center>⋮</center></td>"
ELLIPSIS_STR_DIAGONAL = "<td><center>⋱</center></td>"

TEMPLATE_TYPE = typing.Tuple[str, typing.Tuple[int, ...], typing.Any]
ITEM_TYPE = typing.Union[TEMPLATE_TYPE, str]
INDEX_TYPE = typing.Tuple[int, ...]
ITEM_GENERATOR_TYPE = typing.Iterator[ITEM_TYPE]
SUMMARY_RENDERER_TYPE = typing.Callable[[int, np.ndarray, int], typing.Iterator[str]]
ITEM_RENDERER_TYPE = typing.Callable[[INDEX_TYPE, np.ndarray, int], ITEM_GENERATOR_TYPE]


def make_constant_renderer(const: str) -> SUMMARY_RENDERER_TYPE:
    """Factory function for a single ellipsis renderer.

    :param const: constant string
    :return: generator which produces string
    """

    def wrapper(index: INDEX_TYPE, array: np.ndarray, edge_items: int) -> typing.Iterator[str]:
        yield const

    return wrapper


def ellipsis_renderer_2D(index: INDEX_TYPE, array: np.ndarray, edge_items: int) -> typing.Iterator[str]:
    n, m = array.shape
    yield "<tr>"
    if m > 2 * edge_items:
        for i in range(edge_items):
            yield ELLIPSIS_STR_VERTICAL

        yield ELLIPSIS_STR_DIAGONAL

        for i in range(edge_items):
            yield ELLIPSIS_STR_VERTICAL
    else:
        for i in range(m):
            yield ELLIPSIS_STR_VERTICAL
    yield "</tr>"


def extend_index(index: INDEX_TYPE, coordinate: int) -> INDEX_TYPE:
    return (*index, coordinate)


def render_array_summarized(
    item_renderer: ITEM_RENDERER_TYPE,
    summary_renderer: ITEM_RENDERER_TYPE,
    index: INDEX_TYPE,
    array: np.ndarray,
    edge_items: int,
) -> ITEM_GENERATOR_TYPE:
    """Render array, summarising the inner items that have indices between `edge_items` and `len(array)-edge_items`.

    :param item_renderer: item renderer
    :param summary_renderer: summary item renderer
    :param index: index
    :param array: array to render
    :param edge_items: number of edge items when summarising
    :return:
    """
    for i, item in enumerate(array[:edge_items]):
        yield from item_renderer(extend_index(index, i), item, edge_items)

    yield from summary_renderer(index, array, edge_items)

    for i, item in enumerate(array[-edge_items:], start=len(array) - edge_items):
        yield from item_renderer(extend_index(index, i), item, edge_items)


def _render_array_generic(
    item_renderer: ITEM_RENDERER_TYPE,
    summary_renderer: ITEM_RENDERER_TYPE,
    index: INDEX_TYPE,
    array: np.ndarray,
    edge_items: int,
) -> ITEM_GENERATOR_TYPE:
    """Render array, dispatching to `render_array_summarised` if required.

    :param item_renderer: item renderer
    :param summary_renderer: summary item renderer
    :param index: index
    :param array: array to render
    :param edge_items: number of edge items when summarising
    :return:
    """
    if edge_items and len(array) > 2 * edge_items:
        yield from render_array_summarized(item_renderer, summary_renderer, index, array, edge_items)
    else:
        for i, item in enumerate(array):
            yield from item_renderer(extend_index(index, i), item, edge_items)


def _render_row_1D(index: INDEX_TYPE, row, edge_items: int) -> ITEM_GENERATOR_TYPE:
    yield ("<tr><td style='font-family:monospace;white-space: pre;' title='{}'>{}</td></tr>", index, row)


def _render_array_1D(index: INDEX_TYPE, array: np.ndarray, edge_items: int) -> ITEM_GENERATOR_TYPE:
    return _render_array_generic(
        _render_row_1D, make_constant_renderer(f"<tr>{ELLIPSIS_STR_VERTICAL}</tr>"), index, array, edge_items
    )


def _render_elem_2D(index: INDEX_TYPE, item, edge_items: int) -> ITEM_GENERATOR_TYPE:
    yield ("<td style='font-family:monospace;white-space: pre;' title='{}'>{}</td>", index, item)


def _render_row_2D(index: INDEX_TYPE, row: np.ndarray, edge_items: int) -> ITEM_GENERATOR_TYPE:
    yield "<tr>"
    yield from _render_array_generic(
        _render_elem_2D, make_constant_renderer(ELLIPSIS_STR_HORIZONTAL), index, row, edge_items
    )
    yield "</tr>"


def _render_array_2D(index: INDEX_TYPE, array: np.ndarray, edge_items: int) -> ITEM_GENERATOR_TYPE:
    yield from _render_array_generic(_render_row_2D, ellipsis_renderer_2D, index, array, edge_items)


def _render_row_ND(index: INDEX_TYPE, row: np.ndarray, edge_items: int) -> ITEM_GENERATOR_TYPE:
    yield "<tr><td>"
    yield from _render_table(index, row, edge_items)
    yield "</td></tr>"


def _render_array_ND(index: INDEX_TYPE, array: np.ndarray, edge_items: int) -> ITEM_GENERATOR_TYPE:
    yield from _render_array_generic(
        _render_row_ND, make_constant_renderer(ELLIPSIS_STR_VERTICAL), index, array, edge_items
    )


def _render_array(index: INDEX_TYPE, array: np.ndarray, edge_items: int) -> ITEM_GENERATOR_TYPE:
    if len(array.shape) == 1:
        renderer = _render_array_1D
    elif len(array.shape) == 2:
        renderer = _render_array_2D
    else:
        renderer = _render_array_ND
    return renderer(index, array, edge_items)


def _render_table(index: INDEX_TYPE, array, edge_items: int) -> ITEM_GENERATOR_TYPE:
    yield "<table style='border-style:solid;border-width:1px;'>"
    yield from _render_array(index, array, edge_items)
    yield "</table>"
