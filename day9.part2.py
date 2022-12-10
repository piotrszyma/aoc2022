# Day 9
from io import TextIOWrapper
from typing import Iterable, Literal, cast

LEN = 10
DIMS = 15
DEBUG = False

Move = Literal["U", "D", "L", "R"]


def is_adjacent(p1: tuple[int, int], p2: tuple[int, int]) -> bool:
    (x1, y1), (x2, y2) = p1, p2
    return (
        (x1 == x2 and y1 == y2)  # same pos
        or (x1 == x2 and abs(y1 - y2) == 1)  # same row
        or (y1 == y2 and abs(x1 - x2) == 1)  # same col
        or (abs(x1 - x2) == abs(y1 - y2) == 1)  # diagonally adjacent
    )


def head_moved_diagonally(p1: tuple[int, int], p2: tuple[int, int]) -> bool:
    (x1, y1), (x2, y2) = p1, p2
    return abs(x1 - x2) == abs(y1 - y2) == 1


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


def move_rope(rope: list[tuple[int, int]], move: Move) -> list[tuple[int, int]]:
    old_rope = [*rope]

    old_H = rope[0]
    new_H = apply_move(old_H, move)
    rope[0] = new_H

    for idx, _ in enumerate(rope[:-1]):
        old_H = old_rope[idx]
        old_T = rope[idx + 1]

        new_H = rope[idx]
        if is_adjacent(new_H, old_T):
            new_T = old_T
        elif head_moved_diagonally(old_H, new_H):
            xh0, yh0 = old_H
            xh1, yh1 = new_H

            xh_d = xh1 - xh0
            yh_d = yh1 - yh0

            xt0, yt0 = old_T

            xt1 = xt0 + (xh_d if xh1 != xt0 else 0)
            yt1 = yt0 + (yh_d if yh1 != yt0 else 0)

            new_T = (xt1, yt1)
        else:
            new_T = old_H

        rope[idx + 1] = new_T
    return rope


def consume_moves(moves: Iterable[Move]) -> set[tuple[int, int]]:
    rope: list[tuple[int, int]] = [(0, 0) for _ in range(LEN)]

    visited_by_last = set()
    visited_by_last.add(rope[-1])

    for move_num, move in enumerate(moves):
        print_state(rope)
        rope = move_rope(rope, move)
        visited_by_last.add(rope[-1])

    return visited_by_last


def moves_from_lines(file: TextIOWrapper) -> Iterable[Move]:
    for line in file:
        move, count = line.strip().split(" ")
        count = int(count)
        for _ in range(count):
            assert move in {"U", "D", "L", "R"}
            yield cast(Move, move)


def print_state(rope: list[tuple[int, int]]):
    if not DEBUG:
        return

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

    print(rope)
    input()


def main():
    with open("day9.input.txt", "r") as f:
        visited_by_tail = consume_moves(moves_from_lines(f))

    print(len(visited_by_tail))


if __name__ == "__main__":
    main()
