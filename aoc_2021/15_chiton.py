import numpy as np

import utils
from aoc_2021 import load_data
from itertools import product


class Grid:
    def __init__(self, tile=1):
        costs = np.array(list([int(digit) for digit in row] for row in load_data(__file__)))
        self.costs = self._tiled_costs(costs, tile)

        self.completed = {(0, 0)}
        self.edge = {(0, 0)}
        self.costs[(0, 0)] = 0

    def _tiled_costs(self, costs, tile):
        row_width, col_height = costs.shape
        tiled_costs = np.zeros((row_width * tile, col_height * tile))

        for row_tile, col_tile in product(range(tile), range(tile)):
            offset = row_tile + col_tile
            tile = ((costs + offset - 1) % 9) + 1
            tiled_costs[
            row_width * row_tile:row_width * (row_tile + 1),
            col_height * col_tile:col_height * (col_tile + 1)
            ] = tile

        return tiled_costs

    def solve(self):
        counter = 0
        while self.edge:
            # progress message
            if counter % 100 == 0:
                print(f"{100 * (len(self.completed) + len(self.edge)) / np.product(self.costs.shape):.1f}%")
            counter += 1

            new_completed = set()
            new_edge_nodes = {}
            for node in self.edge:
                row, col = node
                neighbors = [
                    neighbor for neighbor in utils.get_grid_neighbors(self.costs, row, col)
                    if neighbor not in self.edge and neighbor not in self.completed
                ]

                # move from edge to completed
                if not neighbors:
                    new_completed.add(node)
                    continue

                # find lowest value new node
                for neighbor in neighbors:
                    neighbor_cost = self.costs[node] + self.costs[neighbor]
                    if neighbor not in new_edge_nodes or new_edge_nodes[neighbor] > neighbor_cost:
                        new_edge_nodes[neighbor] = neighbor_cost

            # move from edge to completed
            self.completed.update(new_completed)
            self.edge.difference_update(new_completed)

            # find lowest value new node
            if new_edge_nodes:
                new_edge_nodes_by_cost = sorted(new_edge_nodes.items(), key=lambda node_cost: node_cost[1])
                cheapest_new_edge_nodes_by_cost = [
                    node for node in new_edge_nodes_by_cost
                    if node[1] == new_edge_nodes_by_cost[0][1]
                ]
                for node, cost in cheapest_new_edge_nodes_by_cost:
                    self.edge.add(node)
                    self.costs[node] = cost


def main():
    part_1_grid = Grid()
    part_1_grid.solve()
    print(part_1_grid.costs)

    part_2_grid = Grid(tile=5)
    part_2_grid.solve()
    print(part_2_grid.costs)


if __name__ == '__main__':
    main()
