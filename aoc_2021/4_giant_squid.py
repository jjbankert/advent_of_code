from aoc_2021 import load_data
import numpy


def main():
    raw_data = load_data(__file__, splitlines=False)
    sections = raw_data.split('\n\n')
    drawn_numbers = [int(number) for number in sections[0].split(',')]
    bingo_cards = [parse_board(section) for section in sections[1:]]

    has_winner = False
    first_winner = None
    last_winner = None
    for drawn_number in drawn_numbers:
        if has_winner:
            break

        bingo_cards = [numpy.where(bingo_card[:, :] != drawn_number, bingo_card, -1) for bingo_card in bingo_cards]

        remaining_bingo_cards = []
        for card_idx, bingo_card in enumerate(bingo_cards):

            if has_bingo(bingo_card):
                if not first_winner:
                    card_sum = numpy.sum(numpy.where(bingo_card[:, :] == -1, 0, bingo_card))
                    first_winner = f"{card_sum=} * {drawn_number=} = {card_sum * drawn_number}"

                if len(bingo_cards) == 1:
                    card_sum = numpy.sum(numpy.where(bingo_card[:, :] == -1, 0, bingo_card))
                    last_winner = f"{card_sum=} * {drawn_number=} = {card_sum * drawn_number}"
            else:
                remaining_bingo_cards.append(card_idx)

        bingo_cards = [bingo_cards[idx] for idx in remaining_bingo_cards]




    print(first_winner)
    print(last_winner)


def parse_board(section: str) -> numpy.array:
    return numpy.array([[int(char) for char in line.split(' ') if char] for line in section.split('\n')])


def has_bingo(card: numpy.array) -> bool:
    return numpy.any(numpy.all(card == -1, axis=0)) or numpy.any(numpy.all(card == -1, axis=1))


if __name__ == '__main__':
    main()
