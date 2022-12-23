from __future__ import annotations
from dataclasses import dataclass
import sys
from dataclasses import dataclass
from typing import Callable, Union, Literal
import copy

Step = Union["Leaf", "Inner"]


@dataclass
class Op:
    name: str
    f: Callable[[int, int], int]


add = Op("+", lambda a, b: a + b)
sub = Op("-", lambda a, b: a - b)
mul = Op("*", lambda a, b: a * b)
div = Op("/", lambda a, b: a // b)

OPS = {"+": add, "-": sub, "*": mul, "/": div}
INVERSE_OPS = {"/": mul, "*": div, "-": add, "+": sub}


@dataclass
class Leaf:
    value: int


@dataclass
class Inner:
    op: Op
    deps: tuple[str, str]


def one(graph: dict[str, Step]):
    expr = build_expr(graph, "root", human=False)
    expr = collapse(expr)
    assert expr[0] == "LIT"
    print(expr[1])


def two(graph):
    _, _, lexpr, rexpr = build_expr(graph, "root")
    while lexpr[0] != "HUMAN":
        # print()
        if not contains_human(lexpr):
            lexpr, rexpr = rexpr, lexpr
        lexpr, rexpr = invert(lexpr, rexpr)
        lexpr = collapse(lexpr)
        rexpr = collapse(rexpr)
    rexpr = collapse(rexpr)
    assert rexpr[0] == "LIT"
    print(rexpr[1])


Expr = Union['ExprLit', 'ExprOp', 'ExprHuman']
ExprLit = tuple[Literal['LIT'], int]
ExprOp = tuple[Literal['OP'], Op, 'Expr', 'Expr']
ExprHuman = tuple[Literal['HUMAN']]


def build_expr(graph, name, human=True) -> Expr:
    if name == "humn" and human:
        return ("HUMAN",)
    node = graph[name]
    if isinstance(node, Leaf):
        return ("LIT", node.value)

    left, right = node.deps
    lexpr = build_expr(graph, left, human)
    rexpr = build_expr(graph, right, human)
    return ("OP", node.op, lexpr, rexpr)


def contains_human(expr: Expr) -> bool:
    match expr:
        case ['HUMAN']:
            return True
        case ['LIT', _]:
            return False
        case ['OP', _, lexpr, rexpr]:
            return contains_human(lexpr) or contains_human(rexpr)


def collapse(
    expr: Expr,
) -> Expr:
    def _collapse(expr: Expr) -> tuple[Expr, bool]:
        if expr[0] == "HUMAN":
            return expr, False
        if expr[0] == "LIT":
            return expr, True
        assert expr[0] == "OP"
        _, op, lexpr, rexpr = expr
        lval, lok = _collapse(lexpr)
        rval, rok = _collapse(rexpr)
        if not lok or not rok:
            return ("OP", expr[1], lval, rval), False
        assert lval[0] == "LIT"
        assert rval[0] == "LIT"
        return ("LIT", op.f(lval[1], rval[1])), True
    return _collapse(expr)[0]


def invert(lexpr, rexpr) -> tuple[Expr, ExprOp]:
    assert lexpr[0] == "OP"
    _, op, llexpr, rrexpr = lexpr

    invop = INVERSE_OPS[op.name]
    if op.name not in ("+", "*"):
        return llexpr, ("OP", invop, rexpr, rrexpr)
    # commutes, prefer the side with human
    if not contains_human(llexpr):
        llexpr, rrexpr = rrexpr, llexpr
    return llexpr, ("OP", invop, rexpr, rrexpr)


def parse_inner(line: str) -> Inner:
    for o in OPS:
        if o not in line:
            continue
        deps = tuple(d.strip() for d in line.split(o))
        return Inner(op=OPS[o], deps=deps)
    raise ValueError(f"could not parse: {line}")


def input() -> dict[str, Step]:
    lines = [line.strip() for line in sys.stdin.readlines()]
    steps = {}
    for line in lines:
        name, rawvalue = line.split(": ")
        try:
            steps[name] = Leaf(value=int(rawvalue))
        except:
            steps[name] = parse_inner(rawvalue)
    return steps


def main(lines):
    one(copy.deepcopy(lines))
    two(lines)


if __name__ == "__main__":
    main(input())
