import json
import operator
from functools import reduce
from uuid import uuid4

from aoc_2021 import load_data
from itertools import combinations


def main():
    data = load_data(__file__)

    # part 1
    snailfish_number = reduce(operator.add, (SnailfishNumber(row) for row in data))
    print(snailfish_number)
    print(snailfish_number.magnitude())
    print()

    # part 2
    max_magnitude = reduce(
        max,
        ((SnailfishNumber(row_a) + SnailfishNumber(row_b)).magnitude() for row_a, row_b in combinations(data, 2))
    )
    print(max_magnitude)


class SnailfishNumber:
    ROOT_NODE_ID = ''

    def __init__(self, elements: str):
        self.idx = {}
        self._add_node(json.loads(elements))
        self.reduce()

    def _add_node(self, elements, parent_id=None):
        node_id = str(uuid4()) if parent_id is not None else SnailfishNumber.ROOT_NODE_ID

        if isinstance(elements, int):
            self.idx[node_id] = Node(literal=elements, parent_id=parent_id)
        else:
            left, right = elements
            left_uuid = self._add_node(left, node_id)
            right_uuid = self._add_node(right, node_id)

            self.idx[node_id] = Node(left=left_uuid, right=right_uuid, parent_id=parent_id)

        return node_id

    def reduce(self):
        while True:
            has_exploded = False
            for node_id in self.literal_pair_node_ids():
                if self.node_depth(node_id) >= 4:
                    self.explode(node_id)
                    has_exploded = True
                    break
            if has_exploded:
                continue

            has_split = False
            for node_id in self.literal_node_ids():
                if self.idx[node_id].literal >= 10:
                    self.split(node_id)
                    has_split = True
                    break

            if not (has_exploded or has_split):
                break

    def literal_pair_node_ids(self, node_id=ROOT_NODE_ID):
        """find nodes that contain two literal nodes"""
        node = self.idx[node_id]
        left, right = self.idx[node.left_id], self.idx[node.right_id]
        if left.is_literal() and right.is_literal():
            yield node_id
        else:
            if not left.is_literal():
                yield from self.literal_pair_node_ids(node.left_id)
            if not right.is_literal():
                yield from self.literal_pair_node_ids(node.right_id)

    def node_depth(self, node_id):
        depth = 0
        node = self.idx[node_id]
        while True:
            if node.is_root():
                return depth
            else:
                node = self.idx[node.parent_id]
                depth += 1

    def explode(self, node_id):
        node = self.idx[node_id]
        left, right = self.idx[node.left_id], self.idx[node.right_id]

        adjacent_node = self.find_adjacent_literal_id(node_id, 'left')
        if adjacent_node is not None:
            self.idx[adjacent_node].literal += left.literal

        adjacent_node = self.find_adjacent_literal_id(node_id, 'right')
        if adjacent_node is not None:
            self.idx[adjacent_node].literal += right.literal

        node.literal = 0
        del self.idx[node.left_id]
        node.left_id = None
        del self.idx[node.right_id]
        node.right_id = None

    def find_adjacent_literal_id(self, node_id, direction):
        latest_id = node_id

        # searching up
        while True:
            node = self.idx[latest_id]

            parent_id = node.parent_id
            if parent_id is None:
                return None

            parent = self.idx[parent_id]
            parent_direction_child_id = parent.left_id if direction == 'left' else parent.right_id

            if parent_direction_child_id == latest_id:
                latest_id = parent_id
            else:
                latest_id = parent_direction_child_id
                break

        # searching down
        while True:
            node = self.idx[latest_id]

            if node.is_literal():
                return latest_id

            # checking for closest so we switch directions
            latest_id = node.right_id if direction == 'left' else node.left_id

    def literal_node_ids(self, node_id=ROOT_NODE_ID):
        """get ids of literal nodes from left to right"""
        node = self.idx[node_id]
        if node.is_literal():
            yield node_id
        else:
            yield from self.literal_node_ids(node.left_id)
            yield from self.literal_node_ids(node.right_id)

    def split(self, node_id):
        node = self.idx[node_id]

        left_value = node.literal // 2
        right_value = left_value + node.literal % 2

        node.literal = None
        node.left_id = self._add_node(left_value, node_id)
        node.right_id = self._add_node(right_value, node_id)

    def magnitude(self, node_id=ROOT_NODE_ID):
        node = self.idx[node_id]
        if node.is_literal():
            return node.literal
        else:
            return 3 * self.magnitude(node.left_id) + 2 * self.magnitude(node.right_id)

    def __add__(self, other):
        return SnailfishNumber(f"[{repr(self)},{repr(other)}]")

    def __repr__(self):
        return self._node_repr()

    def _node_repr(self, node_id=ROOT_NODE_ID):
        node = self.idx[node_id]
        return str(node.literal) if node.is_literal() \
            else f"[{self._node_repr(node.left_id)},{self._node_repr(node.right_id)}]"

    def __eq__(self, other):
        if isinstance(other, SnailfishNumber) and repr(self) == repr(other):
            return True
        return False


class Node:
    def __init__(self, literal=None, left=None, right=None, parent_id=None):
        self.literal = literal
        self.left_id = left
        self.right_id = right
        self.parent_id = parent_id

    def is_literal(self):
        return not self.literal is None

    def is_root(self):
        return self.parent_id is None

    def __repr__(self):
        if self.is_literal():
            return repr({key: value for key, value in self.__dict__.items() if key in {'literal', 'parent_id'}})
        else:
            return repr(
                {key: value for key, value in self.__dict__.items() if key in {'left_id', 'right_id', 'parent_id'}})


if __name__ == '__main__':
    assert SnailfishNumber('[[[[[9,8],1],2],3],4]') == SnailfishNumber('[[[[0,9],2],3],4]')
    assert SnailfishNumber('[7,[6,[5,[4,[3,2]]]]]') == SnailfishNumber('[7,[6,[5,[7,0]]]]')
    assert SnailfishNumber('[[6, [5, [4, [3, 2]]]], 1]') == SnailfishNumber('[[6,[5,[7,0]]],3]')
    assert SnailfishNumber('[[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]]') == SnailfishNumber(
        '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]')
    assert SnailfishNumber('[[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]') == SnailfishNumber(
        '[[3,[2,[8,0]]],[9,[5,[7,0]]]]')

    assert SnailfishNumber('[[[[4,3],4],4],[7,[[8,4],9]]]') + SnailfishNumber('[1,1]') == SnailfishNumber(
        '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]')

    main()
