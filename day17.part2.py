# Day 17

import collections
from typing import Iterable, NamedTuple

DEBUG = True

SHAPE_MINUS = """
####
"""

SHAPE_PLUS = """
.#.
###
.#.
"""

# Shifted due to local coordinate system.
SHAPE_L = """
###
..#
..#
"""

SHAPE_LINE = """
#
#
#
#
"""

SHAPE_SQUARE = """
##
##
"""


class Point(NamedTuple):
    x: int
    y: int


# TODO: cache me
def shape_to_relative_coords(shape: str) -> set[Point]:
    shape_lines = shape.strip().split("\n")
    points: set[Point] = set()
    for y, line in enumerate(shape_lines):
        for x, symb in enumerate(line):
            if symb == "#":
                points.add(Point(x, y))

    return points


def get_next_shape() -> Iterable[str]:
    while True:
        yield SHAPE_MINUS
        yield SHAPE_PLUS
        yield SHAPE_L
        yield SHAPE_LINE
        yield SHAPE_SQUARE


def highest_rock_y(chamber: set[Point]) -> int:
    if len(chamber) == 0:
        return -1  # One below lowest - no rocks in chamber.

    highest_point = max(chamber, key=lambda p: p.y)
    return highest_point.y


def chamber_height(chamber: set[Point]) -> int:
    return highest_rock_y(chamber) + 1


#
#    y
#  3 |..@@@@.|
#  2 |.......|
#  1 |.......|
#  0 |.......|
#    +-------+ x
#     0123456


def get_moves(moves_pattern: list[str]) -> Iterable[str]:
    while True:
        for move in moves_pattern:
            yield move


def apply_shift(point: Point, shift: Point) -> Point:
    x, y = point
    xs, ys = shift
    return Point(x=x + xs, y=y + ys)


def does_collide(
    chamber: set[Point], shape_pos: Point, shape_items_relative: set[Point]
):
    for item in shape_items_relative:
        item_pos = apply_shift(shape_pos, item)
        x, y = item_pos
        if y < 0 or x > 6 or x < 0:
            return True

        if item_pos in chamber:
            return True

    return False


def add_shape_to_chamber(
    chamber: set[Point], shape_pos: Point, shape_items_relative: set[Point]
) -> set[Point]:
    new_chamber = {*chamber}
    for item in shape_items_relative:
        item_pos = apply_shift(shape_pos, item)
        assert item_pos not in new_chamber
        new_chamber.add(item_pos)
    return new_chamber


def debug_print(chamber: set[Point]):
    if not DEBUG:
        return

    highest_y = highest_rock_y(chamber) + 4

    for y in range(highest_y, -1, -1):
        for x in range(7):
            if Point(x, y) in chamber:
                print("#", end="")
            else:
                print(".", end="")
        print()


def probe_pattern(chamber: set[Point], y_start: int, size: int) -> str:
    pattern = []
    for y in range(y_start, y_start + size):
        row = "".join("#" if (x, y) in chamber else "." for x in range(7))
        pattern.append(row)
    return "\n".join(reversed(pattern))


CHAMBER_WIDTH = 7
# TARGET_ROCK_NO = 2022
TARGET_ROCK_NO = 10**12
SHAPES_COUNT = 5


def main():
    moves_pattern = []
    with open("day17.input.test.txt", "r") as f:
        for line in f:
            moves_pattern.extend(list(line.strip()))

    chamber = set()  # Stores rocks that don't move anymore.

    rock_no = 0
    moves = iter(get_moves(moves_pattern))
    starting_pattern = ""
    last_checked = 0
    patterns = {}

    for shape in get_next_shape():
        rock_no += 1

        if rock_no == TARGET_ROCK_NO + 1:
            break

        shape_items_relative = shape_to_relative_coords(shape)

        # Each rock appears so that its left edge is two units away from the
        # left wall and its bottom edge is three units above the highest rock in
        # the room (or the floor, if there isn't one).
        x = 2
        y = highest_rock_y(chamber) + 4
        shape_pos = Point(x, y)

        while True:
            # debug_print(add_shape_to_chamber(chamber, shape_pos, shape_items_relative))
            # input()

            current_move = next(moves)
            if current_move == "<":
                shift = Point(x=-1, y=0)
            else:
                assert current_move == ">"
                shift = Point(x=1, y=0)

            shape_pos_after_shift = apply_shift(shape_pos, shift)
            collides = does_collide(
                chamber, shape_pos_after_shift, shape_items_relative
            )
            if not collides:  # Apply move only if shape does not collide in result.
                shape_pos = shape_pos_after_shift

            shape_pos_after_moving_down = apply_shift(shape_pos, Point(x=0, y=-1))
            collides = does_collide(
                chamber, shape_pos_after_moving_down, shape_items_relative
            )

            if not collides:  # No collides - nothing hit - can move further.
                shape_pos = shape_pos_after_moving_down
                continue

            # PATTERN CHECKER SECTION START

            # ...#...
            # ..###..
            # ...#...
            # ..####.
            # ....###
            # .#..###
            # .#.####
            # .####..
            # .#.#...
            # .####..

            diff = 50
            size = 5

            # TODO: Find cycle.
            if shape_pos.y > diff:
                while last_checked <= shape_pos.y - diff:
                    y = last_checked
                    current_pattern = probe_pattern(chamber, y, size)
                    if current_pattern not in patterns:
                        print(y)
                        print(current_pattern)
                        print(f"{rock_no=}")
                        print("height", chamber_height(chamber))
                        print(set(patterns.values()))
                        print({k: v for (k, v) in patterns.items() if v < 2})
                        ones = sum((1 for v in patterns.values() if v == 1))
                        print(f"{ones=}")

                    patterns[current_pattern] = patterns.get(current_pattern, 0) + 1
                    last_checked += 1

            # PATTERN CHECKER SECTION END

            # In this case shape after move hit something - so this is final position of shape.
            # Add this shape to chamber

            chamber = add_shape_to_chamber(chamber, shape_pos, shape_items_relative)

            # and move forward to next shape.
            break
    highest_y = highest_rock_y(chamber) + 1
    print(highest_y)


if __name__ == "__main__":
    assert shape_to_relative_coords(SHAPE_L) == set(
        (
            Point(x=0, y=0),
            Point(x=1, y=0),
            Point(x=2, y=0),
            Point(x=2, y=1),
            Point(x=2, y=2),
        )
    )
    main()
