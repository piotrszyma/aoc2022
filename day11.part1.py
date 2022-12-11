# Day 11
from io import TextIOWrapper
import operator
from typing import Callable, Iterable


class Monkey:
    def __init__(
        self,
        monkey_id: int,
        worry_levels: list[int],
        operation: Callable[[int], int],
        test: Callable[[int], bool],
        monkey_id_if_true: int,
        monkey_id_if_false: int,
    ):
        self.id = monkey_id

    def __repr__(self) -> str:
        return f"Monkey<id={self.id}>"


def _get_monkey_id(line: str) -> int:
    assert line.startswith("Monkey")
    return int(line[-2:-1])


def _get_starting_items(line: str) -> list[int]:
    _, items = line.split(": ")
    items = items.split(", ")
    return [int(i) for i in items]


def _get_operation(line: str) -> Callable[[int], int]:
    _, eq = line.split(" = ")
    left, op_symbol, right = eq.split(" ")
    if op_symbol == "+":
        op = operator.add
    elif op_symbol == "*":
        op = operator.mul
    else:
        raise ValueError(f"unexpected op = {op_symbol}")

    def operation(old: int) -> int:
        args = []
        if left.isnumeric():
            args.append(left)
        else:
            args.append(old)

        if right.isnumeric():
            args.append(right)
        else:
            args.append(old)

        return op(args[0], args[1])

    return operation


def _get_test(line: str) -> Callable[[int], bool]:
    assert "Test: divisible by" in line
    div = line.split("divisible by ")
    div = int(div[1])
    return lambda x: x % div == 0


def monkey_from_lines(lines: list[str]) -> Monkey:
    monkey_id = _get_monkey_id(lines[0])
    start_items = _get_starting_items(lines[1])
    operation = _get_operation(lines[2])
    test = _get_test(lines[3])
    monkey_if_true = int(lines[4][-1])
    monkey_if_false = int(lines[5][-1])

    return Monkey(
        monkey_id=monkey_id,
        worry_levels=[],
        operation=lambda x: x,
        test=lambda x: True,
        monkey_id_if_true=1,
        monkey_id_if_false=1,
    )


def stripped(iterable: Iterable[str]) -> Iterable[str]:
    for item in iterable:
        yield item.strip()


def chunked(iterable: Iterable[str], max_chunk_size: int) -> Iterable[list[str]]:
    chunk = []
    for item in iterable:
        chunk.append(item)

        if len(chunk) == max_chunk_size:
            yield chunk
            chunk = []

    yield chunk


def main():
    monkeys = []
    with open("day11.input.test.txt", "r") as f:
        for lines in chunked(stripped(f), max_chunk_size=7):
            monkey = monkey_from_lines(lines)
            monkeys.append(monkey)


if __name__ == "__main__":
    main()
