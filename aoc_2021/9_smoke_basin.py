import itertools

import numpy as np
from scipy import ndimage

from aoc_2021 import load_data
from collections import Counter


def neighbors_smaller(window: np.array):
    return 1 if np.min(window[[0, 1, 3, 4]]) > window[2] else 0


class Cave:
    def __init__(self, terrain):
        self.terrain = terrain

        self.terrain_idx = {}
        self.basin_id = 0

    def determine_basin(self, row, col):
        if self.terrain[row][col] == 9:
            return

        location = (row, col)
        if location not in self.terrain_idx:
            neighbors = self.get_basin_neighbors(row, col)
            basin_id = None
            for neighbor in neighbors:
                if neighbor in self.terrain_idx:
                    basin_id = self.terrain_idx[neighbor]
                    break
            if basin_id is None:
                basin_id = self.new_basin_id()

            self.terrain_idx[location] = basin_id

            for neighbor in neighbors:
                if not neighbor in self.terrain_idx:
                    self.determine_basin(*neighbor)

    def get_basin_neighbors(self, row, col):
        neigbors = set()
        if row > 0:
            neigbors.add((row - 1, col))
        if row < self.terrain.shape[0] - 1:
            neigbors.add((row + 1, col))
        if col > 0:
            neigbors.add((row, col - 1))
        if col < self.terrain.shape[1] - 1:
            neigbors.add((row, col + 1))

        return neigbors

    def new_basin_id(self):
        self.basin_id += 1
        return self.basin_id


def main():
    raw_data = load_data(__file__)
    data = np.array([[int(char) for char in row] for row in raw_data])

    # part 1
    filter_footprint = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
    local_minima = ndimage.generic_filter(
        data,
        neighbors_smaller,
        footprint=filter_footprint,
        mode="constant",
        cval=9,
    )

    risk_levels = np.sum(data[local_minima == 1]) + np.sum(local_minima)
    print(f"{risk_levels=}")

    # part 2
    cave = Cave(data)
    for row, col in itertools.product(range(data.shape[0]), range(data.shape[1])):
        cave.determine_basin(row, col)

    top3_basins = Counter(cave.terrain_idx.values()).most_common(3)
    top3_sizes = [basin_size for basin_id, basin_size in top3_basins]

    print(f"{top3_basins=} -> {top3_sizes[0]*top3_sizes[1]*top3_sizes[2]}")


if __name__ == "__main__":
    main()
