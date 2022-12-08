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
    print("one")


def two(lines):
    print("two")


def input():
    return [line.strip() for line in sys.stdin.readlines()]


def main(lines):
    one(lines)
    two(lines)


if __name__ == "__main__":
    main(input())
