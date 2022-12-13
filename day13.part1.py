# Day 13
import json

DEBUG = False
Content = int | list["Content"]
Packet = list[Content]
# PacketPair = tuple[Packet, Packet]
# Packets = list[PacketPair]


def print_debug(*args):
    if not DEBUG:
        return

    print(*args)


def is_valid_order(left: Content, right: Content, indent=0) -> bool | None:
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
            return True
        elif left > right:
            print_debug(
                "\t" * indent
                + "Right side is smaller, so inputs are NOT in the right order 1"
            )
            return False
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
            return False
        elif len(right) > len(left):  # left runs of order first
            print_debug(
                "\t" * indent
                + "Left side run out of items, so inputs are IN THE RIGHT ORDER"
            )
            return True
        else:
            return None  # Same length, no way to determine order
    else:
        raise ValueError(f"unexpected comparison {left=}, {right=}")


def main():

    with open("day13.input.txt", "r") as f:
        packets_all: list[list[Packet]] = []
        packets_chunk: list[Packet] = []

        for line in f:
            line = line.strip()
            if line == "":
                packets_all.append(packets_chunk)
                packets_chunk = []
                continue

            packet = json.loads(line)
            packets_chunk.append(packet)
            assert isinstance(packet, list)

        if packets_chunk:
            packets_all.append(packets_chunk)

        idx_sum = 0
        for idx, packets in enumerate(packets_all):
            assert len(packets) == 2
            left, right = packets

            print_debug(f"Pair == {idx + 1} ==")
            is_valid = is_valid_order(left, right)
            assert is_valid is not None

            if is_valid:
                idx_sum += idx + 1

        print(idx_sum)


if __name__ == "__main__":
    main()
