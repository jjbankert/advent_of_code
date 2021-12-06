from collections import defaultdict

from aoc_2021 import load_data


def main():
    data = load_data(__file__)
    lanternfish_school = defaultdict(int)
    for lanternfish in data[0].strip().split(','):
        lanternfish_school[int(lanternfish)] += 1

    for _ in range(256):
        new_school = defaultdict(int)
        for ttl, count in lanternfish_school.items():
            if ttl == 0:
                new_school[6] += count
                new_school[8] += count
            else:
                new_school[ttl - 1] += count
        lanternfish_school = new_school

    print(sum(lanternfish_school.values()))


if __name__ == '__main__':
    main()
