from functools import reduce
from itertools import product
from operator import mul

import numpy as np

from aoc_2021 import load_data


def main():
    data = load_data(__file__)
    # naive_solution(data) # requires manual trimming of the input to only contain the small boxes
    fancy_boxes_solution(data)


def naive_solution(data):
    grid = np.zeros((101, 101, 101), dtype=int)
    for row in data:
        value, x_slice, y_slice, z_slice = parse_row(row, offset=51)
        grid[x_slice, y_slice, z_slice] = value

    print(np.sum(grid))


def parse_row(row: str, offset=0):
    raw_value, raw_slices = row.split()
    value = 1 if raw_value == 'on' else 0
    x_slice, y_slice, z_slice = [
        parse_range(raw_slice, offset=offset)
        for raw_slice in raw_slices.split(',')
    ]

    return value, x_slice, y_slice, z_slice


def parse_range(raw_slice: str, offset: int):
    lower, upper = raw_slice.split('=')[1].split('..')
    return slice(int(lower) + offset, int(upper) + offset + 1, 1)


class Bounds:
    def __init__(self, min: int, max: int):
        self.min = min
        self.max = max

    def overlaps(self, other_bounds):
        return not self.min > other_bounds.max and not self.max < other_bounds.min

    @staticmethod
    def subtract_lower(one_bounds, other_bounds):
        if one_bounds.min <= other_bounds.min <= one_bounds.max:
            return Bounds(one_bounds.min, other_bounds.min - 1), Bounds(other_bounds.min, one_bounds.max)
        else:
            return None, one_bounds

    @staticmethod
    def subtract_upper(one_bounds, other_bounds):
        if one_bounds.min <= other_bounds.max <= one_bounds.max:
            return Bounds(other_bounds.max + 1, one_bounds.max), Bounds(one_bounds.min, other_bounds.max)
        else:
            return None, one_bounds

    def __repr__(self):
        return f"{self.min}..{self.max}"


class Box:
    def __init__(self, dimensions: dict[str, Bounds]):
        self.dimensions = dimensions

    @staticmethod
    def from_str(data: str):
        dimensions_bounds = data.split(',')
        dimensions = {}
        for dimension_bounds in dimensions_bounds:
            dimension, raw_bounds = dimension_bounds.split('=')
            dimensions[dimension] = Bounds(*[int(bound) for bound in raw_bounds.split('..')])
        return Box(dimensions)

    def is_valid(self):
        return all(bounds.min <= bounds.max for bounds in self.dimensions.values())

    def get_volume(self):
        return reduce(mul, [bounds.max - bounds.min + 1 for bounds in self.dimensions.values()])

    def __getitem__(self, dimension):
        return self.dimensions[dimension]

    def subtract(self, other_box):
        if not self.overlaps(other_box):
            return {self}

        resolved_boxes = set()
        unresolved_box = self

        for dimension, side_subtract_function in product(
                self.dimensions,
                [Bounds.subtract_lower, Bounds.subtract_upper]
        ):
            resolved_bounds, unresolved_bounds = side_subtract_function(unresolved_box[dimension], other_box[dimension])

            if resolved_bounds:
                resolved_box = Box(unresolved_box.dimensions | {dimension: resolved_bounds})
                if resolved_box.is_valid():
                    resolved_boxes.add(resolved_box)

            unresolved_box = Box(unresolved_box.dimensions | {dimension: unresolved_bounds})
            if not unresolved_box.is_valid():
                break

        return resolved_boxes

    def overlaps(self, other_box):
        return all(self[dimension].overlaps(other_box[dimension]) for dimension in self.dimensions)

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __repr__(self):
        return ','.join([
            f"{dimension}={repr(self[dimension])}"
            for dimension in sorted(self.dimensions)
        ])


def fancy_boxes_solution(data):
    # part 2
    lit_up_boxes = set()
    for row in data:
        is_lit_box, box_str = row.split(' ')
        new_box = Box.from_str(box_str)

        new_lit_up_boxes = set()
        while lit_up_boxes:
            lit_up_box = lit_up_boxes.pop()
            new_lit_up_boxes.update(lit_up_box.subtract(new_box))

        if is_lit_box == 'on':
            new_lit_up_boxes.add(new_box)

        lit_up_boxes = new_lit_up_boxes

    print(sum(box.get_volume() for box in lit_up_boxes))


if __name__ == '__main__':
    # equal boxes
    assert Box.from_str('x=0..1,y=0..1,z=0..1') == Box.from_str('x=0..1,y=0..1,z=0..1')

    # overlapping boxes in 1 dimension
    assert Box.from_str('x=0..2').subtract(Box.from_str('x=2..2')) == {Box.from_str('x=0..1')}
    assert Box.from_str('x=0..1,y=0..1,z=0..1').subtract(Box.from_str('x=0..0,y=0..1,z=0..1')) == \
           {Box.from_str('x=1..1,y=0..1,z=0..1')}

    # non-overlapping boxes
    assert Box.from_str('x=1..1,y=0..1,z=0..1').subtract(Box.from_str('x=0..0,y=0..1,z=0..1')) == \
           {Box.from_str('x=1..1,y=0..1,z=0..1')}
    assert Box.from_str('x=0..2,y=0..2,z=0..0').subtract(Box.from_str('x=1..2,y=1..2,z=1..1')) == \
           {Box.from_str('x=0..2,y=0..2,z=0..0')}

    # 2d boxes overlapping in 2 dimensions
    assert Box.from_str('x=0..2,y=0..2').subtract(Box.from_str('x=1..3,y=1..3')) == \
           {Box.from_str('x=0..0,y=0..2'), Box.from_str('x=1..2,y=0..0')}
    assert Box.from_str('x=1..3,y=1..3').subtract(Box.from_str('x=0..2,y=0..2')) == \
           {Box.from_str('x=3..3,y=1..3'), Box.from_str('x=1..2,y=3..3')}

    # 3d boxes overlapping in 3 dimensions
    assert Box.from_str('x=0..2,y=0..2,z=0..2').subtract(Box.from_str('x=1..3,y=1..3,z=1..3')) == \
           {Box.from_str('x=0..0,y=0..2,z=0..2'), Box.from_str('x=1..2,y=0..0,z=0..2'),
            Box.from_str('x=1..2,y=1..2,z=0..0')}

    # full overlap
    assert Box.from_str('x=0..1,y=0..1,z=0..1').subtract(Box.from_str('x=0..1,y=0..1,z=0..1')) == set()

    # 2d overlap in the middle
    assert Box.from_str('x=0..2,y=0..2').subtract(Box.from_str('x=1..1,y=1..1')) == \
           {Box.from_str('x=0..0,y=0..2'), Box.from_str('x=2..2,y=0..2'),
            Box.from_str('x=1..1,y=0..0'), Box.from_str('x=1..1,y=2..2')}

    main()
