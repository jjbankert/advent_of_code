from aoc_2021 import load_data
import numpy
from collections import Counter


def main():
    data = load_data(__file__)

    vent_lines = []
    for line in data:
        start, end = line.split(' -> ')
        start_position = numpy.fromstring(start, dtype='int32', sep=',')
        end_position = numpy.fromstring(end, dtype='int32', sep=',')
        vent_lines.append((start_position, end_position))

    exact_counter = Counter()
    linspace_counter = Counter()
    for line in vent_lines:
        start, end = line

        # linspace
        number_of_steps = max([abs(end[0] - start[0]), abs(end[1] - start[1])]) + 1
        linspace_positions = [
            tuple(position)
            for position
            in numpy.rint(numpy.linspace(start, end, num=number_of_steps)).astype('int32')
        ]

        # exact
        # if start[0] == end[0]:
        #     lower_range = min(start[1], end[1])
        #     upper_range = max(start[1], end[1]) + 1
        #     length = upper_range - lower_range
        #     exact_positions = list(zip([start[0]] * length, range(lower_range, upper_range)))
        # elif start[1] == end[1]:
        #     lower_range = min(start[0], end[0])
        #     upper_range = max(start[0], end[0]) + 1
        #     length = upper_range - lower_range
        #     exact_positions = list(zip(range(lower_range, upper_range), [start[1]] * length))
        # else:
        #     col_direction = (end[0] - start[0]) // abs(end[0] - start[0])
        #     col_range = range(start[0], end[0] + col_direction, col_direction)
        #     row_direction = (end[1] - start[1]) // abs(end[1] - start[1])
        #     row_range = range(start[1], end[1] + row_direction, row_direction)
        #
        #     exact_positions = list(zip(col_range, row_range))

        # exact_counter.update(exact_positions)
        linspace_counter.update(linspace_positions)

    # debugging differences between exact and linspace counters
    # print(f"{exact_counter.most_common(10)=}")
    # print(f"{linspace_counter.most_common(10)=}")

    dangerous_positions = {key: value for key, value in linspace_counter.items() if value > 1}
    print(len(dangerous_positions))


if __name__ == '__main__':
    main()
