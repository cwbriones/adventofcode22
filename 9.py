import sys


def one(moves):
    solve(moves, 2)


def two(moves):
    solve(moves, 10)


def solve(moves, segments):
    rope = [(0, 0) for _ in range(segments)]

    positions = set()
    deltas = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}
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
        # show(rope, positions)
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


def show(rope, positions):
    syms = [str(i) for i in range(len(rope))]
    syms[0] = "H"
    if len(syms) == 2:
        syms[1] = "T"

    ox, oy = 11, 15
    grid = [["." for _ in range(26)] for _ in range(21)]
    grid[oy][ox] = "s"
    syms = syms[::-1]
    for x, y in positions:
        grid[oy + y][ox + x] = "#"

    for i, (x, y) in enumerate(reversed(rope)):
        grid[oy + y][ox + x] = syms[i]

    print()
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
