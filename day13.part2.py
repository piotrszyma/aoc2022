# Day 13
import json
from functools import cmp_to_key
from typing import Literal

DEBUG = False
Content = int | list["Content"]
Packet = list[Content]
# PacketPair = tuple[Packet, Packet]
# Packets = list[PacketPair]


def print_debug(*args):
    if not DEBUG:
        return

    print(*args)


def comparator(left: Content, right: Content) -> Literal[-1, 0, 1]:
    is_valid = is_valid_order(left, right)
    assert is_valid is not None
    return is_valid


def is_valid_order(left: Content, right: Content, indent=0) -> Literal[-1, 0, 1] | None:
    if left == right:
        return 0

    print_debug("\t" * indent + f"Compare {left} vs {right}")
    t0 = type(left)
    t1 = type(right)

    if t0 != t1:  # One is list other is int.
        left = left if isinstance(left, list) else [left]
        right = right if isinstance(right, list) else [right]
        print_debug(
            "\t" * indent
            + "Mixed types; convert "
            + ("left to " + str(left) if t0 == int else "right to " + str(right))
            + " and retry comparison"
        )
        return is_valid_order(left, right, indent=indent + 1)  # type: ignore
    elif isinstance(left, int) and isinstance(right, int):
        # Both are ints
        if left < right:
            print_debug(
                "\t" * indent
                + "Left side is smaller, so inputs are IN THE RIGHT ORDER 1"
            )
            return -1
        elif left > right:
            print_debug(
                "\t" * indent
                + "Right side is smaller, so inputs are NOT in the right order 1"
            )
            return 1
        else:
            return None
    elif isinstance(left, list) and isinstance(right, list):
        # Both are lists.
        for l, r in zip(left, right):
            res = is_valid_order(l, r, indent=indent + 1)
            if res is not None:
                return res

        if len(right) < len(left):  # right runs out of order first
            print_debug(
                "\t" * indent
                + "Right side run out of items, so inputs are NOT in the right order."
            )
            return 1
        elif len(right) > len(left):  # left runs of order first
            print_debug(
                "\t" * indent
                + "Left side run out of items, so inputs are IN THE RIGHT ORDER"
            )
            return -1
        else:
            return None  # Same length, no way to determine order
    else:
        raise ValueError(f"unexpected comparison {left=}, {right=}")


DIVIDER_1: Content = [[2]]
DIVIDER_2: Content = [[6]]


def main():

    with open("day13.input.txt", "r") as f:
        packets_all: list[Packet] = []

        for line in f:
            line = line.strip()
            if line == "":
                continue

            packet = json.loads(line)
            packets_all.append(packet)
            assert isinstance(packet, list)

        packets_all.append(DIVIDER_1)
        packets_all.append(DIVIDER_2)

        packets_ordered = sorted(packets_all, key=cmp_to_key(comparator))

        idx_1 = packets_ordered.index(DIVIDER_1) + 1
        idx_2 = packets_ordered.index(DIVIDER_2) + 1

        if DEBUG:
            print("\n".join(str(p) for p in packets_ordered))

        print(idx_1 * idx_2)


if __name__ == "__main__":
    main()
