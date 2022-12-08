import sys


def one(lines):
    score = 0
    mapping = {"A": 0, "B": 1, "C": 2, "X": 0, "Y": 1, "Z": 2}
    for a, b in lines:
        a, b = mapping[a], mapping[b]
        score += b + 1
        if a == b:
            score += 3
        elif (b - a) % 3 == 1:
            score += 6
    print(score)


def two(lines):
    score = 0
    mapping = {"A": 0, "B": 1, "C": 2}
    for a, b in lines:
        a = mapping[a]
        b = choose(a, b)
        score += b + 1
        if a == b:
            score += 3
        elif (b - a) % 3 == 1:
            score += 6
    print(score)


def choose(opp, b):
    if b == "X":
        return (opp - 1) % 3
    elif b == "Y":
        return opp
    else:
        return (opp + 1) % 3


def input():
    lines = sys.stdin.readlines()
    return [tuple(line.strip().split()) for line in lines]


def main(lines):
    one(lines)
    two(lines)


if __name__ == "__main__":
    main(input())
