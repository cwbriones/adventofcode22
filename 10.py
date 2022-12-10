import os
import sys

if os.environ.get("DEBUG"):
    def debug(msg):
        print('[DEBUG]: ', end='', file=sys.stderr)
        print(msg, file=sys.stderr)
else:
    def debug(_msg):
        pass


def one(commands):
    signal = 0
    def update_signal(cycle, x):
        nonlocal signal
        if cycle == 20 or (cycle - 20) % 40 == 0:
            debug(f'{cycle}, {x} -> {cycle * x}')
            signal += cycle * x
    run_commands(commands, update_signal)
    print(signal)


def two(commands):
    screen = [False for _ in range(240)]

    def update_screen(cycle, x):
        sprite = (x-1, x, x+1)
        screen[cycle-1] = (cycle-1)%40 in sprite
        if cycle > 50:
            return
        # debug info for earlier cycles
        sprite_row = ['.' for _ in range(40)]
        sprite_row[x] = '#'
        sprite_row[x-1] = '#'
        sprite_row[x+1] = '#'

        row = ''.join('#' if p else '.' for p in screen[40*((cycle-1) // 40):cycle])
        debug(f"{cycle, x}      Sprite: {''.join(sprite_row)}")
        debug(f"{cycle, x}        Draw: {'#' if screen[cycle-1] else '.'}")
        debug(f"{cycle, x} Current row: {row}")
        debug('')

    run_commands(commands, update_screen)

    it = ('#' if p else ' ' for p in screen)
    for row in zip(*([it] * 40)):
        print(''.join(row))

def run_commands(commands, update):
    cycle, x = 1, 1
    for cmd in commands:
        if cmd == 'noop':
            update(cycle, x)
            cycle += 1
        elif cmd.startswith('addx'):
            update(cycle, x)
            update(cycle+1, x)
            cycle += 2
            x += int(cmd[5:])
        else:
            raise ValueError(f'unknown command {cmd}')


def input():
    return [line.strip() for line in sys.stdin.readlines()]


def main(commands):
    one(commands)
    two(commands)


if __name__ == "__main__":
    main(input())
