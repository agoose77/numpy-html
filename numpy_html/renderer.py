import typing

import numpy as np


TD_ITEM_HTML_TEMPLATE = '<td style="font-family:monospace;white-space: pre;" align="center" title="{}">{}</td>'

ELLIPSIS_CELL_HTML_HORIZONTAL = TD_ITEM_HTML_TEMPLATE.format("element(s) elided", "\u2026")
ELLIPSIS_CELL_HTML_VERTICAL = TD_ITEM_HTML_TEMPLATE.format("element(s) elided", "\u22EE")
ELLIPSIS_CELL_HTML_DIAGONAL = TD_ITEM_HTML_TEMPLATE.format("element(s) elided", "\u22F1")
EMPTY_CELL_HTML = TD_ITEM_HTML_TEMPLATE.format("empty array", "\u2800")

INDEX_TYPE = typing.Tuple[int, ...]


class TemplateItem(typing.NamedTuple):
    template: str
    index: INDEX_TYPE
    item: typing.Any


ITEM_TYPE = typing.Union[TemplateItem, str]
ITEM_GENERATOR_TYPE = typing.Iterator[ITEM_TYPE]
SUMMARY_RENDERER_TYPE = typing.Callable[
    [INDEX_TYPE, np.ndarray, int], typing.Iterator[str]
]
ITEM_RENDERER_TYPE = typing.Callable[[INDEX_TYPE, np.ndarray, int], ITEM_GENERATOR_TYPE]


def make_constant_renderer(const: str) -> SUMMARY_RENDERER_TYPE:
    """Factory function for a single ellipsis renderer.

    :param const: constant string
    :return: generator which produces string
    """

    def wrapper(
        index: INDEX_TYPE, array: np.ndarray, edge_items: int
    ) -> typing.Iterator[str]:
        yield const

    return wrapper


def ellipsis_renderer_2d(
    index: INDEX_TYPE, array: np.ndarray, edge_items: int
) -> typing.Iterator[str]:
    n, m = array.shape
    yield "<tr>"
    if m > 2 * edge_items:
        for i in range(edge_items):
            yield ELLIPSIS_CELL_HTML_VERTICAL

        yield ELLIPSIS_CELL_HTML_DIAGONAL

        for i in range(edge_items):
            yield ELLIPSIS_CELL_HTML_VERTICAL
    else:
        for i in range(m):
            yield ELLIPSIS_CELL_HTML_VERTICAL
    yield "</tr>"


def extend_index(index: INDEX_TYPE, coordinate: int) -> INDEX_TYPE:
    return (*index, coordinate)


def render_array_items_summarized(
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


def render_array_items(
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
        yield from render_array_items_summarized(
            item_renderer, summary_renderer, index, array, edge_items
        )
    else:
        for i, item in enumerate(array):
            yield from item_renderer(extend_index(index, i), item, edge_items)


def render_array_0d(index: INDEX_TYPE, item, edge_items: int) -> ITEM_GENERATOR_TYPE:
    yield TemplateItem(f"<tr>{TD_ITEM_HTML_TEMPLATE}</tr>", index, item)


def render_row_1d(index: INDEX_TYPE, row, edge_items: int) -> ITEM_GENERATOR_TYPE:
    yield TemplateItem(f"<tr>{TD_ITEM_HTML_TEMPLATE}</tr>", index, row)


def render_array_1d(
    index: INDEX_TYPE, array: np.ndarray, edge_items: int
) -> ITEM_GENERATOR_TYPE:
    # Special case empty 1D arrays
    if not array.shape[0]:
        renderer = make_constant_renderer(EMPTY_CELL_HTML)
        return renderer(index, array, edge_items)

    return render_array_items(
        render_row_1d,
        make_constant_renderer(f"<tr>{ELLIPSIS_CELL_HTML_VERTICAL}</tr>"),
        index,
        array,
        edge_items,
    )


def render_elem_2d(index: INDEX_TYPE, item, edge_items: int) -> ITEM_GENERATOR_TYPE:
    yield TemplateItem(TD_ITEM_HTML_TEMPLATE, index, item)


def render_row_2d(
    index: INDEX_TYPE, row: np.ndarray, edge_items: int
) -> ITEM_GENERATOR_TYPE:
    yield "<tr>"
    yield from render_array_items(
        render_elem_2d,
        make_constant_renderer(ELLIPSIS_CELL_HTML_HORIZONTAL),
        index,
        row,
        edge_items,
    )
    yield "</tr>"


def render_array_2d(
    index: INDEX_TYPE, array: np.ndarray, edge_items: int
) -> ITEM_GENERATOR_TYPE:
    yield from render_array_items(
        render_row_2d, ellipsis_renderer_2d, index, array, edge_items
    )


def render_row_nd(
    index: INDEX_TYPE, row: np.ndarray, edge_items: int
) -> ITEM_GENERATOR_TYPE:
    yield "<tr><td>"
    yield from render_table(index, row, edge_items)
    yield "</td></tr>"


def render_array_nd(
    index: INDEX_TYPE, array: np.ndarray, edge_items: int
) -> ITEM_GENERATOR_TYPE:
    yield from render_array_items(
        render_row_nd,
        make_constant_renderer(ELLIPSIS_CELL_HTML_VERTICAL),
        index,
        array,
        edge_items,
    )


_shape_length_to_renderer = {0: render_array_0d, 1: render_array_1d, 2: render_array_2d}


def render_array(
    index: INDEX_TYPE, array: np.ndarray, edge_items: int
) -> ITEM_GENERATOR_TYPE:
    renderer = _shape_length_to_renderer.get(len(array.shape), render_array_nd)
    return renderer(index, array, edge_items)


def render_table(index: INDEX_TYPE, array, edge_items: int) -> ITEM_GENERATOR_TYPE:
    yield "<table style='border-style:solid;border-width:1px;'>"
    yield from render_array(index, array, edge_items)
    yield "</table>"
