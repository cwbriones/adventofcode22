from collections import (
    defaultdict,
)
import sys

def count(elves, x, y, dxs, dys):
    return sum(1
        for dx in dxs
        for dy in dys
        if (x + dx, y + dy) in elves
    )

def propose(elves, x, y, i=0):
    movedim = (-1, 0, 1)

    north = count(elves, x, y, dxs=movedim, dys=(-1,))
    south = count(elves, x, y, dxs=movedim, dys=(1,))
    west = count(elves, x, y, dys=movedim, dxs=(-1,))
    east = count(elves, x, y, dys=movedim, dxs=(1,))

    checks = [
        (north, (x, y - 1)),
        (south, (x, y + 1)),
        (west,  (x - 1, y)),
        (east,  (x + 1, y)),
    ]
    if (north + south + east + west) == 0:
        return (x, y)

    for j in range(i, i+4):
        c, move = checks[j % 4]
        if c == 0:
            return move
    return (x, y)

def solve(elves):
    proposals = defaultdict(list)
    moved = set()

    def round(i):
        nonlocal elves, moved
        for x, y in elves:
            move = propose(elves, x, y, i)
            proposals[move].append((x, y))
        done = True
        for dst, srcs in proposals.items():
            if len(srcs) == 1:
                done = done and dst == srcs[0]
                moved.add(dst)
            else:
                moved.update(srcs)
        elves, moved = moved, elves
        proposals.clear()
        moved.clear()
        return done

    for i in range(10):
        round(i)
    # bounding box
    minx, maxx, miny, maxy = bounding(elves)
    print(((maxx - minx + 1) * (maxy - miny + 1)) - len(elves))

    for i in range(10, 100_000):
        if round(i):
            print(i+1)
            break

def draw(elves):
    minx, maxx, miny, maxy = bounding(elves)

    height = maxy - miny + 1
    width = maxx - minx + 1
    output = [['.'] * width for _ in range(height)]
    for x, y in elves:
        output[y-miny][x-minx] = '#'
    for row in output:
        print(''.join(row))

def bounding(elves):
    minx = min(x for x, _ in elves)
    maxx = max(x for x, _ in elves)
    miny = min(y for _, y in elves)
    maxy = max(y for _, y in elves)
    return minx, maxx, miny, maxy


def input() -> set[tuple[int, int]]:
    elves = set()
    for y, row in enumerate([line.strip() for line in sys.stdin.readlines()]):
        for x, c in enumerate(row):
            if c == '#':
                elves.add((x,y))
    return elves


if __name__ == "__main__":
    elves = input()
    solve(elves)
