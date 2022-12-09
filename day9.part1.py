# Day 9


# H
# T

#  0 1 2 <-- col_id
# 0
# 1
# 2
# /\
# row_id

#
# H
# T
#
# H (-1, 0) --> T (-1, 0)
# T (_, _) --> T (0, 0)
#

#
#  H
# T
#
# H (-1, 0) --> T(-1, 1)
# H (0, 1) --> T()

# if is_adjacent(new_head_pos,
import collections
from io import TextIOWrapper
from typing import Iterable, Literal, cast

Move = Literal["U", "D", "L", "R"]


def is_adjancent(p1: tuple[int, int], p2: tuple[int, int]) -> bool:
    (x1, y1), (x2, y2) = p1, p2
    return (
        (x1 == x2 and abs(y1 - y2) == 1)
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
            assert row > 0
            return (row - 1, col)
        case "D":
            return (row + 1, col)
        case "L":
            assert col > 0
            return (row, col - 1)
        case "R":
            return (row, col + 1)

    raise ValueError(f"unexpected move {move}")


def consume_moves(moves: Iterable[Move]):
    H = (0, 0)
    T = (0, 0)
    visited_by_tail = collections.Counter()
    visited_by_tail[T] = 1
    for move in moves:
        old_H = H
        old_T = T

        new_H = apply_move(old_H, move)
        if is_adjancent(new_H, old_T):
            new_T = old_T
        else:
            new_T = old_H

        x, y = new_T
        assert x >= 0
        assert y >= 0
        visited_by_tail[new_T] += 1
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
    with open("day9.input.test.txt", "r") as f:
        visited_by_tail = consume_moves(moves_from_lines(f))
        breakpoint()
        breakpoint()


if __name__ == "__main__":
    main()
