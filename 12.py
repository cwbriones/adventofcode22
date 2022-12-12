import sys
import networkx
from collections import defaultdict


def to_adj(
    grid,
):
    adj = defaultdict(list)
    for i, j, _ in enumerate_grid(grid):
        for n in neighbors(grid, (i, j)):
            adj[(i, j)].append(n)
    return adj


def neighbors(grid, p):
    px, py = p
    for nx, ny in [(px - 1, py), (px + 1, py), (px, py - 1), (px, py + 1)]:
        if nx < 0 or nx >= len(grid[0]) or ny < 0 or ny >= len(grid):
            continue
        if ord(grid[ny][nx]) - ord(grid[py][px]) > 1:
            continue
        yield nx, ny


def find_replace(grid, target, replace):
    for j, row in enumerate(grid):
        for i, c in enumerate(row):
            if c == target:
                row[i] = replace
                return (i, j)
    return None


def enumerate_grid(grid):
    for j, row in enumerate(grid):
        for i, c in enumerate(row):
            yield i, j, c


def input():
    return [list(line.strip()) for line in sys.stdin.readlines()]


def main(grid):
    start = find_replace(grid, "S", "a")
    end = find_replace(grid, "E", "z")
    assert end is not None

    adj = to_adj(grid)
    graph = networkx.DiGraph(incoming_graph_data=adj)

    pathlens = networkx.shortest_path_length(graph, target=end)
    # one
    print(pathlens[start])

    # two
    starts = ((i, j) for i, j, c in enumerate_grid(grid) if c == "a")
    pathlen = min(pathlens[start] for start in starts if start in pathlens)
    print(pathlen)


if __name__ == "__main__":
    main(input())
