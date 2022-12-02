from aoc_2022 import load_data
from enum import Enum


class Shape(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


order = [Shape.PAPER, Shape.ROCK, Shape.SCISSORS]


class Outcome(Enum):
    LOSS = 0
    DRAW = 3
    WIN = 6


shapes_parsing = {
    'A': Shape.ROCK,
    'B': Shape.PAPER,
    'C': Shape.SCISSORS,
    'X': Shape.ROCK,
    'Y': Shape.PAPER,
    'Z': Shape.SCISSORS
}


def main(data=None):
    if data is None:
        data = load_data(__file__)
    data = [line.split(' ') for line in data]

    print(f"{part_1(data)=}")
    print(f"{part_2(data)=}")
    print()


def part_1(data):
    rules = {
        order[idx]: {
            order[(idx + 1) % len(order)]: Outcome.WIN,
            order[idx]: Outcome.DRAW,
            order[idx - 1]: Outcome.LOSS
        }
        for idx in range(len(order))
    }
    score = 0
    for other, you in data:
        you, other = shapes_parsing[you], shapes_parsing[other]
        score += you.value
        score += rules[you][other].value

    return score


def part_2(data):
    outcome_parsing = {'X': Outcome.LOSS, 'Y': Outcome.DRAW, 'Z': Outcome.WIN}

    inverted_rules = {
        order[idx]: {
            Outcome.WIN: order[idx - 1],
            Outcome.DRAW: order[idx],
            Outcome.LOSS: order[(idx + 1) % len(order)]
        }
        for idx in range(len(order))
    }

    score = 0

    for other, you in data:
        score += outcome_parsing[you].value
        score += inverted_rules[shapes_parsing[other]][outcome_parsing[you]].value

    return score


if __name__ == '__main__':
    main(['A Y', 'B X', 'C Z'])
    main()
