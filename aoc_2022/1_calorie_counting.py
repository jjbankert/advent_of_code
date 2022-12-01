from aoc_2022 import load_data
from collections import Counter


def main(data=None):
    if data is None:
        data = load_data(__file__, splitlines=False).strip()
    print(f"{max_calories_by_elf(data)=}")
    print(f"{top_calories_by_elf(data)=}")
    print()


def max_calories_by_elf(data):
    max_elf = 0
    max_calories = 0
    for idx, elf_data in enumerate(data.split('\n\n'), start=1):
        elf_calories = sum(
            int(calorie_amount)
            for calorie_amount in elf_data.split('\n')
        )
        if elf_calories > max_calories:
            max_elf = idx
            max_calories = elf_calories

    return max_elf, max_calories


def top_calories_by_elf(data, topn=3):
    counter = Counter()
    for elf_idx, elf_data in enumerate(data.split('\n\n'), start=1):
        elf_calories = sum(
            int(calorie_amount)
            for calorie_amount in elf_data.split('\n')
        )
        counter.update({elf_idx: elf_calories})

    topn_calories = sum(elf_calories[1] for elf_calories in counter.most_common(topn))
    return topn_calories


if __name__ == '__main__':
    main("""1000
2000
3000

4000

5000
6000

7000
8000
9000

10000""")
    main()
