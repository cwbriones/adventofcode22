from __future__ import annotations
import os
import sys
from copy import deepcopy
from typing import Iterable, cast, Any


if os.environ.get("DEBUG"):

    def debug(msg):
        print("[DEBUG]: ", end="", file=sys.stderr)
        print(msg, file=sys.stderr)

else:

    def debug(msg):
        pass


class Node:
    def __init__(self, item: int, next: Node, prev: Node) -> None:
        self.item: int = item
        self.next: Node = next
        self.prev: Node = prev

    def __repr__(self) -> str:
        return f"Node(item={self.item!r})"


class List:
    def __init__(self):
        self.head: Node = Node(123456789, cast(Any, None), cast(Any, None))
        self.head.next = self.head
        self.head.prev = self.head

    def append(self, item):
        node = Node(item, prev=self.head.prev, next=self.head)
        self.head.prev.next = node
        self.head.prev = node

    def __iter__(self):
        return ListIterator(self)


class ListIterator:
    def __init__(self, lst):
        self.lst = lst
        self.cur = self.lst.head

    def __iter__(self):
        return self

    def __next__(self):
        self.cur = self.cur.next
        if self.cur is self.lst.head:
            raise StopIteration
        return self.cur.item


def one(nums: list[int]) -> None:
    linked = List()
    for n in nums:
        linked.append(n)

    decode(linked)

    # print(', '.join(str(item) for item in linked), end='\n\n')
    node = linked.head
    while node.item != 0:
        node = node.next

    # could do something smarter here but lets be straightforward
    # for now
    total = 0
    i = 0
    while i != 3000:
        i += 1
        node = node.next
        if node is linked.head:
            node = node.next
        if i in (1000, 2000, 3000):
            total += node.item
    print(total)


def decode(linked: List) -> None:
    nodes: list[Node] = []
    dest = linked.head
    while (dest := dest.next) is not linked.head:
        nodes.append(dest)
    nodecount = len(nodes)

    # print('Initial arrangement')
    # print(', '.join(str(item) for item in linked), end='\n\n')
    for src in nodes:
        dest = src

        # Walk from this node's current position forward
        # until we find the spot where it should be inserted
        i: int
        if src.item > 0:
            i = src.item % (nodecount - 1)
        else:
            i = src.item % (nodecount - 1)

        if i == 0:
            continue

        while i > 0:
            dest = dest.next
            if dest is linked.head:
                dest = linked.head.next
            i -= 1

        # remove the node from its position
        #
        #    ____  ____
        #    V   \ V   \
        # prev -> s -> next
        #
        src.prev.next = src.next
        #          ____
        #          V   \
        # prev <- s -> next
        #    \_________^
        #
        src.next.prev = src.prev
        #    __________
        #   V          \
        # prev <- s -> next
        #    \_________^
        #
        # [Nothing points at src now]

        # splice in node after dest
        src.next = dest.next
        #
        # (s.prev, d.prev omitted)
        #    ___________
        #   V           \
        #  d     s -> d.next
        #   \___________^
        #
        src.next.prev = src
        #          ____
        #         V    \
        #  d     s -> d.next
        #   \___________^
        #
        src.prev = dest
        #    ___   ____
        #   V   \ V    \
        #  d     s -> d.next
        #   \___________^
        #
        dest.next = src
        #    ___   ____
        #   V   \ V    \
        #  d --> s -> d.next
    print(', '.join(str(item) for item in linked), end='\n\n')


def two(nums: Iterable[int]) -> None:
    pass


def input() -> list[int]:
    return [int(line.strip()) for line in sys.stdin.readlines()]


def main(lines):
    one(deepcopy(lines))
    two(lines)


if __name__ == "__main__":
    main(input())
