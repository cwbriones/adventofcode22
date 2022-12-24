from collections import (
    deque,
)
import math
import sys

Pair = tuple[int, int]


def solve(board):
    """
    Solve the search problem via BFS.

    The search state is a 4-tuple:
        (x, y, z, nodes)

     x, y - standard coordinates
        z - the period we are in (explained below)
    found - the number of target nodes we have visited

    # Period

    Since the blizzards move a single space at a time, wrapping around,
    they have a periodic behavior. Because of this, we can cache all movements
    with (width * horizontal blizzards) + (height * vertical blizzards) space.

    Furthermore, we know the entire state of the board repeats every LCM(width, height)
    minutes. Therefore we encode this as a part of the search space so that if we
    are at the same coordinates at the same phase in the period, we can prune that
    search path.
    """
    x = board[0].index(".")
    y = 0

    xtarget = board[-1].index(".")
    xblizz, yblizz = extract(board)

    xcache = [set(p for (p, _) in xblizz)]
    width = len(board[1]) - 2
    for _ in range(width - 1):
        xblizz = advance(board, xblizz)
        xcache.append(set(p for (p, _) in xblizz))

    ycache = [set(p for (p, _) in yblizz)]
    height = len(board) - 2
    for _ in range(height - 1):
        yblizz = advance(board, yblizz)
        ycache.append(set(p for (p, _) in yblizz))

    targets = [
        (xtarget, len(board) - 1),
        (x, y),
        (xtarget, len(board) - 1),
    ]
    print(search(board, xcache, ycache, start=(x, y), targets=targets[:1]))
    print(search(board, xcache, ycache, start=(x, y), targets=targets))


def search(
    board: list[list[str]],
    xcache: list[set[Pair]],
    ycache: list[set[Pair]],
    start: Pair,
    targets: list[Pair],
):
    period = math.lcm(len(xcache), len(ycache))
    x, y = start
    fringe: deque[tuple[tuple[int, int, int, int], int]] = deque([((x, y, 0, 0), 0)])
    visited = set()
    while fringe:
        p, t = fringe.popleft()
        if p in visited:
            continue
        visited.add(p)
        # Try to move
        x, y, z, found = p
        if targets[found] == (x, y):
            found += 1
        if found == len(targets):
            return t
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx = x + dx
            ny = y + dy
            if ny >= len(board) or ny < 0 or board[ny][nx] == "#":
                continue
            if (nx, ny) in xcache[(z + 1) % len(xcache)]:
                continue
            if (nx, ny) in ycache[(z + 1) % len(ycache)]:
                continue
            fringe.append(((nx, ny, (z + 1) % period, found), t + 1))
        # Try to wait
        # "cannot share a position with a blizzard"
        if (x, y) in xcache[(z + 1) % len(xcache)]:
            continue
        if (x, y) in ycache[(z + 1) % len(ycache)]:
            continue
        fringe.append(((x, y, (z + 1) % period, found), t + 1))


def advance(board, blizzards: list[tuple[Pair, Pair]]) -> list[tuple[Pair, Pair]]:
    newblizz = []
    for ((x, y), (dx, dy)) in blizzards:
        nx = (x + dx) % len(board[0])
        ny = (y + dy) % len(board)
        while board[ny][nx] == "#":
            nx = (nx + dx) % len(board[0])
            ny = (ny + dy) % len(board)
        newblizz.append(((nx, ny), (dx, dy)))
    return newblizz


def extract(board):
    x_blizzards = []
    y_blizzards = []
    for y, row in enumerate(board):
        for x, c in enumerate(row):
            if c == "^":
                y_blizzards.append(((x, y), (0, -1)))
            elif c == "v":
                y_blizzards.append(((x, y), (0, 1)))
            elif c == "<":
                x_blizzards.append(((x, y), (-1, 0)))
            elif c == ">":
                x_blizzards.append(((x, y), (1, 0)))
    for (x, y), _ in x_blizzards:
        board[y][x] = "."
    for (x, y), _ in y_blizzards:
        board[y][x] = "."
    return x_blizzards, y_blizzards


def input():
    return [list(line.strip()) for line in sys.stdin.readlines()]


if __name__ == "__main__":
    solve(input())
