from aoc_2020 import data_folder


class CalculationError(Exception):
    pass


def main():
    raw_data = (data_folder / "8_handheld_halting.txt").read_text()
    code = list(raw_data.splitlines())
    print(run_code(code))

    code_variants = []
    for idx, line in enumerate(code):
        if line.startswith("jmp"):
            code_variants.append(code[:idx] + ["nop +0"] + code[idx + 1 :])
        elif line.startswith("nop"):
            jmp = "jmp" + line[3:]
            code_variants.append(code[:idx] + [jmp] + code[idx + 1 :])

    for code_variant in code_variants:
        try:
            variant_result = run_code(code_variant, True)
            print(variant_result)
            break
        except Exception:
            pass


def run_code(code: list[str], hard_fail=False) -> int:
    accumulator = 0
    visited_lines = set()
    current_line = 0
    while current_line not in visited_lines:
        visited_lines.add(current_line)

        line = code[current_line]
        if line.startswith("nop "):
            current_line += 1
        elif line.startswith("acc"):
            accumulator += int(line[4:])
            current_line += 1
        elif line.startswith("jmp"):
            current_line += int(line[4:])
        else:
            raise ValueError(line)

        if current_line >= len(code):
            break

    if hard_fail and current_line < len(code):
        raise CalculationError
    else:
        return accumulator


if __name__ == "__main__":
    main()
