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
    print('one')

def two(lines):
    print('two')

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
