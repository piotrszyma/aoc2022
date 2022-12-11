# Day 11
import collections
import operator
from typing import Callable, Iterable

DEBUG = False


class Monkey:
    def __init__(
        self,
        monkey_id: int,
        worry_levels: list[int],
        operation: Callable[[int], int],
        test: Callable[[int], bool],
        monkey_id_if_true: int,
        monkey_id_if_false: int,
        diviser: int,
    ):
        self.id = monkey_id
        self.items = worry_levels
        self.operation = operation
        self.test = test
        self.monkey_id_if_true = monkey_id_if_true
        self.monkey_id_if_false = monkey_id_if_false
        self.diviser = diviser

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
            args.append(int(left))
        else:
            args.append(old)

        if right.isnumeric():
            args.append(int(right))
        else:
            args.append(old)

        if args[0] == args[1] and op == operator.mul:
            return args[0] ** 2

        return op(args[0], args[1])

    return operation


def _get_test(line: str) -> tuple[Callable[[int], bool], int]:
    assert "Test: divisible by" in line
    div = line.split("divisible by ")
    div = int(div[1])
    return (lambda x: x % div == 0, div)


def monkey_from_lines(lines: list[str]) -> Monkey:
    monkey_id = _get_monkey_id(lines[0])
    worry_levels = _get_starting_items(lines[1])
    operation = _get_operation(lines[2])
    test, diviser = _get_test(lines[3])
    monkey_if_true = int(lines[4][-1])
    monkey_if_false = int(lines[5][-1])

    return Monkey(
        monkey_id=monkey_id,
        worry_levels=worry_levels,
        operation=operation,
        test=test,
        monkey_id_if_true=monkey_if_true,
        monkey_id_if_false=monkey_if_false,
        diviser=diviser,
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


def print_debug(*args):
    if not DEBUG:
        return

    print(*args)


def main():
    monkeys: list[Monkey] = []
    # Multiply all dividers from test phase.
    divisers = 1
    with open("day11.input.txt", "r") as f:
        for lines in chunked(stripped(f), max_chunk_size=7):
            monkey = monkey_from_lines(lines)
            monkeys.append(monkey)
            divisers *= monkey.diviser

    rounds = 10000
    inspects_count = collections.Counter()

    for r in range(rounds):
        for monkey in monkeys:
            old_items = monkey.items

            for item in old_items:
                inspects_count[monkey.id] += 1
                new_level = monkey.operation(item)

                new_level = new_level - ((new_level // divisers) * divisers)

                if monkey.test(new_level) is True:
                    monkeys[monkey.monkey_id_if_true].items.append(new_level)
                else:
                    monkeys[monkey.monkey_id_if_false].items.append(new_level)

            monkey.items = []
    for monkey in monkeys:
        print_debug(f"Monkey {monkey.id}: {monkey.items}")

    print_debug(inspects_count)
    (k, v1), (v, v2) = inspects_count.most_common(2)
    print(v1 * v2)


if __name__ == "__main__":
    main()
