"""Read one-dimensional cell-centred grids from whitespace-separated text."""


def parse_grid(text: str) -> list[tuple[float, float]]:
    """Return (left_edge, right_edge) pairs for consecutive edge values.

    The input lists cell edges; n edges define n - 1 cells.
    """
    edges = [float(token) for token in text.split()]
    if len(edges) < 2:
        raise ValueError("a grid needs at least two edges")
    cells = []
    for i in range(0, len(edges) - 1):
        cells.append((edges[i], edges[i + 1]))
    return cells


def cell_widths(text: str) -> list[float]:
    return [right - left for left, right in parse_grid(text)]
