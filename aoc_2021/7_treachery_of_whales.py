import numpy as np

from aoc_2021 import load_data
from utils import gauss_summation


def main():
    data = np.fromstring(
        load_data(__file__, splitlines=False).strip(), dtype="int", sep=","
    )

    # part 1
    idx_costs = {
        candidate_idx: np.sum(np.abs(data - candidate_idx))
        for candidate_idx in range(data.min(), data.max() + 1)
    }
    cheapest_idx(idx_costs)

    # part 2
    idx_costs = {
        candidate_idx: np.sum(gauss_summation(data - candidate_idx))
        for candidate_idx in range(data.min(), data.max() + 1)
    }

    cheapest_idx(idx_costs)


def cheapest_idx(idx_costs):
    lowest_idx, lowest_cost = next(iter(idx_costs.items()))
    for row_idx, row_cost in idx_costs.items():
        if row_cost < lowest_cost:
            lowest_idx, lowest_cost = row_idx, row_cost

    print(f"{lowest_idx=}, {lowest_cost=}")


if __name__ == "__main__":
    main()
