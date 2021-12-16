import numpy as np

from aoc_2021 import load_data


def main():
    data = np.binary_repr(int(load_data(__file__)[0], 16))
    data = ((4 - len(data) % 4) % 4) * '0' + data  # pad with leading zeros

    decoder = Decoder(data)
    part_2_result = decoder.decode_packet()

    print(f"{decoder.version_total=}")
    print(f"{decoder.cursor=}")
    print(f"{part_2_result=}")


class Decoder:
    OPERATORS = [
        sum,
        np.product,
        min,
        max,
        None,
        lambda values: values[0] > values[1],
        lambda values: values[0] < values[1],
        lambda values: values[0] == values[1],
    ]

    def __init__(self, packet):
        self.packet = packet
        self.cursor = 0
        self.version_total = 0

    def decode_packet(self) -> int:
        version = int(self._next_n_bits(3), 2)
        self.version_total += version  # part 1

        packet_type = int(self._next_n_bits(3), 2)
        if packet_type == 4:
            result = self.decode_literal()
        else:
            operand_values = []  # part 2

            if self._next_n_bits(1) == '0':
                payload_length_in_bits = int(self._next_n_bits(15), 2)

                payload_end_cursor = self.cursor + payload_length_in_bits
                while self.cursor != payload_end_cursor:
                    operand_values.append(self.decode_packet())

            else:
                number_of_subpackets = int(self._next_n_bits(11), 2)
                for _ in range(number_of_subpackets):
                    operand_values.append(self.decode_packet())

            # part 2
            result = self.OPERATORS[packet_type](operand_values)

        return result

    def _next_n_bits(self, n):
        bits = self.packet[self.cursor:self.cursor + n]
        self.cursor += n
        return bits

    def decode_literal(self):
        window_size = 5
        window_idx = 0
        literal_value_bits = ''

        while True:
            window = self._next_n_bits(window_size)
            literal_value_bits += window[1:]
            window_idx += 1

            if window[0] == '0':
                break

        return int(literal_value_bits, 2)


if __name__ == '__main__':
    main()
