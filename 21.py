from __future__ import annotations
import argparse
from collections import (
    defaultdict,
    deque,
)
from contextlib import contextmanager
from dataclasses import dataclass
import functools
import math
import os
import sys
from copy import deepcopy
from dataclasses import dataclass
from typing import Callable, Union

Step = Union['Leaf', 'Inner']

@dataclass
class Leaf:
    name: str
    value: int

@dataclass
class Inner:
    name: str
    op: Callable[[int, int], int]
    opname: str
    deps: tuple[str, str]


if os.environ.get("DEBUG"):
    def debug(msg):
        print('[DEBUG]: ', end='', file=sys.stderr)
        print(msg, file=sys.stderr)
else:
    def debug(msg):
        pass


def one(graph: list[Step]):
    resolved: dict[str, int] = {}
    inner: dict[str, Inner] = {}

    for g in graph:
        if isinstance(g, Leaf):
            resolved[g.name] = g.value
        if isinstance(g, Inner):
            inner[g.name] = g

    stack = [inner['root']]
    while stack:
        p = stack.pop()
        if all(d in resolved for d in p.deps):
            a = resolved[p.deps[0]]
            b = resolved[p.deps[1]]
            # print(f'resolve {p.name}: {p.op(a,b)}')
            resolved[p.name] = p.op(a, b)
            continue
        stack.append(p)
        for d in p.deps:
            if d not in resolved:
                stack.append(inner[d])
    print(resolved['root'])

def build_expr(graph, name):
    if name == 'humn':
        return ('HUMAN',)
    node = graph[name]
    if isinstance(node, Leaf):
        return ('LIT', node.value)

    left, right = node.deps
    lexpr = build_expr(graph, left)
    rexpr = build_expr(graph, right)
    return ('OP', node.opname, lexpr, rexpr)

from sympy import Symbol
from sympy.solvers import solve

h = Symbol('h')

def build_npexpr(graph, name):
    if name == 'humn':
        return h
    node = graph[name]
    if isinstance(node, Leaf):
        return node.value
    left, right = node.deps
    lexpr = build_npexpr(graph, left)
    rexpr = build_npexpr(graph, right)
    if node.opname == "+":
        return lexpr + rexpr
    elif node.opname == "-":
        return lexpr - rexpr
    elif node.opname == "*":
        return lexpr * rexpr
    elif node.opname == "/":
        return lexpr / rexpr

def contains_human(expr):
    match expr:
        case ['HUMAN']:
            return True
        case ['LIT', val]:
            return False
        case ['OP', name, lexpr, rexpr]:
            return contains_human(lexpr) or contains_human(rexpr)

def two(graph):
    root = None
    for step in graph:
        if step.name == 'humn':
            # ignore
            continue
        if step.name == 'root' and isinstance(step, Inner):
            root = step
            continue
    assert root is not None
    left, right = root.deps
    lexpr = build_npexpr({g.name: g for g in graph}, left)
    rexpr = build_npexpr({g.name: g for g in graph}, right)
    print(f'ans is 3592056845086 or 301')
    print(lexpr - rexpr)
    print(math.ceil(solve(lexpr - rexpr, h)[0]))
    # _, _, lexpr, rexpr = build_expr({g.name: g for g in graph}, 'root')
    # print(lexpr)
    # print(rexpr)
    # for _ in range(5):
    #     print()
    #     if not contains_human(lexpr):
    #         lexpr, rexpr = rexpr, lexpr
    #     if lexpr[0] == 'HUMAN':
    #         print('DONE')
    #         break
    #     lexpr, rexpr = invert(lexpr, rexpr)
    #     print('LEFT', lexpr)
    #     print('RIGHT', rexpr)
    # print(eval_expr(rexpr))

def eval_expr(expr):
    if expr[0] == 'LIT':
        return expr[1]
    _, op, lexpr, rexpr = expr
    if op == "+":
        return eval_expr(lexpr) + eval_expr(rexpr)
    elif op == "-":
        return eval_expr(lexpr) - eval_expr(rexpr)
    elif op == "*":
        return eval_expr(lexpr) * eval_expr(rexpr)
    elif op == "/":
        return eval_expr(lexpr) // eval_expr(rexpr)

def invert(lexpr, rexpr):
    inverses = {'/': '*', '*': '/', '-': '+', '+': '-'}
    assert lexpr[0] == 'OP'
    _, op, llexpr, rrexpr = lexpr

    invop = inverses[op]
    if op not in ('+', '*'):
        return llexpr, ('OP', invop, rexpr, rrexpr)
    # commutes, prefer the side with human
    if not contains_human(llexpr):
        llexpr, rrexpr = rrexpr, llexpr
    return llexpr, ('OP', invop, rexpr, rrexpr)


def parse_op(line: str):
    ops = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a // b,
    }
    for o in ops:
        if o not in line:
            continue
        deps = tuple(d.strip() for d in line.split(o))
        return deps, ops[o], o
    raise ValueError(f"could not parse: {line}")

def input():
    lines =  [line.strip() for line in sys.stdin.readlines()]
    steps = []
    for line in lines:
        name, rawvalue = line.split(': ')
        val = None
        try:
            val = int(rawvalue)
            step = Leaf(
                name=name,
                value=val,
            )
        except:
            deps, op, opname = parse_op(rawvalue)
            step = Inner(
                name=name,
                deps=deps,
                op=op,
                opname=opname,
            )
        steps.append(step)
    return steps



def main(lines):
    one(deepcopy(lines))
    two(lines)


if __name__ == "__main__":
    main(input())
