from aoc_2021 import load_data


class Digits:
    def __init__(self):
        self.idx = {}
        self.contents = set()

    @staticmethod
    def sort_seven_segments(seven_segments: str):
        return ''.join(sorted(seven_segments))

    def __setitem__(self, digit: int, seven_segments: str):
        self.idx[digit] = seven_segments
        self.idx[seven_segments] = digit
        self.contents.update([digit, seven_segments])

    def __getitem__(self, digit):
        return self.idx[digit]

    def __contains__(self, digit):
        return digit in self.contents

    def __repr__(self):
        return repr(self.idx)


def main():
    raw_data = load_data(__file__)
    data = []
    for row in raw_data:
        input_digits, output_digits = row.split(' | ')
        input_digits = set(Digits.sort_seven_segments(digit) for digit in input_digits.split(' '))
        output_digits = [Digits.sort_seven_segments(digit) for digit in output_digits.split(' ')]
        data.append((input_digits, output_digits))

    simple_digits_count = 0  # part 1
    output_values_sum = 0  # part 2

    for input_digits, output_digits in data:
        found_digits = Digits()

        # simple digits
        for input_digit in input_digits:
            if len(input_digit) == 2:
                found_digits[1] = input_digit
            elif len(input_digit) == 4:
                found_digits[4] = input_digit
            elif len(input_digit) == 3:
                found_digits[7] = input_digit
            elif len(input_digit) == 7:
                found_digits[8] = input_digit

        input_digits.difference_update({found_digits[1], found_digits[4], found_digits[7], found_digits[8]})

        # part 1
        easy_digits = {found_digits[1], found_digits[4], found_digits[7], found_digits[8]}
        for output_digit in output_digits:
            if output_digit in easy_digits:
                simple_digits_count += 1

        # find the 6 length digits
        six_len_digits = {input_digit for input_digit in input_digits if len(input_digit) == 6}
        input_digits.difference_update(six_len_digits)

        # find 9
        found_digits[9] = find_overlapping_digit_candidate_bigger(six_len_digits, found_digits[4])
        six_len_digits.remove(found_digits[9])

        # find 0
        found_digits[0] = find_overlapping_digit_candidate_bigger(six_len_digits, found_digits[1])
        six_len_digits.remove(found_digits[0])

        # fill in 6
        found_digits[6] = next(iter(six_len_digits))

        # only the 5 length input digits remain
        # find 5
        found_digits[5] = find_overlapping_digit_candidate_smaller(input_digits, found_digits[6])
        input_digits.remove(found_digits[5])

        # find 3
        found_digits[3] = find_overlapping_digit_candidate_bigger(input_digits, found_digits[7])
        input_digits.remove(found_digits[3])

        # fill in 2
        found_digits[2] = next(iter(input_digits))
        del input_digits

        # calculate number
        output_number = int(''.join(str(found_digits[digit]) for digit in output_digits))
        output_values_sum += output_number

    print(f"{simple_digits_count=}")
    print(f"{output_values_sum=}")


def find_overlapping_digit_candidate_bigger(candidate_digits, overlap_digit):
    for digit in candidate_digits:
        if all(char in digit for char in overlap_digit):
            return digit


def find_overlapping_digit_candidate_smaller(candidate_digits, overlap_digit):
    for digit in candidate_digits:
        if all(char in overlap_digit for char in digit):
            return digit


if __name__ == '__main__':
    main()
