from aoc_2021 import load_data
from collections import Counter, defaultdict


def main():
    template, insertion_rules_raw = load_data(__file__, splitlines=False).split("\n\n")
    insertion_rules = {}
    for rule in insertion_rules_raw.split("\n"):
        if not rule:
            continue

        element_pair, insert_element = rule.split(" -> ")
        insertion_rules[element_pair] = insert_element

    # part 1
    sorted_element_count_part_1 = naive_expansion(insertion_rules, template, 10)
    print(f"{sorted_element_count_part_1[0][1] - sorted_element_count_part_1[-1][1]}")

    # part 1 optimized
    sorted_element_count_part_1 = optimized_expansion(insertion_rules, template, 10)
    print(f"{sorted_element_count_part_1[0][1] - sorted_element_count_part_1[-1][1]}")

    # part 2
    sorted_element_count_part_2 = optimized_expansion(insertion_rules, template, 40)
    print(f"{sorted_element_count_part_2[0][1] - sorted_element_count_part_2[-1][1]}")


def naive_expansion(insertion_rules, template, iterations=10):
    polymer = list(template)
    for _ in range(iterations):
        new_polymer = [polymer[0]]
        for idx in range(len(polymer) - 1):
            pair = f"{polymer[idx]}{polymer[idx + 1]}"
            new_polymer.append(insertion_rules[pair])
            new_polymer.append(polymer[idx + 1])

        polymer = new_polymer

    element_count = Counter(polymer)
    print(f"{element_count=}")
    return list(element_count.most_common())


def optimized_expansion(insertion_rules, template, iterations=40):
    polymer = defaultdict(int)
    for idx in range(len(template) - 1):
        pair = f"{template[idx]}{template[idx + 1]}"
        polymer[pair] += 1

    for _ in range(iterations):
        new_polymer = defaultdict(int)
        for pair, count in polymer.items():
            new_polymer[f"{pair[0]}{insertion_rules[pair]}"] += count
            new_polymer[f"{insertion_rules[pair]}{pair[1]}"] += count

        polymer = new_polymer

    element_count = defaultdict(int)
    for pair, count in polymer.items():
        element_count[pair[1]] += count
    element_count[template[0]] += 1

    print(f"{dict(element_count)=}")
    return sorted(
        element_count.items(), key=lambda elem_count: elem_count[1], reverse=True
    )


if __name__ == "__main__":
    main()
