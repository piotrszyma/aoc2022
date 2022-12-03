import functools
import itertools
from typing import Iterable


def get_priority(symbol: str) -> int:
    if symbol.lower() == symbol:  # is lowercase
        # ord(a - z) is from 97 to 122
        return ord(symbol) - 96
    else:  # uppercase
        # ord(A - Z) is from 65 to 90
        return ord(symbol) - 38


def triplets(iterable: Iterable[str]) -> Iterable[tuple[str, str, str]]:
    triplet = tuple()
    for item in iterable:
        triplet = (*triplet, item.strip())

        if len(triplet) == 3:
            yield triplet
            triplet = tuple()


def main():
    with open("day3.input.txt", "r") as f:
        priority_total = 0

        for groups in triplets(f):

            # This one is less readable.
            # [badge] = functools.reduce(
            #     lambda prev_uniq, item: set(prev_uniq) & set(item),
            #     groups[1:],  # Apply all other groups.
            #     set[str](groups[0]),  # Start with set over first group.
            # )

            unique = set(groups[0])
            for group in groups[1:]:
                unique &= set(group)
            [badge] = unique

            priority_total += get_priority(badge)

        print(priority_total)


if __name__ == "__main__":
    main()
