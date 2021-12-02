from aoc_2021 import data_folder
import numpy
from numpy.lib.stride_tricks import sliding_window_view


def main():
    raw_data = (data_folder / "1_sonar_sweep.txt").read_text()
    measurements = numpy.array([int(line) for line in raw_data.splitlines() if line])

    # 1
    print(increases(measurements))

    # 2
    # added_measurements = numpy.convolve(measurements, numpy.ones(3), mode='valid')
    added_measurements = numpy.sum(sliding_window_view(measurements, 3), axis=1)
    print(increases(added_measurements))


def increases(data: numpy.array):
    prev = data[0]
    increases = 0
    for datum in data[1:]:
        if datum > prev:
            increases += 1

        prev = datum

    return increases


if __name__ == '__main__':
    main()
