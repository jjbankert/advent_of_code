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
            result = self.decode_operator(packet_type, operand_values)

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

    @staticmethod
    def decode_operator(packet_type, operand_values):
        match packet_type:
            case 0:
                return sum(operand_values)
            case 1:
                return np.product(operand_values)
            case 2:
                return min(operand_values)
            case 3:
                return max(operand_values)
            case 5:
                return 1 if operand_values[0] > operand_values[1] else 0
            case 6:
                return 1 if operand_values[0] < operand_values[1] else 0
            case 7:
                return 1 if operand_values[0] == operand_values[1] else 0
            case _:
                raise NotImplemented


if __name__ == '__main__':
    main()
