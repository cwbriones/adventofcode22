import math
import sys
import re
from enum import IntEnum
from typing import Sequence

_DELTAS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

class Dir(IntEnum):
    R = 0
    D = 1
    L = 2
    U = 3

    def delta(self):
        return _DELTAS[self]

    def turn_right(self):
        return Dir((self + 1) % 4)

    def turn_left(self):
        return Dir((self - 1) % 4)

def one(board: Sequence[str], path: Sequence[int | str]):
    output = [list(row) for row in board]
    x = board[0].find('.')
    y = 0
    width, height = len(board[0]), len(board)

    # left <-  -> right
    syms = '>v<^'
    di = Dir.R
    output[y][x] = '>'
    for move in path:
        if isinstance(move, str):
            if move == 'R':
                di = di.turn_right()
            elif move == 'L':
                di = di.turn_left()
            continue
        output[y][x] = syms[di]
        dx, dy = di.delta()
        for _ in range(move):
            x2 = (x + dx) % width
            y2 = (y + dy) % height
            while board[y2][x2] == ' ':
                x2 = (x2 + dx) % width
                y2 = (y2 + dy) % height
            if board[y2][x2] == '#':
                break
            x, y = x2, y2
            output[y][x] = syms[di]
    print(1000*(y+1) + 4*(x+1) + di)

def build_facemap(board: Sequence[str]):
    width = len(board[0])
    height = len(board)
    sidedim = math.gcd(width, height)

    f = 0
    faces = 'abcdef'
    face_by_name = {}
    for y in range(0, height, sidedim):
        for x in range(0, width, sidedim):
            if board[y][x] == ' ':
                continue
            face_by_name[faces[f]] = (x, y)
            f += 1
    collapsed = [[' '] * (width // sidedim) for _ in range(height // sidedim)]
    for name, (x, y) in face_by_name.items():
        collapsed[y // sidedim][x // sidedim] = name
    print()
    for row in collapsed:
        print(''.join(row))
    print()
    return face_by_name, sidedim

def two(board: Sequence[str], path: Sequence[int | str]):
    facemap, sidedim = build_facemap(board)
    output = [list(row) for row in board]
    x = board[0].find('.')
    y = 0
    width, height = len(board[0]), len(board)

    # left <-  -> right
    syms = '>v<^'
    curdir = Dir.R
    output[y][x] = '>'

    face = 'a'
    for move in path:
        # turn
        if isinstance(move, str):
            if move == 'R':
                curdir = curdir.turn_right()
            elif move == 'L':
                curdir = curdir.turn_left()
            continue
        output[y][x] = syms[curdir]
        # move
        for _ in range(move):
            dx, dy = curdir.delta()
            x2 = x + dx
            y2 = y + dy
            dir2 = curdir
            if (x2 < 0 or y2 < 0 or x2 >= width or y2 >= height) or board[y2][x2] == ' ':
                # traverse face
                x2, y2, dir2, face2 = traverse(facemap, sidedim, x, y, curdir, face)
            else:
                face2 = get_face(facemap, sidedim, x, y)
            if board[y2][x2] == '#':
                # wall
                break
            # print(f'{(x, y)} -> {(x2, y2)} (dir={di.name})')
            x, y, face, curdir = x2, y2, face2, dir2
            output[y][x] = syms[curdir]
    # print(x, y, int(curdir))
    print(1000*(y+1) + 4*(x+1) + curdir)

def get_face(facemap, sidedim, x, y):
    x = (x // sidedim) * sidedim
    y = (y // sidedim) * sidedim
    return next(k for (k, v) in facemap.items() if v == (x, y))

def traverse(facemap, sidedim, x, y, curdir, face):
    # hardcode ftw
    #
    #   ab
    #   c
    #  de
    #  f
    #
    conns = {
        ('a', Dir.U): ('f', Dir.R),
        ('b', Dir.U): ('f', Dir.U),
        ('b', Dir.R): ('e', Dir.L),
        ('b', Dir.D): ('c', Dir.L),
        ('c', Dir.R): ('b', Dir.U),
        ('e', Dir.R): ('b', Dir.L),
        ('e', Dir.D): ('f', Dir.L),
        ('f', Dir.R): ('e', Dir.U),
        ('f', Dir.D): ('b', Dir.D),
        ('f', Dir.L): ('a', Dir.D),
        ('d', Dir.L): ('a', Dir.R),
        ('d', Dir.U): ('c', Dir.R),
        ('c', Dir.L): ('d', Dir.D),
        ('a', Dir.L): ('d', Dir.R),
    }
    # test
    #
    #   a
    # bcd
    #   ef
    #
    # conns = {
    #     ('a', Dir.U): ('b', Dir.D),
    #     ('a', Dir.R): ('f', Dir.L),
    #     ('d', Dir.R): ('f', Dir.D),
    #     ('f', Dir.U): ('d', Dir.L),
    #     ('f', Dir.R): ('a', Dir.L),
    #     ('f', Dir.D): ('b', Dir.R),
    #     ('e', Dir.D): ('b', Dir.U),
    #     ('e', Dir.L): ('c', Dir.U),
    #     ('c', Dir.D): ('e', Dir.R),
    #     ('b', Dir.D): ('e', Dir.U),
    #     ('b', Dir.L): ('f', Dir.U),
    #     ('b', Dir.U): ('a', Dir.D),
    #     ('c', Dir.U): ('a', Dir.R),
    #     ('a', Dir.L): ('c', Dir.D),
    # }
    # figure out the location within the first face
    fx, fy = facemap[face]
    x -= fx
    y -= fy

    # map edges from each face onto one another
    newface, newdir = conns[(face, curdir)]
    dimmax = sidedim - 1
    rotations = {
        (Dir.R, Dir.D): (dimmax - y, 0),
        (Dir.L, Dir.D): (y, 0),
        (Dir.D, Dir.D): (x, 0),
        (Dir.R, Dir.L): (dimmax, dimmax - y),
        (Dir.D, Dir.L): (dimmax, x),
        (Dir.L, Dir.R): (0, dimmax - y),
        (Dir.U, Dir.R): (0, x),
        (Dir.D, Dir.U): (dimmax - x, dimmax),
        (Dir.R, Dir.U): (y, dimmax),
        (Dir.L, Dir.U): (dimmax - y, dimmax),
        (Dir.U, Dir.U): (x, dimmax),
    }
    assert (curdir, newdir) in rotations, f'{(curdir, newdir)}'
    x, y = rotations[(curdir, newdir)]

    # finally, remap to coords on board
    fx, fy = facemap[newface]
    x += fx
    y += fy
    return x, y, newdir, newface

def input():
    lines = [line.strip('\n') for line in sys.stdin.readlines()]
    board = lines[:-2]
    maxlen = max(len(b) for b in board)
    for i, b in enumerate(board):
        padding = ' ' * (maxlen - len(b))
        board[i] = b + padding
    path = []
    for c in re.split(r'(\d+)', lines[-1]):
        if c in ('L', 'R'):
            path.append(c)
            continue
        if c != '':
            path.append(int(c))
    return board, path

board, path = input()
one(board, path)
two(board, path)
