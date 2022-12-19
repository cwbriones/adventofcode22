from __future__ import annotations
from collections import (
    deque,
)
from dataclasses import dataclass
import sys
from copy import deepcopy
from typing import Callable, NamedTuple, Iterator


def one(monkeys: list[Monkey]) -> None:
    run(monkeys, 20, divide=True)


def two(monkeys: list[Monkey]) -> None:
    run(monkeys, 10_000)


def run(monkeys: list[Monkey], rounds: int, divide: bool = False) -> None:
    p = 1
    for m in monkeys:
        p *= m.test[0]
    for _ in range(rounds):
        for monkey in monkeys:
            while (res := monkey.inspect(divide=divide)) is not None:
                item, target = res
                monkeys[target].receive(item % p)
    monkeys.sort(key=lambda m: m.count, reverse=True)
    print(monkeys[0].count * monkeys[1].count)


def input() -> list["Monkey"]:
    it = (line.strip() for line in sys.stdin.readlines())
    monkeys = []
    while True:
        monkey = read_monkey(it, len(monkeys))
        monkeys.append(monkey)
        try:
            gap = next(it)
            assert gap == ""
        except StopIteration:
            return monkeys


class Test(NamedTuple):
    modulus: int
    iftrue: int
    iffalse: int


@dataclass
class Monkey:
    items: deque[int]
    test: Test
    op: Callable[[int], int]
    count = 0

    def inspect(self, divide: bool = False) -> tuple[int, int] | None:
        if not self.items:
            return None
        self.count += 1

        item = self.items.popleft()
        item = self.op(item)
        if divide:
            item = item // 3

        if item % self.test[0] == 0:
            return item, self.test[1]
        else:
            return item, self.test[2]

    def receive(self, item: int) -> None:
        self.items.append(item)


def read_monkey(it: Iterator[str], num: int) -> Monkey:
    expect_label(it, f"Monkey {num}")
    items = expect_label(it, "Starting items", parse=read_items)
    op = expect_label(it, "Operation", parse=read_op)
    test = read_test(it)
    return Monkey(items=deque(items), test=test, op=op)


def read_test(it: Iterator[str]) -> Test:
    modulus = expect_label(it, "Test", parse=read_cond)
    iftrue = expect_label(it, parse=read_target)
    iffalse = expect_label(it, parse=read_target)
    return Test(modulus, iftrue, iffalse)


def read_items(line: str) -> list[int]:
    return [int(x.strip()) for x in line.split(",")]


def read_target(line: str) -> int:
    line = assert_prefix(line, "throw to monkey")
    return int(line)


def read_op(line: str) -> Callable[[int], int]:
    line = assert_prefix(line, "new = old ")

    op, rhs = line.split(" ")

    if op == "+":
        if rhs == "old":
            return lambda old: old * 2
        else:
            rhs = int(rhs)
            return lambda old: old + rhs
    elif op == "*":
        if rhs == "old":
            return lambda old: old * old
        else:
            rhs = int(rhs)
            return lambda old: old * rhs
    else:
        raise ValueError(f"unknown op {op}")


def read_cond(line: str) -> int:
    return int(line[len("divisible by ") :])


def assert_prefix(line: str, prefix: str) -> str:
    assert line.startswith(prefix)
    l = len(prefix)
    return line[l:].strip()


def expect_label(it, label=None, parse=None):
    line = next(it)
    if label is not None:
        assert_prefix(line, label)
    _, snd = line.split(":")
    snd = snd.strip()
    if parse is not None:
        return parse(snd)
    return snd


def main(monkeys: list[Monkey]) -> None:
    one(deepcopy(monkeys))
    two(monkeys)


if __name__ == "__main__":
    main(input())
