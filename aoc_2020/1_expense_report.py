import json
from itertools import combinations
from aoc_2020 import data_folder


def main():
    expenses = json.loads((data_folder / "1_expenses.json").read_text())
    iterate_over_expenses(combinations(expenses, 2), 2020)
    iterate_over_expenses(combinations(expenses, 3), 2020)


def iterate_over_expenses(expense_combinations, desired_sum):
    for combination in expense_combinations:
        product_for_specified_sum(combination, desired_sum)


def product_for_specified_sum(expenses, desired_sum):
    if sum(expenses) == desired_sum:
        print(f"{' * '.join([str(expense) for expense in expenses])} = {product(*expenses)}")


def product(*numbers):
    result = 1
    for number in numbers:
        result *= number

    return result


if __name__ == "__main__":
    main()
