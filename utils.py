def get_grid_neighbors(grid, row, col, diagonal=False) -> set[tuple[int, int]]:
    if diagonal:
        raise NotImplemented

    neigbors = set()
    if row > 0:
        neigbors.add((row - 1, col))
    if row < grid.shape[0] - 1:
        neigbors.add((row + 1, col))
    if col > 0:
        neigbors.add((row, col - 1))
    if col < grid.shape[1] - 1:
        neigbors.add((row, col + 1))

    return neigbors


def gauss_summation(n) -> int:
    """calculate 1+2+...+n"""
    n = abs(n)
    return round(n * (n + 1) / 2)
