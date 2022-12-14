from functools import cmp_to_key
import sys
from ast import literal_eval
from typing import Literal

# NOTE: Recursive types are only supported by pyright
Expr = int | list['Expr']

Cmp = Literal[0, 1, -1]

def compare(left: Expr, right: Expr) -> Cmp:
    match (left, right):
        case ([*_] as left, [*_] as right):
            for a, b in zip(left, right):
                if (res := compare(a, b)) != 0:
                    return res
            return cmp(len(left), len(right))
        case ([*_], _):
            return compare(left, [right])
        case (_, [*_]):
            return compare([left], right)
        case _:
            return cmp(left, right)


def cmp(a, b) -> Cmp:
    return (a > b) - (a < b)


def one(pairs):
    print(sum(i for i, (p, q) in enumerate(pairs, start=1) if compare(p, q) < 1))


def two(pairs):
    keys: list[Expr] = [[[2]], [[6]]]
    values = keys.copy()
    for pair in pairs:
        values.extend(pair)

    values.sort(key=cmp_to_key(compare))

    i = values.index(keys[0]) + 1
    j = values.index(keys[1]) + 1
    print(i * j)


def input() -> list[Expr]:
    lines = [line.strip() for line in sys.stdin.readlines()]
    while len(lines) % 3 != 0:
        lines.append("")
    # E Z
    return [[literal_eval(s) for s in ls[:2]] for ls in zip(*[iter(lines)] * 3)]


def main(lines):
    one(lines)
    two(lines)


if __name__ == "__main__":
    main(input())
