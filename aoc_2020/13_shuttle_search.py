from aoc_2020 import data_folder


def main():
    raw_data = (data_folder / "13_shuttle_search.txt").read_text()
    timestamp, buslines = raw_data.strip().split("\n")
    part_1(timestamp, buslines)

    part_2(buslines)


def part_1(timestamp, buslines):
    timestamp = int(timestamp)
    buslines = [int(line) for line in buslines.split(',') if line != 'x']

    next_arrival_time, next_arrival_line = min(
        ((next_arrival(timestamp, busline), busline) for busline in buslines),
        key=lambda arrival: arrival[0]
    )

    waiting_time = next_arrival_time - timestamp
    print(f"{waiting_time=} * {next_arrival_line=} = {waiting_time * next_arrival_line}")


def next_arrival(timestamp, busline):
    return timestamp if timestamp % busline == 0 else busline * (timestamp // busline + 1)


def part_2(buslines):
    deltas = {int(line): idx for idx, line in enumerate(buslines.split(',')) if line != 'x'}
    print(deltas)

    timestamp = 0
    while True:

        if all((timestamp + offset) % line == 0 for line, offset in deltas.items()):
            break
        timestamp += 823 - deltas[823]

        if timestamp % 100_000_000 == 0:
            print(timestamp)

    print(timestamp)


if __name__ == '__main__':
    main()
