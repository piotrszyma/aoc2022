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


def is_diagonal(p1: tuple[int, int], p2: tuple[int, int]) -> bool:
    (x1, y1), (x2, y2) = p1, p2
    return abs(x1 - x2) == 2 or abs(y1 - y2) == 2


def consume_moves(moves: Iterable[Move]) -> set[tuple[int, int]]:
    rope: list[tuple[int, int]] = [(0, 0) for _ in range(10)]

    visited_by_last = set()
    visited_by_last.add(rope[-1])

    for move in moves:
        old_rope = [*rope]
        old_H = rope[0]
        old_T = rope[1]
        new_H = apply_move(old_H, move)

        if is_adjancent(new_H, old_T):
            new_T = old_T
        else:
            new_T = old_H

        rope[0] = new_H
        rope[1] = new_T
        # print_state(rope)
        # print(rope)
        # input()

        for idx, _ in enumerate(rope[:-1]):
            if idx == 0:
                continue

            old_H = old_rope[idx]
            old_T = old_rope[idx + 1]
            new_H = rope[idx]  # Head was moved in previous iteration step.
            # if idx == 1:
            #     breakpoint()

            if is_adjancent(new_H, old_T):
                new_T = old_T
            elif is_diagonal(new_H, old_T):  # non adjacent & diagonal move
                # breakpoint()
                x1, y1 = old_H
                x2, y2 = new_H
                x_diff = x2 - x1
                y_diff = y2 - y1
                x3, y3 = old_T
                new_T = x3 + x_diff, y3 + y_diff
            else:
                new_T = old_H

            rope[idx] = new_H
            rope[idx + 1] = new_T

        # breakpoint()  # After iteration
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

DIMS = 10


def print_state(rope: list[tuple[int, int]]):
    rope_m = {}
    for idx, pos in enumerate(rope):
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
