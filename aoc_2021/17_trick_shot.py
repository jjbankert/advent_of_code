from itertools import product

from aoc_2021 import load_data
from utils import gauss_summation


def main(debug=False):
    print(load_data(__file__)[0])

    if debug:
        x_min = 20
        x_max = 30
        y_min = -10
        y_max = -5
    else:
        x_min = 211
        x_max = 232
        y_min = -124
        y_max = -69

    # part 1
    max_height = gauss_summation(abs(y_min) - 1)
    print(f"{max_height=}")

    # part 2
    min_x_speed = 1
    while gauss_summation(min_x_speed) < x_min:
        min_x_speed += 1

    print(f"{min_x_speed=}")

    valid_velocities = []

    for x_speed_initial, y_speed_initial in product(range(min_x_speed, x_max + 1), range(y_min, abs(y_min))):
        x_speed, y_speed = x_speed_initial, y_speed_initial
        x, y = 0, 0
        while x <= x_max and y >= y_min:
            x += x_speed
            y += y_speed
            if x_min <= x <= x_max and y_min <= y <= y_max:
                valid_velocities.append((x_speed_initial, y_speed_initial))
                break

            x_speed = x_speed - 1 if x_speed > 0 else 0
            y_speed -= 1

    print(valid_velocities)
    print(f"{len(valid_velocities)=}")


if __name__ == '__main__':
    main()
