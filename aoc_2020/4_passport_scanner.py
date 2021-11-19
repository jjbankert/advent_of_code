from aoc_2020 import data_folder
import re
from typing import Callable
from functools import partial


class PassportPolicies:
    @staticmethod
    def is_valid_passport(passport: dict, policies: list[Callable[[dict], bool]]):
        return all(policy(passport) for policy in policies)

    @staticmethod
    def has_required_fields(passport: dict):
        return all(
            field in passport
            for field in {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
        )

    @staticmethod
    def valid_height(passport: dict):
        height = passport["hgt"]
        return (
            150 <= int(height[:-2]) <= 193
            if height[-2:] == "cm"
            else 59 <= int(height[:-2]) <= 76
            if height[-2:] == "in"
            else False
        )

    @staticmethod
    def valid_haircolor(passport: dict):
        return bool(re.match(r"#[0-9a-f]{6}", passport["hcl"]))

    @staticmethod
    def valid_eyecolor(passport: dict):
        return passport["ecl"] in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}

    @staticmethod
    def valid_passport_id(passport: dict):
        return bool(re.match(r"^[0-9]{9}$", passport["pid"]))


def main():
    raw_data = (data_folder / "4_passports.txt").read_text()
    passports = [parse_passport(passport) for passport in raw_data.split("\n\n")]

    policies = [
        PassportPolicies.has_required_fields,
        lambda passport: 1920 <= int(passport["byr"]) <= 2002,
        lambda passport: 2010 <= int(passport["iyr"]) <= 2020,
        lambda passport: 2020 <= int(passport["eyr"]) <= 2030,
        PassportPolicies.valid_height,
        PassportPolicies.valid_haircolor,
        PassportPolicies.valid_eyecolor,
        PassportPolicies.valid_passport_id,
    ]

    valid_passports = [
        passport
        for passport in passports
        if PassportPolicies.is_valid_passport(passport, policies)
    ]

    print(f"{len(valid_passports)=}")


def parse_passport(raw_data: str) -> dict[str, str]:
    return dict(
        pair.split(":")
        for line in raw_data.strip().split("\n")
        for pair in line.split(" ")
    )


if __name__ == "__main__":
    main()
