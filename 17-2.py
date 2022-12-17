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
GRID_WIDTH = 7

if os.environ.get("DEBUG"):

    def debug(msg):
        print("[DEBUG]: ", end="", file=sys.stderr)
        print(msg, file=sys.stderr)

else:

    def debug(msg):
        pass


# Each piece is 4 wide and 4 tall
def can_place(grid, piece, x, y):
    if y < 0 or x < 0 or x >= GRID_WIDTH:
        return False
    while len(grid) < y + DIM:
        grid.append(0)

    #    ....
    #    ....
    #    ####
    #    ^
    #    coord
    for py in reversed(range(DIM)):
        gy = y + (DIM - 1 - py)
        for px in range(DIM):
            gx = px + x
            if gx >= GRID_WIDTH:
                if piece[py] & (1 << (DIM - 1 - px)) == 0:
                    continue
                return False
            if grid[gy] & (1 << GRID_WIDTH - 1 - gx) > 0 and piece[py] & (1 << (DIM - 1 - px)) > 0:
                return False
    return True


def place(grid, piece, x, y):
    for py in reversed(range(DIM)):
        gy = y + (DIM - 1 - py)
        # debug(f'py={py} place {"." * x + int_to_str(piece[py], DIM)}')
        # debug(f'gy={gy}  onto {int_to_str(grid[gy], GRID_WIDTH)}')
        for px in range(DIM):
            gx = px + x
            if gx >= GRID_WIDTH:
                if piece[py] & (1 << (DIM - 1 - px)) == 0:
                    continue
                raise ValueError("cannot place")
            mask = ((piece[py] << 3) >> x)
            grid[gy] |= mask
            # if grid[gy] & (1 << (GRID_WIDTH - 1 - gx)) == 0 and piece[py] & (1 << (DIM - 1 - px)) == 1:
            #     grid[gy] |= (1 << (GRID_WIDTH - 1 - gx))
        # debug(f'           {int_to_str(grid[gy], GRID_WIDTH)}')
    return True

def int_to_str(value, width):
    out = []
    for i in range(width):
        mask = 1 << (width - i - 1)
        if mask & value > 0:
            out.append('#')
        else:
            out.append('.')
    return ''.join(out)

def intpiece(piece: list[str]) -> list[int]:
    vals = []
    for row in piece:
        n = 0
        for shift, c in enumerate(reversed(row)):
            if c == '#':
                n += 1 << shift
        vals.append(n)
    return vals

def one(jets):
    # start at least 3 tall
    grid = [0 for _ in range(3)]
    tallest = 0
    jet_idx = 0
    start = time.process_time_ns()

    intpieces = [intpiece(p) for p in pieces]
    print(intpieces)
    for i in range(2022):
        piece = intpieces[i % len(pieces)]
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
            if row > 0:
                tallest = len(grid) - i
                break
    elapsed = (time.process_time_ns() - start) / 1_000_000
    print(f'{elapsed:.1f}ms')
    print(tallest)


def display(grid):
    pass
    # debug("+-------+")
    # for row in reversed(grid):
    #     debug("|" + int_to_str(row, GRID_WIDTH) + "|")
    # debug("+-------+")
    # debug("")


def two(jets):
    pass


def input():
    return sys.stdin.readline().strip()


def main(jets):
    one(deepcopy(jets))
    two(jets)


if __name__ == "__main__":
    main(input())
