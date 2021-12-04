from aoc_2021 import load_data
import numpy


def main():
    data = numpy.array([[int(char) for char in line] for line in load_data(__file__)])
    raw_gamma = numpy.round(numpy.average(data, axis=0))
    gamma = binary_array_to_decimal(raw_gamma)
    epsilon = binary_array_to_decimal(numpy.ones(len(raw_gamma))) - gamma
    print(gamma * epsilon)

    oxygen_rows = data
    for col_idx in range(data.shape[1]):
        col = oxygen_rows[:, col_idx]
        most_common_bit = numpy.floor(numpy.average(col) + 0.5)
        new_oxygen_rows = oxygen_rows[numpy.where(oxygen_rows[:, col_idx] == most_common_bit)[0]]

        if len(new_oxygen_rows) == 0:
            break
        elif len(new_oxygen_rows) == 1:
            oxygen_rows = new_oxygen_rows
            break
        else:
            oxygen_rows = new_oxygen_rows
    oxygen = binary_array_to_decimal(oxygen_rows[0])

    carbondioxide_rows = data
    for col_idx in range(data.shape[1]):
        col = carbondioxide_rows[:, col_idx]
        least_common_bit = int(numpy.floor(numpy.average(col) + 0.5)) ^ 1
        new_carbondioxide_rows = carbondioxide_rows[numpy.where(carbondioxide_rows[:, col_idx] == least_common_bit)[0]]

        if len(new_carbondioxide_rows) == 0:
            break
        elif len(new_carbondioxide_rows) == 1:
            carbondioxide_rows = new_carbondioxide_rows
            break
        else:
            carbondioxide_rows = new_carbondioxide_rows
    carbondioxide = binary_array_to_decimal(carbondioxide_rows[0])

    print(oxygen * carbondioxide)


def binary_array_to_decimal(binary_array: numpy.array) -> int:
    return int(''.join(str(int(digit)) for digit in binary_array), 2)


if __name__ == '__main__':
    main()
