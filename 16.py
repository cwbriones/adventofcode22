from collections import (
    defaultdict,
)
from dataclasses import dataclass
import sys
import re
import networkx
import typing
import itertools


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
            total=self.total + tick * self.flow,
            n=self.n - tick,
        )


def one(valves: dict[str, Valve]):
    memo = defaultdict(lambda: 0)
    best = search(SearchState(cur=valves["AA"], n=30), valves, memo)
    print(best)


def search(state: SearchState, valves, memo, visited=None):
    if visited is None:
        visited = set()
    outs = state.cur.outs
    reachable = [
        r for r in outs if r not in visited and outs[r] <= state.n and r != "AA"
    ]

    score = state.total + state.flow * state.n
    key = frozenset(visited)
    memo[key] = max(memo[key], score)

    if not reachable:
        # wait out remaining time
        return score
    best = 0
    for r in reachable:
        visited.add(r)
        newstate = state.move_to(valves[r])
        score = search(newstate, valves, memo, visited)
        if score > best:
            best = score
        visited.remove(r)
    return best


def two(valves: dict[str, Valve]):
    memo = defaultdict(lambda: 0)
    search(SearchState(cur=valves["AA"], n=26), valves, memo)

    needs_visit = frozenset(set(valves) - {"AA"})
    fill_memo(needs_visit, memo)

    best = 0
    for subset in subsets(needs_visit):
        me = frozenset(subset)
        ele = needs_visit - me
        if (total := memo[me] + memo[ele]) > best:
            best = total
    print(best)


def fill_memo(visited, memo):
    """
    Fill in the memo with partial results for impossible final states.

    Certain visited states never arise because it is impossible for the walk to
    reach all of those nodes in the allotted time. Consider the graph

                          AA <- 20 -> BB <- 15 -> CC

    {'BB', 'CC'} will never be in the search results because it would take t=35
    seconds to occur, which is greater than the t=26 limit.

    This means that the best score you can get from a run that attempts to visit those
    nodes is the best /possible/ score out of its subsets.

    e.g. Subsets are {'BB'} and {'CC'}. BB is reachable in 20, CC is never reachable.
    Therefore we expect memo[{'BB'}] to set memo[{'BB', 'CC'}] = memo[{'BB'}]
    """
    if visited not in memo:
        best = 0
        for v in visited:
            flow = fill_memo(visited - {v}, memo)
            if flow > best:
                best = flow
        memo[visited] = best
    return memo[visited]


def subsets(S):
    for m in range(len(S) // 2 + 1):
        yield from itertools.combinations(S, m)


def input():
    PAT = re.compile(
        r"Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z]{2}(, [A-Z]{2})*)"
    )

    rates = {}
    edges = {}
    for line in sys.stdin.readlines():
        match = PAT.match(line)
        if match is None:
            raise ValueError(line)
        name, flow, outs, _ = match.groups()
        flow = int(flow)
        rates[name] = int(flow)
        edges[name] = outs.split(", ")

    weights = build_weights(edges, rates)
    valves = {
        name: Valve(name=name, flow=rates[name], outs=weights[name]) for name in weights
    }
    return valves


def build_weights(edges: dict[str, list[str]], rates: dict[str, int]):
    graph = networkx.DiGraph(incoming_graph_data=edges)
    nonempty = [name for name in edges if rates[name] > 0 or name == "AA"]

    weights = defaultdict(dict)
    for i, end in enumerate(nonempty):
        pathlens = networkx.shortest_path_length(graph, target=end)
        assert isinstance(pathlens, dict)
        for start in nonempty[i + 1 :]:
            # +1 because this is time to reach and then open
            weights[start][end] = pathlens[start] + 1
            weights[end][start] = pathlens[start] + 1
    return weights


def main(valves):
    one(valves)
    two(valves)


if __name__ == "__main__":
    main(input())
