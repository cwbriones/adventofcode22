from collections import deque
from typing import TypeVar, Callable, Iterable, Protocol

T = TypeVar('T')

Point = tuple[int, int]

def single_step(x, y):
    return [(x - 1, y), (x + 1, y), (x, y + 1), (x, y - 1)]

def ucs(
    graph: list[list[T]],
    start: Point,
    end: Point,
    connected: Callable[[T, T], bool],
    neighbors: Callable[[int, int], Iterable[Point]] = single_step,
):
    fringe: 'deque[tuple[tuple[int, int], int]]' = deque([(start, 0)])
    visited = set()
    ny = len(graph)
    nx = len(graph[0])

    while fringe:
        p, total = fringe.popleft()
        if p in visited:
            continue
        if p == end:
            return total
        visited.add(p)
        x, y = p
        h = graph[y][x]
        for qx, qy in neighbors(x, y):
            if qx >= nx or qx < 0:
                continue
            if qy >= ny or qy < 0:
                continue
            if not connected(h, graph[qy][qx]):
                continue
            q = (qx, qy)
            fringe.append((q, total + 1))
    return None

class Graph(Protocol):
    pass

class Grid:
    def __init__(self, grid, connected):
        self.grid = grid
        self.ny = len(self.grid)
        self.nx = len(self.grid[0])
        self.connected = connected

    def vertices(self):
        for j, row in enumerate(self.grid):
            for i, h in enumerate(row):
                yield i, j, h

    def neighbors(self, p):
        x, y, h = p
        for qx, qy in single_step(x, y):
            if qx >= self.nx or qx < 0:
                continue
            if qy >= self.ny or qy < 0:
                continue
            if not self.connected(h, self.grid[qy][qx]):
                continue
            yield qx, qy


def generic(
    graph: list[list[T]],
    start: Point,
    end: Point,
    connected: Callable[[T, T], bool],
):
    fringe: 'deque[tuple[tuple[int, int], int]]' = deque([(start, 0)])
    visited = set()
    ny = len(graph)
    nx = len(graph[0])

    while fringe:
        p, total = fringe.popleft()
        if p in visited:
            continue
        if p == end:
            return total
        visited.add(p)
        x, y = p
        h = graph[y][x]
        for qx, qy in neighbors(x, y):
            if qx >= nx or qx < 0:
                continue
            if qy >= ny or qy < 0:
                continue
            if not connected(h, graph[qy][qx]):
                continue
            q = (qx, qy)
            fringe.append((q, total + 1))
    return None
