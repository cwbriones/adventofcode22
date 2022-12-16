from collections import (
    defaultdict,
)
from dataclasses import dataclass
import sys
import re
import networkx
import typing
import itertools

from  multiprocessing import Pool, cpu_count

PAT = re.compile(r"Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z]{2}(, [A-Z]{2})*)")

@dataclass
class Valve:
    name: str
    flow: int
    outs: dict[str, int]

class SearchState(typing.NamedTuple):
    cur: Valve
    flow: int = 0
    total: int = 0
    n: int = 30

    def move_to(self, valve: Valve):
        tick = self.cur.outs[valve.name]
        return self._replace(
            cur=valve,
            flow=self.flow + valve.flow,
            total=self.total + tick*self.flow,
            n=self.n - tick,
        )

def search(state: SearchState, valves, remaining, path=None):
    if path is None:
        path = []
    outs = state.cur.outs
    reachable = [r for r in outs if r in remaining and outs[r] <= state.n]
    if not reachable:
        # wait out remaining time
        return state.total + state.flow * state.n, path
    best = 0
    bestpath = path
    for r in reachable:
        remaining.remove(r)
        newstate = state.move_to(valves[r])
        score, fullpath = search(newstate, valves, remaining, path=path + [valves[r].name])
        if score > best:
            best = score
            bestpath = fullpath
        remaining.add(r)
    return best, bestpath

def one(valves: dict[str, Valve]):
    remaining = {name for name in valves if name != 'AA'}
    best, _ = search(SearchState(cur=valves['AA'], n=30), valves, remaining)
    print(best)

def two(valves: dict[str, Valve]):
    nonempty = set(name for name, v in valves.items() if v.flow > 0)
    def search_with_elephant(s):
        ele = set(s)
        remaining = nonempty - ele

        # elephant goes for ele, I go for nonempty
        state = SearchState(cur=valves['AA'], n=26)
        return \
            search(state, valves, remaining)[0] +\
            search(state, valves, ele)[0]
    print(max(search_with_elephant(s) for s in progress(subsets(nonempty))))

def subsets(S):
    for m in range(len(S) // 2 + 1):
        yield from itertools.combinations(S, m)

def progress(it):
    items = list(it)
    total = len(items)
    for i, item in enumerate(items):
        remain = total - i
        if remain % 500 == 0:
            print(remain)
        yield item

def input():
    lines = [line.strip() for line in sys.stdin.readlines()]

    rates = {}
    edges = {}
    for line in lines:
        match = PAT.match(line)
        if match is None:
            raise ValueError(line)
        name, flow, outs, _ = match.groups()
        flow = int(flow)
        rates[name] = int(flow)
        edges[name] = outs.split(', ')

    weights = build_weights(edges, rates)
    valves = {
        name: Valve(name=name, flow=rates[name], outs=weights[name])
        for name in weights
    }
    return valves

def build_weights(edges: dict[str, list[str]], rates: dict[str, int]):
    graph = networkx.DiGraph(incoming_graph_data=edges)
    nonempty = [name for name in edges if rates[name] > 0 or name == 'AA']

    weights = defaultdict(dict)
    for i, end in enumerate(nonempty):
        pathlens = networkx.shortest_path_length(graph, target=end)
        assert isinstance(pathlens, dict)
        for start in nonempty[i+1:]:
            # +1 because this is time to reach and then open
            weights[start][end] = pathlens[start] + 1
            weights[end][start] = pathlens[start] + 1
    return weights


def main(valves):
    one(valves)
    two(valves)


if __name__ == "__main__":
    main(input())
