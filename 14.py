from dataclasses import dataclass, field
import sys
from copy import deepcopy

from contextlib import contextmanager
import cProfile
import pstats
from pstats import SortKey

@dataclass
class Grid:
    maxy: int
    part_two: bool
    walls: set[tuple[int, int]] = field(default_factory=set)
    placed: set[tuple[int, int]] = field(default_factory=set)

    @classmethod
    def from_paths(cls, paths, part_two=False):
        maxy = 0
        for path in paths:
            for x, y in path:
                maxy = max(maxy, y)
        walls = set()
        for path in paths:
            for start, end in zip(path, path[1:]):
                for x, y in line(start, end):
                    walls.add((x, y))
        if part_two:
            maxy += 2
        return Grid(maxy, part_two, walls=walls)

    def peek(self, x, y, dx=0, dy=0):
        q = (x + dx, y + dy)
        if q in self.walls:
            return '#'
        elif q in self.placed:
            return 'o'
        elif self.part_two and y + dy == self.maxy:
            # infinite wall
            return '#'
        return '.'

    def place(self, p: tuple[int, int]):
        self.placed.add(p)

    def add_piece(self):
        x, y = 500, 0
        # fall until we hit something
        while True:
            oldy = y
            while y < self.maxy and self.peek(x, y, dy=1) == '.':
                y += 1
            if y < self.maxy and self.peek(x, y, dx=-1, dy=1) == '.':
                # try left
                x -= 1
                y += 1
            elif y < self.maxy and self.peek(x, y, dx=1, dy=1) == '.':
                # try right
                x += 1
                y += 1
            if oldy != y:
                # successfully moved, keep falling
                continue
            space = self.peek(x, y, 0, 0)
            if space == '.' and y < self.maxy:
                self.place((x, y))
                return True
            return False


def one(paths):
    grid = Grid.from_paths(paths)
    c = 0
    while True:
        if not grid.add_piece():
            print(c)
            break
        c += 1


def two(paths):
    grid = Grid.from_paths(paths, part_two=True)
    c = 0

    with profiled(stream=sys.stderr):
        while True:
            if not grid.add_piece():
                print(c)
                break
            c += 1

@contextmanager
def profiled(stream, sortby=SortKey.CUMULATIVE):
    pr = cProfile.Profile()
    pr.enable()
    yield
    pr.disable()
    ps = pstats.Stats(pr, stream=stream).sort_stats(sortby)
    ps.print_stats()


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
