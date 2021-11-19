from aoc_2020 import data_folder

from collections import defaultdict
from itertools import combinations


def main():
    raw_data = (data_folder / "10_adapter_array.txt").read_text()
    complete_chain = sorted([int(line.strip()) for line in raw_data.splitlines()])
    complete_chain = [0] + complete_chain + [complete_chain[-1] + 3]

    deltas = defaultdict(int)
    for lower, higher in zip(complete_chain[:-1], complete_chain[1:]):
        deltas[higher - lower] += 1

    print(deltas)
    print(deltas[1] * deltas[3])

    subsections = get_subsections(complete_chain)
    print(subsections)

    subsection_variations = []
    for idx, subsection in enumerate(subsections):
        if idx > 0:
            subsection = [subsections[idx - 1][-1]] + subsection

        if idx < len(subsections) - 1:
            subsection = subsection + [subsections[idx + 1][0]]

        subsection_variations.append(len(get_subsection_variations(subsection)))

    print(product(*subsection_variations))


def product(*numbers):
    result = 1
    for number in numbers:
        result *= number

    return result


def get_subsections(chain: list[int]) -> list[list[int]]:
    chain_of_chains = []
    new_chain = []
    for idx in range(len(chain) - 1):
        new_chain.append(chain[idx])

        if chain[idx + 1] == chain[idx] + 3:
            chain_of_chains.append(new_chain)
            new_chain = []

    return chain_of_chains


def get_subsection_variations(chain: list[int]) -> list[list[int]]:
    if len(chain) == 1:
        return [chain]

    start = chain[0]
    middle_chain = chain[1:-1]
    end = chain[-1]

    variations = [[start, end]]
    for length in range(1, len(middle_chain)):
        for combination in combinations(middle_chain, length):
            variation = [start] + list(combination) + [end]
            if is_valid_chain(variation):
                variations.append(variation)

    return variations


def is_valid_chain(chain: list[int]) -> bool:
    return all(higher - lower <= 3 for lower, higher in zip(chain[:-1], chain[1:]))


if __name__ == "__main__":
    main()
