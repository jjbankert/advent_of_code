from aoc_2020 import data_folder


def main():
    boarding_passes = (data_folder / "5_boarding_passes.txt").read_text().splitlines()
    print(max(decode_binary(boarding_pass) for boarding_pass in boarding_passes))

    available_seats = {x for x in range(1024)}
    for boarding_pass in boarding_passes:
        available_seats.remove(decode_binary(boarding_pass))

    print(sorted(list(available_seats)))


def decode_binary(encoded: str):
    flipped_str = encoded[::-1]
    value = 0
    for idx, letter in enumerate(flipped_str):
        if letter in {"B", "R"}:
            value += 2 ** idx

    return value


if __name__ == "__main__":
    main()
