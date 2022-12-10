# Day 10


from io import TextIOWrapper
from typing import Callable, Iterable

DEBUG = False


class CPU:
    def __init__(self):
        self.reg_X = 1
        self.cycle = 0


class Cmd:
    def __init__(self, name: str, cycles: int, callback: Callable[[CPU, "Cmd"], None]):
        self.name = name
        self.cycles_left = cycles
        self.callback = callback

    def tick(self):
        self.cycles_left -= 1

    def completed(self):
        return self.cycles_left == 0


def parse_cmd(f: TextIOWrapper) -> Iterable[Cmd]:
    for line in f:
        cmd = line.strip()
        if cmd == "noop":
            yield Cmd(cmd, 1, lambda cpu, cmd: None)
        elif cmd.startswith("addx"):
            _, raw_inc = cmd.split(" ")
            inc = int(raw_inc)

            def cb(cpu: CPU, cmd: Cmd):
                if cmd.cycles_left == 0:
                    cpu.reg_X += inc

            yield Cmd(cmd, 2, cb)


def run_cpu(f: TextIOWrapper):
    cpu = CPU()
    signal_strength_sum = 0
    for cmd in parse_cmd(f):
        while not cmd.completed():
            cpu.cycle += 1

            if (cpu.cycle % 40) == 20:
                if DEBUG:
                    print(
                        cpu.cycle,
                        "cmd",
                        cmd.name,
                        "reg_X",
                        cpu.reg_X,
                        "cmd_cycles_left",
                        cmd.cycles_left,
                        sep="\t",
                    )
                signal_strength_sum += cpu.cycle * cpu.reg_X

            # Apply cycle action.
            cmd.cycles_left -= 1
            cmd.callback(cpu, cmd)
    return signal_strength_sum


def main():
    with open("day10.input.txt", "r") as cmd:
        print(run_cpu(cmd))


if __name__ == "__main__":
    main()
