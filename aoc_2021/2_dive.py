from aoc_2021 import load_data


def main():
    raw_data = load_data(__file__)
    actions = [(line.split(' ')[0], int(line.split(' ')[1])) for line in raw_data]
    step_1(actions)
    step_2(actions)

def step_1(actions):
    depth = 0
    horizontal = 0

    for direction, step_size in actions:
        if direction == 'forward':
            horizontal += step_size
        elif direction == 'down':
            depth += step_size
        elif direction == 'up':
            depth -= step_size

    print(depth * horizontal)


def step_2(actions):
    depth = 0
    horizontal = 0
    aim = 0

    for direction, step_size in actions:
        if direction == 'down':
            aim += step_size
        elif direction == 'up':
            aim -= step_size
        elif direction == 'forward':
            horizontal += step_size
            depth += aim * step_size

    print(depth * horizontal)


if __name__ == '__main__':
    main()
