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


if os.environ.get("DEBUG"):
    def debug(msg):
        print('[DEBUG]: ', end='', file=sys.stderr)
        print(msg, file=sys.stderr)
else:
    def debug(msg):
        pass


def one(monkeys):
    for m in monkeys:
        print(f'Monkey {m.label}: {m.items}')
    for _ in range(20):
        for monkey in monkeys:
            while True:
                res = monkey.inspect()
                if res is None:
                    break
                item, target = res
                monkeys[target].receive(item)
    for m in monkeys:
        print(f'Monkey {m.label}: {m.inspect_count}')
    monkeys.sort(key=lambda m: m.inspect_count, reverse=True)
    print(monkeys[0].inspect_count * monkeys[1].inspect_count)


def two(monkeys):
    for _ in range(10_000):
        for monkey in monkeys:
            while True:
                res = monkey.inspect()
                if res is None:
                    break
                item, target = res
                monkeys[target].receive(item)
    for m in monkeys:
        print(f'Monkey {m.label}: {m.inspect_count}')
    monkeys.sort(key=lambda m: m.inspect_count, reverse=True)
    print(monkeys[0].inspect_count * monkeys[1].inspect_count)


def input():
    it = (line.strip() for line in sys.stdin.readlines())
    monkeys = []
    while True:
        monkey = read_monkey(it)
        monkey.label = len(monkeys)
        monkeys.append(monkey)
        try:
            gap = next(it)
            assert gap == ""
        except StopIteration:
            return monkeys

@dataclass
class Monkey:
    items: deque[int]
    test: object
    op: object
    worry: int = 0
    label: int = 0
    inspect_count = 0

    def inspect(self):
        if not self.items:
            return None
        self.inspect_count += 1

        item = self.items.popleft()
        # update worry level
        item = self.op(item) // 3

        target = self.test(item)
        return item, target

    def receive(self, item):
        self.items.append(item)

def read_monkey(it):
    expect_prefix(it, prefix="Monkey")
    items = expect_prefix(it, prefix="Starting", parse=parse_list)
    op = expect_prefix(it, parse=read_op)
    cond = expect_prefix(it, parse=read_cond)
    iftrue = expect_prefix(it, parse=read_target)
    iffalse = expect_prefix(it, parse=read_target)

    test = lambda v: iftrue if cond(v) else iffalse
    return Monkey(items=deque(items), test=test, op=op)

def parse_list(line):
    return [int(x.strip()) for x in line.split(',')]

def read_target(line):
    line = assert_prefix(line, "throw to monkey")
    return int(line)

def read_op(line):
    line = assert_prefix(line, "new = old ")

    op, rhs = line.split(" ")

    if op == '+':
        if rhs == "old":
            return lambda v: v * 2
        else:
            val = int(rhs)
            return lambda v: v + val
    elif op == '*':
        if rhs == "old":
            return lambda v: v * v
        else:
            val = int(rhs)
            return lambda v: v * val
    else:
        raise ValueError(f"unknown op {op}")

def read_cond(line):
    v = int(line[len("divisible by "):])
    return lambda x: x % v == 0

def assert_prefix(line, prefix):
    assert line.startswith(prefix)
    l = len(prefix)
    return line[l:].strip()

def expect_prefix(it, prefix=None, parse=None):
    line = next(it)
    fst, snd = line.split(':')
    snd = snd.strip()
    if prefix is not None:
        assert fst.startswith(prefix), f'{fst} does not start with {prefix}'
    if parse is not None:
        return parse(snd)
    return snd

def main(monkeys):
    one(deepcopy(monkeys))
    two(monkeys)


if __name__ == "__main__":
    main(input())
