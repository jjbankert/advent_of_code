from collections import defaultdict
from itertools import product
from aoc_2021 import load_data


def main():
    input_dots, input_folds = load_data(__file__, splitlines=False).split("\n\n")

    dots = set()
    for dot in input_dots.split("\n"):
        x, y = dot.split(",")
        dots.add((int(x), int(y)))

    for input_fold in input_folds.split("\n"):
        if not input_fold:
            continue

        dimension, position = input_fold[11:].split("=")
        position = int(position)

        dots = fold(dots, dimension, position)
        print(len(dots))

    for y, x in product(
        range(max(dot[1] for dot in dots) + 1), range(max(dot[0] for dot in dots) + 1)
    ):
        if x == 0:
            print()

        if (x, y) in dots:
            print("X", end="")
        else:
            print(" ", end="")


def fold(dots, dimension, position):
    new_dots = set()

    for dot in dots:
        if dimension == "x":
            new_dots.add(
                (dot[0] if dot[0] < position else 2 * position - dot[0], dot[1])
            )
        else:
            new_dots.add(
                (dot[0], dot[1] if dot[1] < position else 2 * position - dot[1])
            )

    return new_dots


if __name__ == "__main__":
    main()
