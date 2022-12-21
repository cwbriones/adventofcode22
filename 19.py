from __future__ import annotations
from collections import (
    deque,
    defaultdict
)
from operator import itemgetter
import os
import sys
from copy import deepcopy
import math
import re
from typing import Literal, TypeVar, get_args, Iterable
# from enum import IntEnum, auto
#
# class Res(IntEnum):
#     ORE = 0
#     CLAY = auto()
#     OBSIDIAN = auto()
#     GEODE = auto()

GEODE = 3
Resource = Literal['ore', 'clay', 'obsidian', 'geode']
RESOURCES = get_args(Resource)
N = len(RESOURCES)

class Counter(tuple[int, int, int, int]):
    def __new__(cls, x1, x2, x3, x4) -> Counter:
        return super().__new__(cls, (x1, x2, x3, x4))

    def add(self, two: Counter) -> Counter:
        return Counter(*(a + b for a, b in zip(self, two)))

    def add_index(self, idx: int, val: int) -> Counter:
        return Counter(*(a + val if i == idx else a for i, a in enumerate(self)))

    def sub(self, two: Counter) -> Counter:
        return Counter(*(a - b for a, b in zip(self, two)))

    def mul(self, k: int) -> Counter:
        return Counter(*(a * k for a in self))

    @staticmethod
    def empty():
        # could be a singleton :shruggie:
        return Counter(0, 0, 0, 0)

Blueprint = tuple[Counter, Counter, Counter, Counter]

def one(blueprints: Iterable[Blueprint]):
    print(blueprints)
    quality_sum = 0
    for bid, blueprint in enumerate(blueprints, start=1):
        best = find_best(blueprint)
        print(f'best is {best}: q = {best} * {bid} = {best*bid}')
        quality_sum += best*bid
    print(quality_sum)

def two(blueprints: Iterable[Blueprint]):
    pass

def find_best(
    blueprint: Blueprint,
) -> int:
    best = (0, None, None)
    SearchState = tuple[Counter, Counter, int, list[str]]

    resources = Counter.empty().add_index(idx=0, val=1)
    stack: deque[SearchState] = deque([(resources, Counter.empty(), 1, [])])
    MAXTIME = 24

    while stack:
        robots, resources, time, history = stack.popleft()
        if time > MAXTIME:
            best = max(best, (resources[3], robots, history), key=itemgetter(0))
            continue

        for kind, cost in enumerate(blueprint):
            if kind != GEODE and robots[kind] >= max(cost[kind] for cost in blueprint):
                # If we already have as many robots as the highest cost for any build, we
                # do not need any more of that type (besides geode)
                continue
            elif not all(rs > 0 or c == 0 for rs, c in zip(robots, cost)):
                # waiting will not help
                continue
            elapsed = max((
                math.ceil((c-r) / cnt)
                for (cnt, r, c) in zip(robots, resources, cost)
                if r < c
            ), default=0)
            newtime = time + elapsed + 1
            if newtime > MAXTIME:
                continue
            entry = f't={time} deciding to wait {elapsed} res={resources}'
            # elapse time
            newresources = resources
            for _ in range(elapsed):
                newresources = newresources.add(robots)
            entry += f'\nt={time + elapsed} res={newresources}'
            # build the robot
            newresources = newresources.sub(cost).add(robots)
            newrobots = robots.add_index(kind, 1)
            entry += f'\nt={time + elapsed} built {RESOURCES[kind]} res={newresources}'
            stack.append((newrobots, newresources, newtime, history + [entry]))

        # don't do anything until the end
        newresources = resources
        for _ in range(MAXTIME+1-time):
            newresources = newresources.add(robots)
        history = history + [f't={time} nothing left to do.']
        stack.append((robots, newresources, MAXTIME+1, history))
    # if best[0] > 0:
    #     for h in best[-1]:
    #         print(f'{h}')
    return best[0]

def input() -> list[Blueprint]:
    costpat = re.compile(r'(\d+) (ore|clay|obsidian|geode)')
    bps: list[Blueprint] = []
    indices = {k: i for (i, k) in enumerate(RESOURCES)}
    for line in sys.stdin.readlines():
        line = line.strip()
        _, costline = line.split(': ')
        costmap: list[Counter] = [Counter(0, 0, 0, 0)] * 4
        for costentry in costline.split('Each '):
            if not costentry:
                continue
            name, costline = costentry.split(" costs ")
            assert name.endswith(" robot")
            name = name[:-6]
            assert name in RESOURCES

            costs = [0] * len(get_args(Resource))
            for val, kind in costpat.findall(costline):
                costs[indices[kind]] = int(val)
            costmap[indices[name]] = Counter(*costs)
        bps.append(tuple(costmap))
    return bps


def main(lines):
    one(lines)
    two(lines)


if __name__ == "__main__":
    main(input())
