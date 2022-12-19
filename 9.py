import sys


def one(moves):
    solve(moves, 2)


def two(moves):
    solve(moves, 10)


def solve(moves, segments, debug=False):
    rope = [(0, 0) for _ in range(segments)]

    positions = set()
    deltas = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}
    history = []
    for move, amt in moves:
        delta = deltas[move]
        for _ in range(amt):
            # move head
            rope[0] = addpos(rope[0], delta)

            # move everything else
            i = 1
            while i < len(rope) and too_far(rope[i], rope[i - 1]):
                rope[i] = follow(rope[i], rope[i - 1])
                i += 1
            positions.add(rope[-1])
        history.append(list(rope))
    if debug:
        show(moves, history)
    print(len(positions))


def too_far(p, q):
    return abs(p[0] - q[0]) > 1 or abs(p[1] - q[1]) > 1


def follow(p, leader):
    dx, dy = leader[0] - p[0], leader[1] - p[1]
    if abs(dx) == 2 and abs(dy) == 1:
        return addpos(p, (dx // 2, dy))
    if abs(dy) == 2 and abs(dx) == 1:
        return addpos(p, (dx, dy // 2))
    return addpos(p, (dx // 2, dy // 2))


def addpos(pos, d):
    return (pos[0] + d[0], pos[1] + d[1])


def show(moves, history):
    syms = [str(i) for i in range(len(history[0]))]
    syms[0] = "H"
    if len(syms) == 2:
        syms[1] = "T"
    syms = syms[::-1]

    minx, maxx, miny, maxy = 0, 0, 0, 0
    for step in history:
        for x, y in step:
            minx = min(x, minx)
            maxx = max(x, maxx)
            miny = min(y, miny)
            maxy = max(y, maxy)
    width = maxx - minx + 1
    height = maxy - miny + 1

    ox, oy = -minx, -miny
    for (move, amt), rope in zip(moves, history):
        grid = [["." for _ in range(width)] for _ in range(height)]
        grid[oy][ox] = "s"
        # for x, y in visited:
        #     grid[oy + y][ox + x] = "#"

        for i, (x, y) in enumerate(reversed(rope)):
            grid[oy + y][ox + x] = syms[i]

        print(f"== {move} {amt} ==")
        for row in grid:
            print("".join(row))
        print()


def input():
    moves = []
    for line in sys.stdin.readlines():
        move, amt = line.strip().split(" ")
        moves.append((move, int(amt)))
    return moves


def main(lines):
    one(lines)
    two(lines)


if __name__ == "__main__":
    main(input())
