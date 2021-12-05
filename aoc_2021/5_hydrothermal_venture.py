from collections import Counter

import numpy

from aoc_2021 import load_data


def main():
    data = load_data(__file__)

    # preprocessing
    vent_lines = []
    for line in data:
        start, end = line.split(' -> ')
        start_position = numpy.fromstring(start, dtype='int32', sep=',')
        end_position = numpy.fromstring(end, dtype='int32', sep=',')
        vent_lines.append((start_position, end_position))
    vent_lines = numpy.array(vent_lines)

    print('Calculating', flush=True)

    # part 1
    horizontal_and_vertical_vents = numpy.concatenate((
        vent_lines[vent_lines[:, 0, 0] == vent_lines[:, 1, 0]],
        vent_lines[vent_lines[:, 0, 1] == vent_lines[:, 1, 1]]
    ))
    calculate_dangerous_positions(horizontal_and_vertical_vents)

    # part 2
    calculate_dangerous_positions(vent_lines)


def calculate_dangerous_positions(vent_lines: numpy.array):
    counter = Counter(
        position
        for start, end in vent_lines
        for position in discrete_steps(start, end)
    )

    dangerous_positions = {key: value for key, value in counter.items() if value > 1}
    print(len(dangerous_positions), flush=True)


def discrete_steps(start, end) -> list[tuple]:
    number_of_steps = max([abs(end[0] - start[0]), abs(end[1] - start[1])]) + 1
    return [
        tuple(position)
        for position
        in numpy.rint(numpy.linspace(start, end, num=number_of_steps)).astype('int32')
    ]


if __name__ == '__main__':
    main()
