from dataclasses import dataclass
from functools import partial
from pathlib import Path

from aoc_2020 import data_folder


def main():
    forest = Forest(data_folder / "3_forest.txt")
    slopes = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]
    for slope in slopes:
        path = forest.path(slope[0], slope[1])
        print(f"{slope=}, trees: {forest.trees_in_path(path)}")


@dataclass(frozen=True)
class Position:
    row: int
    column: int


class Forest:
    def __init__(self, path: Path):
        self.forest = path.read_text().splitlines()
        self.width = len(self.forest[0])
        self.default_downhill = partial(self.downhill, slope=1, sideways=3)

    def position_info(self, position: Position) -> str:
        return self.forest[position.row][position.column]

    def path(self, slope=1, sideways=3):
        positions = []
        current_position = Position(0, 0)
        while (
            current_position := self.downhill(current_position, slope, sideways)
        ) is not None:
            positions.append(current_position)

        return positions

    def downhill(self, start: Position, slope, sideways) -> Position:
        return (
            None
            if start.row + slope >= len(self.forest)
            else Position(start.row + slope, (start.column + sideways) % self.width)
        )

    def trees_in_path(self, path: list[Position]):
        return sum(1 for position in path if self.position_info(position) == "#")


if __name__ == "__main__":
    main()
