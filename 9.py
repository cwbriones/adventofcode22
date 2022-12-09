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


def one(moves):
    hx, hy = 0, 0
    tx, ty = 0, 0

    positions = set()
    deltas = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0)}
    for move, amt in moves:
        dx, dy = deltas[move]
        for _ in range(amt):
            # move head
            hx += dx
            hy += dy
            # move tail to where the head was
            if abs(hx - tx) > 1 or abs(hy - ty) > 1:
                tx, ty = hx - dx, hy - dy
            positions.add((tx, ty))
            # show((hx, hy), (tx, ty))
    print(len(positions))

def show(hp, tp):
    (hx, hy), (tx, ty) = hp, tp
    grid = [['.' for _ in range(6)] for _ in range(5)]
    grid[4][0] = 's'
    grid[4 + ty][tx] = 'T'
    grid[4 + hy][hx] = 'H'

    print(f'h=({hx}, {hy}) t=({tx}, {ty})')
    for row in grid:
        print(''.join(row))
    print()


def two(lines):
    print("two")


def input():
    moves = []
    for line in sys.stdin.readlines():
        move, amt = line.strip().split(' ')
        moves.append((move, int(amt)))
    return moves


def main(lines):
    one(lines)
    two(lines)


if __name__ == "__main__":
    main(input())
