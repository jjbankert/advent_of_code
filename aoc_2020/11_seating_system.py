from aoc_2020 import data_folder
from itertools import product


def main():
    raw_data = (data_folder / "11_seating_system.txt").read_text()
    grid = Grid(raw_data)
    current_hash = hash(grid)

    print(f"{str(grid)}\n\n")
    while True:
        grid.update('complex')
        if (new_hash := hash(grid)) != current_hash:
            current_hash = new_hash
            print(f"{str(grid)}\n\n")
        else:
            break

    print(f"{grid.occupied_seats()=}")


class Grid:

    def __init__(self, grid: str):
        self.grid = grid.splitlines()

    def update(self, strategy: str):
        new_grid = []
        for row_idx, row in enumerate(self.grid):
            new_row = []

            for col_idx, symbol in enumerate(row):
                if symbol == '.':
                    new_row.append(symbol)
                    continue

                neighbors = self.get_unoccupied_neighbor_seats_simple(row_idx, col_idx) \
                    if strategy == 'simple' \
                    else self.get_unoccupied_neighbor_seats_complex(row_idx, col_idx)

                if symbol == 'L' and neighbors == 0:
                    new_row.append('#')
                elif symbol == '#' and neighbors >= 5:
                    new_row.append('L')
                else:
                    new_row.append(symbol)

            new_grid.append(new_row)

        self.grid = new_grid

    def get_unoccupied_neighbor_seats_simple(self, row_idx, col_idx):
        # neighbours
        neighbor_idxs = product(
            range(max(0, row_idx - 1), min(len(self.grid), row_idx + 2)),
            range(max(0, col_idx - 1), min(len(self.grid[row_idx]), col_idx + 2))
        )

        return sum(
            1
            for neighbor_row, neighbor_col
            in neighbor_idxs
            if self.grid[neighbor_row][neighbor_col] == '#'
        )

    def get_unoccupied_neighbor_seats_complex(self, row_idx, col_idx):
        steps = set(step for step in product([-1, 0, 1], repeat=2))
        steps.remove((0, 0))

        neighbors = 0
        for step in steps:
            new_row_idx, new_col_idx = row_idx + step[0], col_idx + step[1]
            while 0 <= new_row_idx < len(self.grid) and 0 <= new_col_idx < len(self.grid[row_idx]):
                symbol = self.grid[new_row_idx][new_col_idx]
                if symbol == '.':
                    new_row_idx, new_col_idx = new_row_idx + step[0], new_col_idx + step[1]
                else:
                    if symbol == '#':
                        neighbors += 1
                    break

        return neighbors

    def occupied_seats(self):
        return sum(1 for row in self.grid for symbol in row if symbol == '#')

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.grid)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(str(self.grid))


if __name__ == '__main__':
    main()
