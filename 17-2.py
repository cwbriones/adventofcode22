import os
import sys
from collections import defaultdict

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
        mask = (piece[py] << 3) >> x
        if (mask & grid[gy]) > 0:
            return False
        for px in range(DIM):
            gx = px + x
            if gx >= GRID_WIDTH:
                if piece[py] & (1 << (DIM - 1 - px)) == 0:
                    continue
                return False
            if (
                grid[gy] & (1 << GRID_WIDTH - 1 - gx) > 0
                and piece[py] & (1 << (DIM - 1 - px)) > 0
            ):
                return False
    return True


def place(grid, piece, x, y):
    for py in reversed(range(DIM)):
        gy = y + (DIM - 1 - py)
        mask = (piece[py] << 3) >> x
        grid[gy] |= mask
    return True


def int_to_str(value, width):
    out = []
    for i in range(width):
        mask = 1 << (width - i - 1)
        if mask & value > 0:
            out.append("#")
        else:
            out.append(".")
    return "".join(out)


def intpiece(piece: list[str]) -> list[int]:
    vals = []
    for row in piece:
        n = 0
        for shift, c in enumerate(reversed(row)):
            if c == "#":
                n += 1 << shift
        vals.append(n)
    return vals


def one(jets):
    print(run(jets, iterations=2022))


def run(jets, iterations, f=None):
    grid = [0 for _ in range(3)]
    height = 0
    jet_idx = 0

    intpieces = [intpiece(p) for p in pieces]
    for i in range(iterations):
        pidx = i % len(intpieces)

        piece = intpieces[pidx]
        x, y = 2, height + 3

        if f is not None:
            f(i, pidx, jet_idx, height)
        while True:
            # blow
            move = jets[jet_idx]
            jet_idx = (jet_idx + 1) % len(jets)
            if move == "<" and can_place(grid, piece, x - 1, y):
                x -= 1
            elif move == ">" and can_place(grid, piece, x + 1, y):
                x += 1
            # fall
            if not can_place(grid, piece, x, y - 1):
                break
            y -= 1
        place(grid, piece, x, y)
        display(grid)
        for i, row in enumerate(reversed(grid)):
            if row > 0:
                height = len(grid) - i
                break
    return height


def display(grid):
    pass
    # debug("+-------+")
    # for row in reversed(grid):
    #     debug("|" + int_to_str(row, GRID_WIDTH) + "|")
    # debug("+-------+")
    # debug("")


def two(jets):
    n = 1000000000000
    start, length, delta = find_cycle(jets)

    # capture the heights at each part of the cycle
    heights = []
    def capture(i, pidx, jet_idx, height):
        heights.append(height)
    run(jets, iterations=start + length, f=capture)

    # We know
    # - when the cycle starts
    # - how much it grows with each iteration
    # - how much it grows relative to the start within each iteration

    # Compute how many full cycles elapse and find out how far we are
    # into the final cycle
    num_cycles = (n - start) // length
    excess = (n - start) % length

    # Add on the accumulated height of every complete cycle, plus
    # the amount gained from the partial final cycle.
    total = heights[start] + delta * num_cycles
    total += heights[start + excess] - heights[start]
    print(total)


def find_cycle(jets):
    """
    Finds a cycle in the growth pattern.

    A minimum condition for a cycle to occur is that the current piece
    and current jet must be the same. Build a map of every time the
    jet and piece occur and the first time they repeat.

    Once we find the first repeat, we store the height every time this
    jet/piece pair occurs. From that we can compute the minimum cycle
    length by finding when the difference in heights recur. This is
    done in quadratic time but this should be okay because the list should
    be somewhat sparse.

    Finally, the cycle length is determined by taking the minimum repeating
    height growth (the other entries represent cycle multiples).
    """
    seen = defaultdict(list)
    cycle_key = None

    def _find_cycle(i, pidx, jet_idx, height):
        nonlocal cycle_key
        key = (pidx, jet_idx)
        if key in seen and cycle_key is None:
            cycle_key = key
            seen[key].append((i, height))
        elif cycle_key is None or key == cycle_key:
            seen[key].append((i, height))

    run(jets, iterations=10000, f=_find_cycle)

    # Find the cycle length and delta
    heights = seen[cycle_key]
    distances = dict()
    # fixme: does this have to be quadratic?
    # clearly from the actual input, it is possible for a piece/jet combo
    # to recur without the cycle starting
    for hi, (i, h1) in enumerate(heights):
        for j, h2 in heights[hi + 1 :]:
            if h2 - h1 not in distances:
                distances[h2 - h1] = j - 1
            distances[h2 - h1] = min(distances[h2 - h1], j - i)
    indices = {i for i, _ in heights}
    delta = min(distances)
    cycle = distances[delta]
    for i, _ in heights:
        if i + cycle in indices:
            return i, cycle, delta
    raise ValueError("no cycle found?")


def input():
    return sys.stdin.readline().strip()


def main(jets):
    one(jets)
    two(jets)


if __name__ == "__main__":
    main(input())
