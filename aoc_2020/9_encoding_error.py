from aoc_2020 import data_folder
from itertools import combinations


def main(preamble_length=25):
    raw_data = (data_folder / "9_encoding_error.txt").read_text()
    data = [int(line.strip()) for line in raw_data.splitlines() if line]

    for lower_idx in range(0, len(data) - preamble_length - 1):
        preamble = data[lower_idx : lower_idx + preamble_length]
        target = data[lower_idx + preamble_length]
        if not in_previous_sums(target, preamble):
            print(target)
            weak_number = target
            break

    for idx in range(len(data)):
        intermediate_sum = 0
        length = 0
        while intermediate_sum < weak_number:
            length += 1
            intermediate_sum = sum(data[idx : idx + length])

        if intermediate_sum == weak_number:
            weak_sequence = data[idx : idx + length]
            print(weak_sequence)
            sorted_weak_sequence = sorted(weak_sequence)
            print(sorted_weak_sequence[0] + sorted_weak_sequence[-1])

            break


def in_previous_sums(target, previous_numbers):
    previous_numbers = list(set(previous_numbers))
    return any(target == x + y for x, y in combinations(previous_numbers, 2))


if __name__ == "__main__":
    main(25)
