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
        if line != "":
            group.append(int(line))
        elif group:
            group = []
            groups.append(group)
    return groups


def main(lines):
    one(lines)
    two(lines)


if __name__ == "__main__":
    main(input())
