from aoc_2020 import data_folder


class Heading:
    HEADINGS = ['E', 'S', 'W', 'N']

    def __init__(self):
        self.heading_idx = 0

    def get(self):
        return self.HEADINGS[self.heading_idx]

    def update(self, action: str):
        direction = 1 if action[0] == 'R' else -1

        ticks = int(action[1:]) // 90
        self.heading_idx = (self.heading_idx + direction * ticks) % len(self.HEADINGS)

    def __str__(self):
        return self.get()

    def __repr__(self):
        return str(self)


heading_mults = {
    'N': (1, 0),
    'E': (0, 1),
    'S': (-1, 0),
    'W': (0, -1)
}


def part_1(data):
    north, east = 0, 0
    heading = Heading()

    for action in data.splitlines():

        if not action:
            continue

        if action[0] in {'L', 'R'}:
            heading.update(action)
            continue

        if action[0] == 'F':
            action = f"{heading.get()}{action[1:]}"

        heading_mult = heading_mults[action[0]]
        stepsize = int(action[1:])
        north, east = north + heading_mult[0] * stepsize, east + heading_mult[1] * stepsize

    print(f"{north=}, {east=}")
    distance = abs(north) + abs(east)
    print(f"{distance=}")


def part_2(data):
    waypoint_north, waypoint_east = 1, 10
    location_north, location_east = 0, 0

    rotation_transformation = {
        'L': (lambda north, east: (east, -north)),
        'R': (lambda north, east: (-east, north)),
    }

    for action in data.splitlines():

        if not action:
            continue

        if action[0] in {'L', 'R'}:
            for _ in range(int(action[1:]) // 90):
                waypoint_north, waypoint_east = rotation_transformation[action[0]](waypoint_north, waypoint_east)
            continue

        steps = int(action[1:])
        if action[0] == 'F':
            location_north += waypoint_north * steps
            location_east += waypoint_east * steps
        else:
            heading_mult = heading_mults[action[0]]
            waypoint_north = waypoint_north + heading_mult[0] * steps
            waypoint_east = waypoint_east + heading_mult[1] * steps

    print(f"{location_north=}, {location_east=}")
    distance = abs(location_north) + abs(location_east)
    print(f"{distance=}")


def main():
    raw_data = (data_folder / "12_rain_risk.txt").read_text()
    part_1(raw_data)

    part_2(raw_data)


if __name__ == '__main__':
    main()
