from collections import defaultdict

from aoc_2021 import load_data


def main():
    graph = defaultdict(set)
    for row in load_data(__file__):
        start, end = row.split('-')

        # necessary for step 2, and a speed boost for step 1
        if start != 'end' and end != 'start':
            graph[start].add(end)

        if end != 'end' and start != 'start':
            graph[end].add(start)

    part_1_paths = search_multiple_upper(graph, ['start'])
    part_2_paths = search_twice_lower(graph, ['start'])

    print(f"{len(part_1_paths)=}")
    print(f"{len(part_2_paths)=}")


class Part2Path:
    def __init__(self, graph, path):
        self.graph = graph
        self.path = path
        self.path_members = set(path)


def search_multiple_upper(graph, path):
    paths = []

    for next_node in graph[path[-1]]:
        if next_node == 'end':
            paths.append(path + [next_node])
        elif (next_node.islower() and next_node not in path) or next_node.isupper():
            for longer_path in search_multiple_upper(graph, path + [next_node]):
                if longer_path:
                    paths.append(longer_path)

    return paths


def search_twice_lower(graph, path, any_small_twice=False):
    paths = []

    for next_node in graph[path[-1]]:
        if next_node == 'end':
            paths.append(path + [next_node])
        else:
            if next_node.islower():
                if next_node not in path:
                    longer_paths = search_twice_lower(graph, path + [next_node], any_small_twice)
                else:
                    if not any_small_twice:
                        longer_paths = search_twice_lower(graph, path + [next_node], True)
                    else:
                        longer_paths = []
            elif next_node.isupper():
                longer_paths = search_twice_lower(graph, path + [next_node], any_small_twice)
            else:
                longer_paths = []

            for longer_path in longer_paths:
                if longer_path:
                    paths.append(longer_path)

    return paths


if __name__ == '__main__':
    main()
