from aoc_2020 import data_folder
from itertools import product


def main():
    raw_data = (data_folder / "11_seating_system.txt").read_text()
    grid = Grid(raw_data)
    current_hash = hash(grid)
    while True:
        grid.update()
        if (new_hash := hash(grid)) != current_hash:
            current_hash = new_hash
        else:
            break

    print(f"{grid.occupied_seats()=}")


class Grid:

    def __init__(self, grid: str):
        self.grid = grid.splitlines()

    def update(self):
        new_grid = []
        for row_idx, row in enumerate(self.grid):
            new_row = []

            for col_idx, symbol in enumerate(row):
                if symbol == '.':
                    new_row.append(symbol)
                    continue

                # neighbours
                neighbor_idxs = product(
                    range(max(0, row_idx - 1), min(len(self.grid), row_idx + 2)),
                    range(max(0, col_idx - 1), min(len(row), col_idx + 2))
                )

                neighbors = sum(
                    1
                    for neighbor_row, neighbor_col
                    in neighbor_idxs
                    if self.grid[neighbor_row][neighbor_col] == '#'
                )

                if symbol == 'L' and neighbors == 0:
                    new_row.append('#')
                elif symbol == '#' and neighbors >= 5:
                    new_row.append('L')
                else:
                    new_row.append(symbol)

            new_grid.append(new_row)

        self.grid = new_grid

    def occupied_seats(self):
        return sum(1 for row in self.grid for symbol in row if symbol == '#')

    def __str__(self):
        return '\n'.join(self.grid)

    def __hash__(self):
        return hash(str(self.grid))


if __name__ == '__main__':
    main()
