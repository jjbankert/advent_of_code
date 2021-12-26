import numpy as np
from scipy import ndimage

from aoc_2021 import load_data


def main():
    grid = Grid.from_str(load_data(__file__))
    print(grid.run())
    print(grid)


class Grid:
    str_to_int = {
        '.': 0,
        '>': 1,
        'v': 2
    }

    int_to_str = {
        0: '.',
        1: '>',
        2: 'v'
    }

    def __init__(self, grid: np.array):
        self._grid = grid

    @staticmethod
    def from_str(input_str):
        return Grid(np.array([[Grid.str_to_int[item] for item in row] for row in input_str], dtype=int))

    def run(self):
        done = False
        steps = 0

        grid = self._grid
        while not done:
            if steps % 100 == 0:
                print(steps)

            # east
            new_grid = ndimage.generic_filter(grid, self._step, size=(1, 3), mode='wrap',
                                              extra_arguments=(self.str_to_int['>'],))
            # south
            new_grid = ndimage.generic_filter(new_grid, self._step, size=(3, 1), mode='wrap',
                                              extra_arguments=(self.str_to_int['v'],))

            if np.array_equal(grid, new_grid):
                done = True
                self._grid = new_grid
            else:
                grid = new_grid

            steps += 1

        return steps

    @staticmethod
    def _step(data, symbol):
        before, mid, after = data
        if after == 0 and mid == symbol:
            return 0
        elif mid == 0 and before == symbol:
            return before
        else:
            return mid

    def __repr__(self):
        return '\n'.join([''.join([self.int_to_str[item] for item in row]) for row in self._grid])


if __name__ == '__main__':
    main()
