import sys
import copy
from search import ucs


def one(grid):
    start = find_replace(grid, "S", "a")
    assert start is not None
    end = find_replace(grid, "E", "z")
    assert end is not None

    pathlen = ucs(grid, start, end, connected)
    assert pathlen is not None
    print(pathlen)


def two(grid):
    find_replace(grid, "S", "a")
    end = find_replace(grid, "E", "z")
    assert end is not None

    shortest = min(
        pathlen
        for start in starts(grid, "a")
        if (pathlen := ucs(grid, start, end, connected)) is not None
    )
    print(shortest)


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


def connected(h1, h2):
    return ord(h2) - ord(h1) <= 1


def input():
    return [list(line.strip()) for line in sys.stdin.readlines()]


def main(lines):
    one(copy.deepcopy(lines))
    two(lines)


if __name__ == "__main__":
    main(input())
