import argparse
from collections import (
    defaultdict,
    deque,
)
from contextlib import contextmanager
from dataclasses import dataclass
import functools
import math
import os
import sys
from copy import deepcopy

@dataclass
class Grid:
    minx: int
    maxx: int
    miny: int
    maxy: int
    grid: list[list[str]]

    def draw(self):
        self.grid[0][500 - self.minx] = "+"
        for row in self.grid:
            print("".join(row))
        self.grid[0][500 - self.minx] = "."


    @classmethod
    def from_paths(cls, paths):
        minx, maxx, miny, maxy = 100000, 0, 0, 0
        for path in paths:
            for x, y in path:
                minx = min(minx, x)
                maxx = max(maxx, x)
                miny = min(miny, y)
                maxy = max(maxy, y)
        minx -= 1
        maxx += 1

        grid = [["." for _ in range(minx, maxx + 1)] for _ in range(miny, maxy + 1)]
        for path in paths:
            for start, end in zip(path, path[1:]):
                for x, y in line(start, end):
                    grid[y - miny][x - minx] = "#"
        return Grid(minx, maxx, miny, maxy, grid)

    def peek(self, p, dx=0, dy=0):
        x, y = p
        x += dx
        y += dy
        if x < self.minx or x > self.maxx:
            return None
        if y < self.miny or y > self.maxy:
            return None
        return self.grid[y - self.miny][x - self.minx]

    def place(self, p):
        x, y = p
        self.grid[y - self.miny][x - self.minx] = 'o'

    def add_piece(self):
        pos = [500, 0]
        # fall until we hit something
        while True:
            oldpos = [pos[0], pos[1]]
            while self.peek(pos, dy=1) == '.':
                pos[1] += 1
            # try left
            if self.peek(pos, dx=-1, dy=1) == '.':
                pos[0] -= 1
                pos[1] += 1
            elif self.peek(pos, dx=1, dy=1) == '.':
                pos[0] += 1
                pos[1] += 1
            if pos == oldpos:
                self.place(pos)
                return self.falls_forever(pos)

    def falls_forever(self, pos):
        return pos[1] == self.maxy


if os.environ.get("DEBUG"):

    def debug(msg):
        print("[DEBUG]: ", end="", file=sys.stderr)
        print(msg, file=sys.stderr)

else:

    def debug(msg):
        pass


def one(paths):
    grid = Grid.from_paths(paths)
    c = 0
    while True:
        done = grid.add_piece()
        if done:
            break
        c += 1
    grid.draw()
    print(c)


def two(paths):
    pass

def line(start, end):
    assert start[0] == end[0] or start[1] == end[1]
    if (dx := sign(end[0] - start[0])) != 0:
        x = start[0]
        while x != end[0]:
            yield (x, start[1])
            x += dx
        yield (x, start[1])
    elif (dy := sign(end[1] - start[1])) != 0:
        y = start[1]
        while y != end[1]:
            yield (start[0], y)
            y += dy
        yield (start[0], y)


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    return 0


def input():
    lines = (line.strip() for line in sys.stdin.readlines())
    paths = []
    for line in lines:
        path = [[int(x) for x in pair.split(",")] for pair in line.split(" -> ")]
        paths.append(path)
    return paths


def main(lines):
    one(deepcopy(lines))
    two(lines)


if __name__ == "__main__":
    main(input())
