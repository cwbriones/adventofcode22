import sys
from typing import TypeVar, Iterable


Cube = tuple[int, int, int]
T = TypeVar("T")


def main(lava: set[Cube]) -> None:
    # define the boundaries
    maxx, maxy, maxz = 0, 0, 0
    for x, y, z in lava:
        maxx = max(x, maxx)
        maxy = max(y, maxy)
        maxz = max(z, maxz)

    def in_bounds(cube):
        x, y, z = cube
        return x >= 0 and y >= 0 and z >= 0 and x <= maxx and y <= maxy and z <= maxz

    def is_open_air(p):
        """
        If a cube of air is touching the bounding box of all cubes, then it cannot
        be contained by any of the lava cubes.
        """
        x, y, z = p
        at_boundary = x == 0 or y == 0 or z == 0 or x == maxx or y == maxy or z == maxz
        return at_boundary and p not in lava

    # all cubes within boundaries that are not lava
    air = set(s for cube in lava for s in sides(cube) if in_bounds(s) and s not in lava)

    # walk and merge the cubes into connected groups
    visited = set()
    groups = []
    while air:
        group = set()
        start = air.pop()
        if start in visited:
            continue
        search = [start]
        while search:
            cube = search.pop()
            if cube in visited or cube in lava or not in_bounds(cube):
                continue
            visited.add(cube)
            group.add(cube)
            for side in sides(cube):
                search.append(side)
        groups.append(group)

    # If a single cube is touching open air, the whole group is open
    inner_area = sum(
        surface_area(g) for g in groups if not any(is_open_air(p) for p in g)
    )
    total = surface_area(lava)
    # one
    print(total)
    # two
    print(total - inner_area)


def surface_area(cubes: set[Cube]) -> int:
    area = 0
    for cube in cubes:
        for side in sides(cube):
            if side not in cubes:
                area += 1
    return area


def sides(cube: Cube) -> Iterable[Cube]:
    x, y, z = cube
    yield from [
        (x - 1, y, z),
        (x + 1, y, z),
        (x, y - 1, z),
        (x, y + 1, z),
        (x, y, z - 1),
        (x, y, z + 1),
    ]


def input() -> set[Cube]:
    return set(tuple(map(int, line.split(","))) for line in sys.stdin.readlines())


if __name__ == "__main__":
    main(input())
