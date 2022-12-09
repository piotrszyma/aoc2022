# Day 9
from io import TextIOWrapper
from typing import Iterable, Literal, cast

Move = Literal["U", "D", "L", "R"]


def is_adjancent(p1: tuple[int, int], p2: tuple[int, int]) -> bool:
    (x1, y1), (x2, y2) = p1, p2
    return (
        (x1 == x2 and y1 == y2)
        or (x1 == x2 and abs(y1 - y2) == 1)
        or (y1 == y2 and abs(x1 - x2) == 1)  # same row
        or (abs(x1 - x2) == abs(y1 - y2) == 1)  # same col  # diagonally adjacent
    )


def apply_move(
    pos: tuple[int, int],
    move: Move,
) -> tuple[int, int]:
    (row, col) = pos
    match move:
        case "U":
            return (row - 1, col)
        case "D":
            return (row + 1, col)
        case "L":
            return (row, col - 1)
        case "R":
            return (row, col + 1)

    raise ValueError(f"unexpected move {move}")


def consume_moves(moves: Iterable[Move]) -> set[tuple[int, int]]:
    H = (0, 0)
    T = (0, 0)
    visited_by_tail = set()
    visited_by_tail.add(T)
    for move in moves:
        old_H = H
        old_T = T

        new_H = apply_move(old_H, move)
        if is_adjancent(new_H, old_T):
            new_T = old_T
        else:
            new_T = old_H

        visited_by_tail.add(new_T)
        T = new_T
        H = new_H

    return visited_by_tail


def moves_from_lines(file: TextIOWrapper) -> Iterable[Move]:
    for line in file:
        move, count = line.strip().split(" ")
        count = int(count)
        for _ in range(count):
            assert move in {"U", "D", "L", "R"}
            yield cast(Move, move)


def main():
    with open("day9.input.txt", "r") as f:
        visited_by_tail = consume_moves(moves_from_lines(f))

    print(len(visited_by_tail))


if __name__ == "__main__":
    main()
