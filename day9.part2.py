# Day 9
from io import TextIOWrapper
from typing import Iterable, Literal, cast

Move = Literal["U", "D", "L", "R"]


def is_adjancent(p1: tuple[int, int], p2: tuple[int, int]) -> bool:
    (x1, y1), (x2, y2) = p1, p2
    return (
        (x1 == x2 and y1 == y2)
        or (x1 == x2 and abs(y1 - y2) == 1)  # same row
        or (y1 == y2 and abs(x1 - x2) == 1)  # same col
        or (abs(x1 - x2) == abs(y1 - y2) == 1)  # diagonally adjacent
    )


def is_non_diagonal_non_adjacent(p1: tuple[int, int], p2: tuple[int, int]):
    (x1, y1), (x2, y2) = p1, p2
    vertical = abs(x1 - x2) == 2 and abs(y1 - y2) == 0
    horizontal = abs(x1 - x2) == 0 and abs(y1 - y2) == 2

    return horizontal or vertical


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


def is_diagonal(p1: tuple[int, int], p2: tuple[int, int]) -> bool:
    (x1, y1), (x2, y2) = p1, p2
    return abs(x1 - x2) == 2 and abs(y1 - y2) == 2


def is_non_diagonal_move(p1: tuple[int, int], p2: tuple[int, int]) -> bool:
    (x1, y1), (x2, y2) = p1, p2
    return (x1 == x2 and y1 != y2) or (x1 != x2 and y1 == y2)


def move_rope(rope: list[tuple[int, int]], move: Move) -> list[tuple[int, int]]:
    old_rope = [*rope]

    old_H = rope[0]
    new_H = apply_move(old_H, move)
    rope[0] = new_H

    for idx, _ in enumerate(rope[:-1]):
        old_H = old_rope[idx]
        old_T = rope[idx + 1]

        new_H = rope[idx]
        if is_adjancent(new_H, old_T):
            new_T = old_T
        elif is_non_diagonal_non_adjacent(new_H, old_T):
            new_T = old_H
        else:
            new_T = old_H

        rope[idx + 1] = new_T
    return rope


LEN = 10
DIMS = 6


def consume_moves(moves: Iterable[Move]) -> set[tuple[int, int]]:
    rope: list[tuple[int, int]] = [(0, 0) for _ in range(LEN)]

    visited_by_last = set()
    visited_by_last.add(rope[-1])

    for move_num, move in enumerate(moves):
        rope = move_rope(rope, move)
        visited_by_last.add(rope[-1])
        print_state(rope)
        print(rope)
        input()

    return visited_by_last


def moves_from_lines(file: TextIOWrapper) -> Iterable[Move]:
    for line in file:
        move, count = line.strip().split(" ")
        count = int(count)
        for _ in range(count):
            assert move in {"U", "D", "L", "R"}
            yield cast(Move, move)


# ......
# ......
# ......
# ....H.
# 4321..  (4 covers 5, 6, 7, 8, 9, s)

# ......
# ......
# ....H.
# ....1.
# 432...  (4 covers 5, 6, 7, 8, 9, s)

# ......
# ......
# ....H.
# ...21.
# 43....  (4 covers 5, 6, 7, 8, 9, s)


# ......
# ......
# ....H.
# .4321.
# 5.....  (5 covers 6, 7, 8, 9, s)

# ......
# ....H.
# ....1.
# .432..
# 5.....  (5 covers 6, 7, 8, 9, s)

# ....H.
# ....1.
# ..432.
# .5....
# 6.....  (6 covers 7, 8, 9, s)


def print_state(rope: list[tuple[int, int]]):
    rope_m = {}
    for idx, pos in enumerate(rope):
        if pos in rope_m:
            continue
        rope_m[pos] = idx

    dims = DIMS
    for x in range(-dims, dims):
        for y in range(-dims, dims):
            if (x, y) in rope_m:
                s = rope_m[(x, y)]
                if s == 0:
                    s = "H"
                print(s, end="")
            else:
                print(".", end="")
        print("")

    # print(rope)


def main():
    with open("day9.input.test.txt", "r") as f:
        visited_by_tail = consume_moves(moves_from_lines(f))

    # print(len(visited_by_tail))

    # dims = DIMS
    # for x in range(-dims, dims):
    #     for y in range(-dims, dims):
    #         if (x, y) in visited_by_tail:
    #             print("X", end="")
    #         else:
    #             print(" ", end="")
    #     print("")


if __name__ == "__main__":
    main()
