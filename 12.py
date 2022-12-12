from collections import (
    deque,
)
import sys
import copy


def one(grid):
    start = find_replace(grid, "S", "a")
    assert start is not None
    end = find_replace(grid, "E", "z")
    assert end is not None

    pathlen = search(grid, start, end)
    assert pathlen is not None
    print(pathlen)


def two(grid):
    find_replace(grid, "S", "a")
    end = find_replace(grid, "E", "z")
    assert end is not None

    shortest = min(
        pathlen
        for start in starts(grid, "a")
        if (pathlen := search(grid, start, end)) is not None
    )
    print(shortest)


def search(grid, start, end):
    fringe = deque([(start, 0)])
    visited = set()
    ny = len(grid)
    nx = len(grid[0])
    while fringe:
        p, pathlen = fringe.popleft()
        if p in visited:
            continue
        if p == end:
            return pathlen
        visited.add(p)
        x, y = p
        h = grid[y][x]
        for qx, qy in [(x - 1, y), (x + 1, y), (x, y + 1), (x, y - 1)]:
            if qx >= nx or qx < 0:
                continue
            if qy >= ny or qy < 0:
                continue
            if diff(h, grid[qy][qx]) > 1:
                continue
            q = (qx, qy)
            fringe.append((q, pathlen + 1))
    return None


def find_replace(grid, target, replace):
    for j, row in enumerate(grid):
        for i, c in enumerate(row):
            if c == target:
                row[i] = replace
                return (i, j)
    return None


def starts(grid, target):
    for j, row in enumerate(grid):
        for i, c in enumerate(row):
            if c == target:
                yield (i, j)


def diff(h1, h2):
    return ord(h2) - ord(h1)


def input():
    return [list(line.strip()) for line in sys.stdin.readlines()]


def main(lines):
    one(copy.deepcopy(lines))
    two(lines)


if __name__ == "__main__":
    main(input())
