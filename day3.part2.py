from typing import Iterable


def get_priority(symbol: str) -> int:
    if symbol.lower() == symbol:  # is lowercase
        # ord(a - z) is from 97 to 122
        return ord(symbol) - 96
    else:  # uppercase
        # ord(A - Z) is from 65 to 90
        return ord(symbol) - 38


def triplets(iterable: Iterable[str]) -> Iterable[list[str]]:
    triplet = []
    for item in iterable:
        triplet.append(item.strip())

        if len(triplet) == 3:
            yield triplet
            triplet = []


def main():
    with open("day3.input.txt", "r") as f:
        priority_total = 0

        for (first, second, third) in triplets(f):
            first_uniq = set(first)
            second_uniq = set(second)
            third_uniq = set(third)
            [common_item] = first_uniq & second_uniq & third_uniq

            priority_total += get_priority(common_item)

        print(priority_total)


if __name__ == "__main__":
    main()
