import numpy as np
from itertools import product
from aoc_2021 import load_data


class Octopus:
    def __init__(self, energy_level: int):
        self.energy_level = energy_level

    def increment_energy(self):
        self.energy_level += 1
        return self.energy_level

    def reset(self):
        self.energy_level = 0

    def __str__(self):
        return str(self.energy_level)

    def __repr__(self):
        return str(self)


class Grid:
    def __init__(self, data):
        self._grid = np.array([
            [Octopus(int(level)) for level in line]
            for line in data
        ])

    def get_octopus(self, row, col):
        return self._grid[row][col]

    def time_step(self):
        processed_flash_locations = set()
        new_flash_locations = set()

        for row, col in product(range(self._grid.shape[0]), range(self._grid.shape[1])):
            if self.get_octopus(row, col).increment_energy() > 9:
                new_flash_locations.add((row, col))

        while new_flash_locations:
            new_flash_location = new_flash_locations.pop()
            processed_flash_locations.add(new_flash_location)

            for neighbor in self.neighbors(*new_flash_location):
                if self.get_octopus(*neighbor).increment_energy() > 9:
                    if not (neighbor in new_flash_locations or neighbor in processed_flash_locations):
                        new_flash_locations.add(neighbor)

        for processed_flash_location in processed_flash_locations:
            self.get_octopus(*processed_flash_location).reset()

        return len(processed_flash_locations)

    def neighbors(self, row, col):
        neighbors = set(
            (neighbor_row, neighbor_col)
            for neighbor_row, neighbor_col
            in product(
                range(max(row - 1, 0), min(row + 2, self._grid.shape[0])),
                range(max(col - 1, 0), min(col + 2, self._grid.shape[1]))
            )
        )
        neighbors.remove((row, col))
        return neighbors

    def __str__(self):
        return '\n'.join([''.join([str(octopus) for octopus in row]) for row in self._grid])

    def __repr__(self):
        return str(self)


def main():
    grid = Grid(load_data(__file__))

    iteration = 0
    total_flashes_after_100_steps = 0
    first_all_flash_step = None
    while iteration < 100 or first_all_flash_step is None:
        print(iteration)
        print(grid)
        print()

        step_flashes = grid.time_step()
        iteration += 1

        # part 1
        if iteration <= 100:
            total_flashes_after_100_steps += step_flashes

        # part 2
        if step_flashes == grid._grid.size and first_all_flash_step is None:
            first_all_flash_step = iteration

    print(grid)
    print()
    print(f"{total_flashes_after_100_steps=}")
    print(f"{first_all_flash_step=}")


if __name__ == '__main__':
    main()
