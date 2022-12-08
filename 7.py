from collections import (
    Counter,
)
import sys


def one(dirsizes):
    print(sum(v for v in dirsizes.values() if v <= 100_000))


def two(dirsizes):
    total = 70_000_000
    unused = total - dirsizes[""]
    needed = 30_000_000 - unused

    candidates = []
    for d, s in dirsizes.items():
        if s >= needed:
            candidates.append((d, s))
    candidates.sort(key=lambda p: p[1])
    print(candidates[0][1])


def get_dirsizes(cmds):
    cwd = None
    files = {}
    for cmd, out in cmds:
        if cmd.startswith("cd"):
            dirname = cmd[3:]
            if dirname == "..":
                cwd.pop()
            elif dirname == "/":
                cwd = [""]
            else:
                cwd.append(dirname)
        elif cmd.startswith("ls"):
            for entry in out:
                if entry.startswith("dir"):
                    continue
                sizestr, name = entry.split()
                size = int(sizestr)
                path = "/".join(cwd) + "/" + name
                files[path] = size
        else:
            raise ValueError(f'unknown command "{cmd}"')
    dirsizes = Counter()
    for f, size in files.items():
        path = f
        i = path.rfind("/")
        while i >= 0:
            path = path[:i]
            dirsizes[path] += size
            i = path.rfind("/")
    return dirsizes


def input():
    cmds = []
    lines = [l.strip() for l in sys.stdin.readlines()]
    i = 0
    while i < len(lines):
        cmd = lines[i][2:]
        output = []
        i += 1
        while i < len(lines) and not lines[i].startswith("$"):
            output.append(lines[i])
            i += 1
        cmds.append((cmd, output))
    return get_dirsizes(cmds)


def main(lines):
    one(lines)
    two(lines)


if __name__ == "__main__":
    main(input())
