from aoc_2020 import data_folder
from dataclasses import dataclass
from collections import Counter


@dataclass
class Row:
    lower_bound: int
    upper_bound: int
    letter: str
    password: str


def main():
    raw_data = (data_folder / "2_password_policy.txt").read_text()
    parsed_rows = parse(raw_data)

    # part 1
    compliant_rows = [row for row in parsed_rows if complies_with_old_policy(row)]
    print(len(compliant_rows))

    # part 2
    compliant_rows = [row for row in parsed_rows if complies_with_new_policy(row)]
    print(len(compliant_rows))


def parse(raw_data: str):
    rows = []
    for raw_line in raw_data.splitlines():
        clean_line = raw_line.strip()

        if not clean_line:
            continue

        raw_range, raw_letter, password = clean_line.split(" ")
        lower_bound, upper_bound = raw_range.split("-")
        letter = raw_letter.strip(":")

        rows.append(Row(int(lower_bound), int(upper_bound), letter, password))

    return rows


def complies_with_old_policy(row: Row):
    counted_letters = Counter(row.password)

    return row.lower_bound <= counted_letters.get(row.letter, 0) <= row.upper_bound


def complies_with_new_policy(row: Row):
    lower_compliance = (
        safe_get_from_string(row.password, row.lower_bound - 1) == row.letter
    )
    upper_compliance = (
        safe_get_from_string(row.password, row.upper_bound - 1) == row.letter
    )

    return (lower_compliance or upper_compliance) and not (
        lower_compliance and upper_compliance
    )


def safe_get_from_string(string: str, idx: int):
    return string[idx] if 0 <= idx < len(string) else None


if __name__ == "__main__":
    main()
