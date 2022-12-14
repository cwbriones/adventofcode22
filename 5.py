import sys
import re
import copy

NUM = re.compile("\d+")


def one(inputs):
    stacks, moves = inputs
    for cnt, src, dst in moves:
        for _ in range(cnt):
            stacks[dst].append(stacks[src].pop())
    print("".join(s[-1] for s in stacks))


def two(inputs):
    stacks, moves = inputs
    for cnt, src, dst in moves:
        stacks[dst].extend(stacks[src][-cnt:])
        stacks[src] = stacks[src][:-cnt]
    print("".join(s[-1] for s in stacks))


def input():
    # read the stacks
    lines = sys.stdin.readlines()
    stacks = []
    for i, line in enumerate(lines):
        line = line.strip("\n")
        if not line:
            break
        line = line.replace("[", " ").replace("]", " ")
        stacks.append(line)
    stacks.pop()
    stacks = [s for s in [list(reversed(s)) for s in zip(*stacks)] if s[0] != " "]
    for stack in stacks:
        while stack[-1] == " ":
            stack.pop()
    # read the moves
    moves = []
    for line in lines[i + 1 :]:
        moves.append([int(n) for n in NUM.findall(line)])
        moves[-1][1] -= 1
        moves[-1][2] -= 1
    return stacks, moves


def main(lines):
    one(copy.deepcopy(lines))
    two(lines)


if __name__ == "__main__":
    main(input())
