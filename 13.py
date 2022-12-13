from functools import cmp_to_key
import sys


def compare(left, right, depth=0):
    if isinstance(left, int) and isinstance(right, int):
        return cmp(left, right)
    elif isinstance(left, list) and isinstance(right, list):
        for a, b in zip(left, right):
            if (res := compare(a, b, depth + 1)) != 0:
                return res
        return cmp(len(left), len(right))
    elif isinstance(left, int):
        return compare([left], right, depth)
    elif isinstance(right, int):
        return compare(left, [right], depth)
    else:
        raise ValueError("bad comparison")


def cmp(a, b):
    return (a > b) - (a < b)


def one(pairs):
    print(sum(i for i, (p, q) in enumerate(pairs, start=1) if compare(p, q) < 1))


def two(pairs):
    keys = [[[2]], [[6]]]
    values = keys.copy()
    for pair in pairs:
        values.extend(pair)

    values.sort(key=cmp_to_key(compare))

    i = values.index(keys[0]) + 1
    j = values.index(keys[1]) + 1
    print(i * j)


def input():
    lines = [line.strip() for line in sys.stdin.readlines()]
    while len(lines) % 3 != 0:
        lines.append("")
    # E Z
    return [[eval(s) for s in ls[:2]] for ls in zip(*[iter(lines)] * 3)]


def main(lines):
    one(lines)
    two(lines)


if __name__ == "__main__":
    main(input())
