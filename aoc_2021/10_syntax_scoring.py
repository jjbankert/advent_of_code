from aoc_2021 import load_data


class IllegalCharacter(Exception):
    pass


def main():
    data = load_data(__file__)

    symbol_pairs = {"(": ")", "[": "]", "{": "}", "<": ">"}
    syntax_symbol_values = {")": 3, "]": 57, "}": 1197, ">": 25137}
    completion_symbol_values = {"(": 1, "[": 2, "{": 3, "<": 4}

    # part 1
    syntax_value_counter = 0

    # part 2
    completion_values = []

    for line in data:
        open_chunks = []
        try:
            for symbol in line:
                if symbol in symbol_pairs:
                    open_chunks.append(symbol)
                else:
                    if open_chunks and symbol == symbol_pairs[open_chunks[-1]]:
                        open_chunks.pop()
                    else:
                        # part 1 syntax error
                        syntax_value_counter += syntax_symbol_values[symbol]
                        raise IllegalCharacter
        except IllegalCharacter:
            continue

        # part 2, now we have an incomplete line
        completion_value = 0
        for open_chunk in reversed(open_chunks):
            completion_value *= 5
            completion_value += completion_symbol_values[open_chunk]
        completion_values.append(completion_value)

    # part 1
    print(f"{syntax_value_counter=}")

    # part 2
    completion_values = sorted(completion_values, key=lambda value: len(str(value)))
    print(f"{completion_values[(len(completion_values)+1)//2]=}")


if __name__ == "__main__":
    main()
