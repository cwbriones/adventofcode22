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

def one(elves):
    print(max(sum(e) for e in elves))

def two(elves):
    sums = [sum(e) for e in elves]
    sums.sort(reverse=True)
    print(sum(sums[:3]))

def input():
    group = []
    groups = []
    for line in sys.stdin.readlines():
        line = line.strip()
        if line != '':
            group.append(int(line))
        elif group:
            group = []
            groups.append(group)
    return groups

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
