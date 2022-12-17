import sys
import re

Point = tuple[int, int]


def one(beacons, ycheck):
    """
    For part one, we take all scanner/beacon pairs. Knowing the y coordinate to
    check, we keep the x-delta fixed such that the manhattan distance is no closer
    than that sensors beacon (otherwise it would be the closest). This gives us
    an interval where the beacon *definitely isn't*.

    Once we have these intervals, they are sorted and collapsed into a set of
    non-overlapping intervals. We can then simply sum the lengths of all of these
    intervals for the answer.
    """
    best = {s: manhattan(s, beacons[s]) for s in beacons}
    in_row = sum(1 for _, by in set(sensors.values()) if by == ycheck)
    ranges = scan_fixed_y(best, ycheck)
    not_possible = sum(b - a + 1 for (a, b) in ranges) - in_row
    print(not_possible)


def manhattan(p: Point, q: Point) -> int:
    return abs(p[1] - q[1]) + abs(p[0] - q[0])


def scan_fixed_y(sensors, check):
    ranges = []
    for sensor, best in sensors.items():
        x, y = sensor
        deltax = best - abs(y - check)
        if deltax < 0:
            # we can't learn anything from this sensor
            continue
        # anything at most deltax away cannot possibly have a beacon
        start, end = x - deltax, x + deltax
        if start > end:
            raise ValueError("wat")
        ranges.append((start, end))
    ranges.sort(key=lambda p: p[0])
    return merge(ranges)


def merge(ranges):
    assert len(ranges) > 0
    merged = [list(ranges[0])]
    for start, end in ranges[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
            continue
        merged.append([start, end])
    return merged


def two(beacons: dict[tuple[int, int], tuple[int, int]]):
    """
    For part two, we exploit the fact that the solution is unique.

    This means the position is nestled between two pairs of sensors. If you
    think of all the spaces less than or equal to each sensors best manhattan
    distance, you get a diamond. Each diamond side has slope 1 or -1.

    Since we know the point is between each pair, one of the pairs consists
    of two sides of these diamonds with slope 1, the other pair with slope -1.

    We iterate through all pairs of sensors, checking if their sides are apart
    by exactly 2 spaces. If so, we keep that pair in a set of m=-1 and m=1.

    Finally, we check all of these lines for an intersection - there should be
    exactly one that fulfills the criteria of not being seen by any sensor.
    """
    sensors = {s: manhattan(s, beacons[s]) for s in beacons}

    matches_up = set()
    matches_down = set()
    for sensora, sensorb in pairs(list(sensors)):
        a1, b1, c1, d1 = diamonds(sensora, sensors[sensora])
        a2, b2, c2, d2 = diamonds(sensorb, sensors[sensorb])
        if (m := midpoint(a1, b2)) is not None:
            matches_up.add(m)
        elif (m := midpoint(b1, a2)) is not None:
            matches_up.add(m)
        elif (m := midpoint(c1, d2)) is not None:
            matches_down.add(m)
        elif (m := midpoint(d1, c2)) is not None:
            matches_down.add(m)
    candidates = intersections(matches_up, matches_down)
    points = [
        p for p in candidates if all(manhattan(s, p) > b for s, b in sensors.items())
    ]
    if len(points) != 1:
        print("no solution found? possibly bad input")
        return
    ((x, y),) = points
    print(x * 4000000 + y)


def diamonds(sensor: Point, best: int):
    #      / \
    #   a /   \ c
    #    /  .  \
    #    \     /
    #   d \   / b
    #      \ /
    a = y_intercept(x=sensor[0], y=sensor[1] + best)
    b = y_intercept(x=sensor[0], y=sensor[1] - best)
    c = y_intercept(x=sensor[0], y=sensor[1] + best, m=-1)
    d = y_intercept(x=sensor[0], y=sensor[1] - best, m=-1)
    return a, b, c, d


def midpoint(a, b):
    if abs(a - b) != 2:
        return None
    elif a < b:
        return a + 1
    else:
        return b + 1


def y_intercept(x, y, m=1):
    return y - x * m


def pairs(items):
    for i, item in enumerate(items):
        for other in items[i + 1 :]:
            yield item, other


def intersections(lines_up, lines_down):
    # find where x1 == x2 and y1 == y2
    # y =   x + up
    # y = - x + down
    # y = (up + down) / 2
    for up in lines_up:
        for down in lines_down:
            y = (up + down) // 2
            x = y - up
            yield (x, y)


def input():
    PAT = re.compile(r"at x=(-?\d+), y=(-?\d+)")
    ycheck = 2_000_000

    lines = [l.strip() for l in sys.stdin.readlines()]
    try:
        ycheck = int(lines[0])
        lines = lines[1:]
    except ValueError:
        pass

    sensors = {}
    for line in lines:
        sensor, beacon = tuple(
            (int(m.group(1)), int(m.group(2))) for m in PAT.finditer(line.strip())
        )
        sensors[sensor] = beacon
    return sensors, ycheck


def main(sensors, ycheck):
    one(sensors, ycheck)
    two(sensors)


if __name__ == "__main__":
    sensors, ycheck = input()
    main(sensors, ycheck)
