from __future__ import annotations
import sys
from typing import Iterable, cast, Any


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
        self.cur = lst.head
        self.end = lst.head

    def __iter__(self):
        return self

    def __next__(self):
        self.cur = self.cur.next
        if self.cur is self.end:
            raise StopIteration
        return self.cur.item


def one(nums: Iterable[int]) -> None:
    linked = List()
    for n in nums:
        linked.append(n)

    decrypt(linked)
    print(coords(linked))


def two(nums: Iterable[int]) -> None:
    linked = List()
    for n in nums:
        linked.append(n * 811589153)
    decrypt(linked, 10)
    print(coords(linked))


def decrypt(linked: List, rounds=1) -> None:
    nodes = []
    dest = linked.head
    while (dest := dest.next) is not linked.head:
        nodes.append(dest)
    for _ in range(rounds):
        decrypt_inner(linked, nodes)

def decrypt_inner(linked, nodes):
    nodecount = len(nodes)
    for src in nodes:
        dest = src

        # Walk from this node's current position forward
        # until we find the spot where it should be inserted
        #
        # We mod (n - 1) to avoid excessive loops. The -1
        # accounts for the fact that the node being moved
        # is not considered a part of walk
        if src.item < 0:
            i = src.item  % (nodecount - 1)
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


def coords(linked):
    node = linked.head
    while node.item != 0:
        node = node.next

    total = 0
    i = 0
    while i != 3000:
        i += 1
        node = node.next
        if node is linked.head:
            node = node.next
        if i in (1000, 2000, 3000):
            total += node.item
    return total


def show(linked):
    print(', '.join(str(item) for item in linked), end='\n\n')


def input() -> list[int]:
    return [int(line.strip()) for line in sys.stdin.readlines()]


def main(lines):
    one(lines)
    two(lines)


if __name__ == "__main__":
    main(input())
