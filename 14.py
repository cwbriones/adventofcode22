import argparse
from collections import (
    defaultdict,
    deque,
)
from contextlib import contextmanager
from dataclasses import dataclass, field
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
    # grid: list[list[str]]

    walls: set[tuple[int, int]] = field(default_factory=set)
    placed: set[tuple[int, int]] = field(default_factory=set)

    # def draw(self):
    #     self.grid[0][500 - self.minx] = "+"
    #     for row in self.grid:
    #         print("".join(row))
    #     self.grid[0][500 - self.minx] = "."


    @classmethod
    def from_paths(cls, paths):
        minx, maxx, miny, maxy = 100000, 0, 0, 0
        for path in paths:
            for x, y in path:
                minx = min(minx, x)
                maxx = max(maxx, x)
                miny = min(miny, y)
                maxy = max(maxy, y)
        # grid = [["." for _ in range(minx, maxx + 1)] for _ in range(miny, maxy + 1)]
        walls = set()
        for path in paths:
            for start, end in zip(path, path[1:]):
                walls.add(tuple(start))
                walls.add(tuple(end))
                for x, y in line(start, end):
                    # grid[y - miny][x - minx] = "#"
                    walls.add((x, y))
        # grid.append(['.' for _ in grid[0]])
        # grid.append(['#' for _ in grid[0]])
        return Grid(minx, maxx, miny, maxy, walls=walls)

    def peek(self, p, dx=0, dy=0):
        x, y = p
        x += dx
        y += dy
        q = (x, y)
        if q in self.walls:
            return '#'
        elif q in self.placed:
            return 'o'
        if y == self.maxy + 2:
            # infinite wall
            return '#'
        return '.'

    def place(self, p: tuple[int, int]):
        self.placed.add(p)

    def add_piece(self):
        pos = [500, 0]
        # fall until we hit something
        while True:
            oldpos = [pos[0], pos[1]]
            while self.peek(pos, dy=1) == '.':
                pos[1] += 1
            if self.peek(pos, dx=-1, dy=1) == '.':
                # try left
                pos[0] -= 1
                pos[1] += 1
            elif self.peek(pos, dx=1, dy=1) == '.':
                # try right
                pos[0] += 1
                pos[1] += 1
            if pos != oldpos:
                # successfully moved, keep falling
                continue
            space = self.peek(pos, 0, 0)
            if space == '.':
                self.place(tuple(pos))
                return True
            return False

    def can_place(self, pos):
        return pos[1] == self.maxy


if os.environ.get("DEBUG"):

    def debug(msg):
        print("[DEBUG]: ", end="", file=sys.stderr)
        print(msg, file=sys.stderr)

else:

    def debug(msg):
        pass


# def one(paths):
#     grid = Grid.from_paths(paths)
#     c = 0
#     while True:
#         done = grid.add_piece()
#         if done:
#             break
#         c += 1
#     print(c)
#     print(len(grid.placed))


def two(paths):
    grid = Grid.from_paths(paths)
    c = 0
    while True:
        if not grid.add_piece():
            print(c)
            break
        c += 1

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
    # one(deepcopy(lines))
    two(lines)


if __name__ == "__main__":
    main(input())
