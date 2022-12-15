import argparse
from collections import (
    defaultdict,
    deque,
)
from itertools import chain
from contextlib import contextmanager
from dataclasses import dataclass
import functools
import math
import os
import sys
from copy import deepcopy
import re

PAT = re.compile(r"at x=(-?\d+), y=(-?\d+)")


def manhattan(p, q):
    return abs(p[1] - q[1]) + abs(p[0] - q[0])

def scan_fixed_x(sensors, check):
    return scan_fixed(sensors, check, selector=lambda p: p)

def scan_fixed_y(sensors, check):
    return scan_fixed(sensors, check, selector=lambda p: (p[1], p[0]))

def scan_fixed(sensors, check, selector):
    ranges = []
    for sensor, best in sensors.items():
        fst, snd = selector(sensor)
        delta = best - abs(fst - check)
        if delta < 0:
            # we can't learn anything from this sensor
            continue
        # anything at most deltax away cannot possibly have a beacon
        start, end = snd - delta, snd + delta
        if start > end:
            raise ValueError("wat")
        ranges.append((start, end))
    ranges.sort(key=lambda p: p[0])
    return merge(ranges)

def complement(ranges, low, high):
    possible = []
    lastend = low
    for start, end in ranges:
        if start > lastend:
            possible.append((lastend, start - 1))
        lastend = end + 1
    if lastend < high:
        possible.append((lastend, high))
    return possible

def one(sensors, ycheck):
    best = {s: manhattan(s, sensors[s]) for s in sensors}
    in_row = sum(
        1
        for _, by in set(sensors.values())
        if by == ycheck
    )
    ranges = scan_fixed_y(best, ycheck)
    not_possible = sum(b - a + 1 for (a, b) in ranges) - in_row
    print(not_possible)

def two(sensors, ycheck):
    best = {s: manhattan(s, sensors[s]) for s in sensors}
    score = lambda y: sum(abs(s[1] - y) for s in best if abs(s[1] - y) > 0)

    # find the min score in the y direction
    minscore = float('inf')
    lo, hi = 0, ycheck*2
    while lo < hi:
        mid = (lo + hi) // 2
        if score(mid) < score(mid + 1):
            hi = mid
        else:
            lo = mid + 1
    y = lo

    while True:
        curscore = score(y-1)
        if curscore <= minscore:
            minscore = curscore
            y -= 1
        else:
            break

    # search the space from here onward
    while y < ycheck*2:
        # print(f'==== y={y} ====')
        ranges = scan_fixed_y(best, y)
        possible = complement(ranges, 0, ycheck*2)
        if possible:
            x = possible[0][0]
            print(f'x={x} y={y} {score(y)}')
            print(4000000*x + y)
            break
        y += 1

def merge(ranges):
    assert len(ranges) > 0
    merged = [list(ranges[0])]
    for start, end in ranges[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
            continue
        merged.append([start, end])
    return merged

def dims(coords) -> tuple[int, int, int, int] | None:
    coorditer = iter(coords)
    try:
        minx, miny = next(coorditer)
        maxx, maxy = minx, miny
        for x, y in coorditer:
            minx = min(x, minx)
            miny = min(y, miny)
            maxx = max(x, maxx)
            maxy = max(y, maxy)
    except StopIteration:
        return None
    return minx, maxx, miny, maxy


def input():
    lines = [l.strip() for l in sys.stdin.readlines()]
    ycheck = 2_000_000
    try:
        ycheck = int(lines[0])
        lines = lines[1:]
    except ValueError:
        pass

    sensors = {}
    for line in lines:
        sensor, beacon = tuple(
            (int(m.group(1)), int(m.group(2)))
            for m in PAT.finditer(line.strip())
        )
        sensors[sensor] = beacon
    return sensors, ycheck


def main(sensors, ycheck):
    one(sensors, ycheck)
    two(sensors, ycheck)


if __name__ == "__main__":
    sensors, ycheck = input()
    main(sensors, ycheck)
