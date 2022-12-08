import sys


def one(trees):
    vis = [[False] * len(trees[0]) for _ in trees]
    check_vis(trees, vis)
    trees = transpose(trees)
    vis = transpose(vis)
    check_vis(trees, vis)
    print(sum(1 for row in vis for t in row if t))


def transpose(arr):
    return [list(r) for r in zip(*arr)]


def check_vis(trees, vis):
    for j, row in enumerate(trees):
        tmax = -1
        i = 0
        for i, t in enumerate(row):
            if t > tmax:
                vis[j][i] = True
                tmax = t
        tmax = -1
        for k, t in enumerate(reversed(row)):
            i = len(row) - k - 1
            if t > tmax:
                vis[j][i] = True
                tmax = t


def two(trees):
    scores = [[1] * len(trees[0]) for _ in trees]
    check_score(trees, scores)
    trees = transpose(trees)
    scores = transpose(scores)
    check_score(trees, scores)
    print(max(s for row in scores for s in row))


def check_score(trees, scores):
    for j, row in enumerate(trees):
        for i, _ in enumerate(row):
            scores[j][i] *= score(row, i)


def score(row, i):
    t = row[i]
    j1 = i - 1
    while j1 > 0 and row[j1] < t:
        j1 -= 1
    if j1 < 0:
        j1 = 0
    j2 = i + 1
    while j2 < len(row) - 1 and row[j2] < t:
        j2 += 1
    if j2 == len(row):
        j2 = len(row) - 1
    return (i - j1) * (j2 - i)


def input():
    return [[int(c) for c in line.strip()] for line in sys.stdin.readlines()]


def main(lines):
    one(lines)
    two(lines)


if __name__ == "__main__":
    main(input())
