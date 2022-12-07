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

def one(lines):
    s = 0
    for line in lines:
        l = int(len(line) / 2)
        fst, snd = line[:l], line[l:]
        c = priority(next(c for c in fst if c in snd))
        s += c
    print(s)

def two(lines):
    s = 0
    for group in zip(*([iter(lines)]* 3)):
        g = set(group[0])
        g.intersection_update(group[1])
        g.intersection_update(group[2])
        s += priority(next(iter(g)))
    print(s)

def priority(c):
    p = ord(c) - ord('a') + 1
    if p < 0:
        p += 58
    return p

def input():
    return [line.strip() for line in sys.stdin.readlines()]

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
