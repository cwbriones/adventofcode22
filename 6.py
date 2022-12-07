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
from itertools import islice

def sliding_window(iterable, n):
    # sliding_window('ABCDEFG', 4) --> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)

def find_first_packet(msg, n):
    for i, pack in enumerate(sliding_window(msg, n), start=n):
        if len(set(pack)) == n:
            print(i)
            return
    print('nothing was found?')

def one(msg):
    find_first_packet(msg, 4)

def two(msg):
    find_first_packet(msg, 14)

def input():
    return sys.stdin.readlines()[0].strip()

def main(lines):
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=False, action='store_true')
    args = parser.parse_args(sys.argv[1:])
    if args.p:
        two(lines)
        return
    one(lines)

if __name__ == '__main__':
    main(input())
