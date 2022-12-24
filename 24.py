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


def one(board):
    x = board[0].index('.')
    y = 0

    xtarget = board[-1].index('.')
    xblizz, yblizz = extract(board)

    xcache = [set(p for (p, _) in xblizz)]
    width = len(board[1]) - 2
    print(width)
    for _ in range(width - 1):
        xblizz = advance(board, xblizz)
        xcache.append(set(p for (p, _) in xblizz))
    print(len(xcache))

    ycache = [set(p for (p, _) in yblizz)]
    height = len(board) - 2
    for _ in range(height - 1):
        yblizz = advance(board, yblizz)
        ycache.append(set(p for (p, _) in yblizz))
    print(height)
    print(len(ycache))

    period = math.lcm(width, height)
    print(f"board is {width}x{height}: {period}")

    search: deque[tuple[tuple[int, int, int], int]] = deque([((x, y, 0), 0)])
    visited = set()
    print(period)
    while search:
        p, t = search.popleft()
        if p in visited:
            continue
        if p[0] == xtarget and p[1] == len(board) - 1:
            print('done')
            print(p, t)
            break
        visited.add(p)
        # Try to move
        x, y, z = p
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx = x + dx
            ny = y + dy
            if board[ny][nx] == '#':
                continue
            if (nx, ny) in xcache[(z + 1) % len(xcache)]:
                continue
            if (nx, ny) in ycache[(z + 1) % len(ycache)]:
                continue
            search.append(((nx, ny, (z + 1) % period), t + 1))
        # Try to wait
        # "cannot share a position with a blizzard"
        if (x, y) in xcache[(z + 1) % len(xcache)]:
            continue
        if (x, y) in ycache[(z + 1) % len(ycache)]:
            continue
        search.append(((x, y, (z + 1) % period), t + 1))

Pair = tuple[int, int]

def advance(board, blizzards: list[tuple[Pair, Pair]]) -> list[tuple[Pair, Pair]]:
    newblizz = []
    for ((x, y), (dx, dy)) in blizzards:
        nx = (x + dx) % len(board[0])
        ny = (y + dy) % len(board)
        while board[ny][nx] == '#':
            nx = (nx + dx) % len(board[0])
            ny = (ny + dy) % len(board)
        newblizz.append(((nx, ny), (dx, dy)))
    return newblizz

def two(board):
    pass

def extract(board):
    x_blizzards = []
    y_blizzards = []
    for y, row in enumerate(board):
        for x, c in enumerate(row):
            if c == '^':
                y_blizzards.append(((x, y), (0, -1)))
            elif c == 'v':
                y_blizzards.append(((x, y), (0, 1)))
            elif c == '<':
                x_blizzards.append(((x, y), (-1, 0)))
            elif c == '>':
                x_blizzards.append(((x, y), (1, 0)))
    for (x, y), _ in x_blizzards:
        board[y][x] = '.'
    for (x, y), _ in y_blizzards:
        board[y][x] = '.'
    return x_blizzards, y_blizzards


def input():
    return [list(line.strip()) for line in sys.stdin.readlines()]


if __name__ == "__main__":
    lines = input()
    one(deepcopy(lines))
    two(lines)
