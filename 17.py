import os
import sys
import time
from copy import deepcopy

# fmt: off
pieces = [
    ["....",
     "....",
     "....",
     "####"],

    ["....",
     ".#..",
     "###.",
     ".#.."],

    ["....",
     "..#.",
     "..#.",
     "###."],

    ["#...",
     "#...",
     "#...",
     "#..."],

    ["....",
     "....",
     "##..",
     "##.."],
]
# fmt: on
DIM = 4

if os.environ.get("DEBUG"):

    def debug(msg):
        print("[DEBUG]: ", end="", file=sys.stderr)
        print(msg, file=sys.stderr)

else:

    def debug(msg):
        pass


# Each piece is 4 wide and 4 tall
def can_place(grid, piece, x, y):
    if y < 0 or x < 0 or x >= len(grid[0]):
        return False
    while len(grid) < y + DIM:
        grid.append(["."] * 7)

    #    ....
    #    ....
    #    ####
    #    ^
    #    coord
    for py in reversed(range(DIM)):
        gy = y + (DIM - 1 - py)
        for px in range(DIM):
            gx = px + x
            if gx >= len(grid[gy]):
                if piece[py][px] == ".":
                    continue
                return False
            if grid[gy][gx] == "#" and piece[py][px] == "#":
                return False
    return True


def place(grid, piece, x, y):
    for py in reversed(range(DIM)):
        gy = y + (DIM - 1 - py)
        debug(f'py={py} place {"." * x + piece[py]}')
        debug(f'gy={gy}  onto {"".join(grid[gy])}')
        for px in range(DIM):
            gx = px + x
            if gx >= len(grid[y]):
                if piece[py][px] == ".":
                    continue
                raise ValueError("cannot place")
            if grid[gy][gx] == "." and piece[py][px] == "#":
                grid[gy][gx] = "#"
        debug(f'           {"".join(grid[gy])}')
    return True


def one(jets):
    # start at least 3 tall
    grid = [["."] * 7 for _ in range(3)]
    tallest = 0
    jet_idx = 0
    start = time.process_time_ns()
    for i in range(2022):
        piece = pieces[i % len(pieces)]
        x, y = 2, tallest + 3
        while True:
            # blow
            move = jets[jet_idx % len(jets)]
            jet_idx += 1
            if move == "<" and can_place(grid, piece, x - 1, y):
                x -= 1
            elif move == ">" and can_place(grid, piece, x + 1, y):
                x += 1
            # fall
            debug("tick")
            if not can_place(grid, piece, x, y - 1):
                debug(f"at rest {x} {y}")
                break
            y -= 1
        place(grid, piece, x, y)
        display(grid)
        for i, row in enumerate(reversed(grid)):
            if any(r == "#" for r in row):
                tallest = len(grid) - i
                break
    elapsed = (time.process_time_ns() - start) / 1_000_000
    print(f'{elapsed:.1f}ms')
    print(tallest)


def display(grid):
    debug("+-------+")
    for row in reversed(grid):
        debug("|" + "".join(row) + "|")
    debug("+-------+")
    debug("")


def two(jets):
    pass


def input():
    return sys.stdin.readline().strip()


def main(jets):
    one(deepcopy(jets))
    two(jets)


if __name__ == "__main__":
    main(input())
