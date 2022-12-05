# Day 5

from dataclasses import dataclass
from typing import Iterable, Iterator


@dataclass
class Command:
    source: int
    target: int
    count: int


class Stack:
    def __init__(self):
        self.items: list[str] = []

    def push(self, value: str):
        self.items.append(value)

    def pop(self) -> str:
        return self.items.pop()


class Stacks:
    def __init__(self, count: int):
        self.stacks = [Stack() for _ in range(count)]

    def at(self, idx: int) -> Stack:
        return self.stacks[idx]

    def move(self, command: Command):
        for _ in range(command.count):
            item = self.at(command.source).pop()
            self.at(command.target).push(item)


def split_cols(line: str) -> Iterable[str]:
    idx = 0
    while True:
        yield line[idx : idx + 4]
        idx += 4


def get_row_items(line: str) -> Iterable[str | None]:
    idx = 0
    while idx < len(line) - 1:
        if line[idx] == "[":
            yield line[idx + 1 : idx + 2]
            idx += 4
        elif line[idx] == " ":
            yield None
            idx += 4


def get_command(line: str) -> Command:
    _, count, _, source, _, target = line.split(" ")
    return Command(count=int(count), source=int(source) - 1, target=int(target) - 1)


def newline_stripped(lines: Iterator[str]) -> Iterator[str]:
    for line in lines:
        yield line.replace("\n", "")


def main():
    with open("day5.input.txt", "r") as file:
        lines = newline_stripped(iter(file))
        initial_values: list[list[str | None]] | None = None

        while True:
            line = next(lines)
            if "[" not in line:
                break

            items_in_line = list(get_row_items(line))

            initial_values = initial_values or [[] for _ in items_in_line]

            for idx, item in enumerate(items_in_line):
                initial_values[idx].append(item)

        assert initial_values

        stacks = Stacks(len(initial_values))
        for idx, initial in enumerate(initial_values):
            initial = reversed(initial)
            for item in initial:
                if item is None:
                    continue

                stacks.at(idx).push(item)

        for line in lines:
            if line == "":
                continue

            command = get_command(line)

            stacks.move(command)

        print("".join(s.items[-1] for s in stacks.stacks))


if __name__ == "__main__":
    main()
