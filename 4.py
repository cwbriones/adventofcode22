import sys


def one(pairs):
    print(sum(1 for p, q in pairs if overlap_fully(p, q)))


def two(pairs):
    print(sum(1 for p, q in pairs if overlap_partially(p, q)))


def overlap_fully(p, q):
    if p[0] > q[0]:
        p, q = q, p
    return (p[0] < q[0] and q[1] <= p[1]) or (
        p[0] == q[0] and (q[1] <= p[1] or p[1] <= q[1])
    )


def overlap_partially(p, q):
    if p[0] > q[0]:
        p, q = q, p
    return overlap_fully(p, q) or p[0] <= q[0] <= p[1]


def input():
    pairs = []
    for line in sys.stdin.readlines():
        fst, snd = line.strip().split(",")
        fst = tuple(int(c) for c in fst.split("-"))
        snd = tuple(int(c) for c in snd.split("-"))
        pairs.append((fst, snd))
    return pairs


def main(lines):
    one(lines)
    two(lines)


if __name__ == "__main__":
    main(input())
