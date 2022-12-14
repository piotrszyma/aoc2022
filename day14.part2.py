# Day 14
import enum
from typing import Iterable

DEBUG = True


class Type(enum.Enum):
    ROCK = "rock"
    SAND = "sand"
    AIR = "air"


Point = tuple[int, int]


def slides(items: list[str], size=1) -> Iterable[list[str]]:
    idx = 0
    while idx + size < len(items) + 1:
        yield items[idx : idx + size]
        idx += 1


def points_from_line(line: str) -> Iterable[Point]:
    points = line.split(" -> ")
    for start, end in slides(points, 2):
        xs, ys = (int(n) for n in start.split(","))
        xe, ye = (int(n) for n in end.split(","))

        if xs != xe:
            if xs < xe:
                while xs <= xe:
                    yield (xs, ys)
                    xs += 1
            else:
                while xs >= xe:
                    yield (xs, ys)
                    xs -= 1
        else:
            if ys < ye:
                while ys <= ye:
                    yield (xs, ys)
                    ys += 1
            else:
                while ys >= ye:
                    yield (xs, ys)
                    ys -= 1


#   4     5  5
#   9     0  0  <-- cols
#   4     0  3
# 0 ......+...
# 1 ..........
# 2 ..........
# 3 ..........
# 4 ....#...##
# 5 ....#...#.
# 6 ..###...#.
# 7 ........#.
# 8 ........#.
# 9 #########.
# /\
# rows


def next_sand_pos(cave: dict[Point, Type], start: Point, floor_y: int) -> Point:
    x, y = start

    while True:
        direct = cave.get((x, y + 1), Type.AIR)
        left_diag = cave.get((x - 1, y + 1), Type.AIR)
        right_diag = cave.get((x + 1, y + 1), Type.AIR)
        # TODO: check for these cases?
        # left = cave.get((x - 1, y), Type.AIR)
        # right = cave.get((x + 1, y), Type.AIR)

        if y == floor_y - 1:
            break

        if direct == Type.AIR:
            y += 1
        elif left_diag == Type.AIR:
            y += 1
            x -= 1
        elif right_diag == Type.AIR:
            y += 1
            x += 1
        else:
            break

    return (x, y)


def print_sand(cave: dict[Point, Type]):
    min_x = min(p[0] for p in cave.keys())
    max_x = max(p[0] for p in cave.keys())
    min_y = min(p[1] for p in cave.keys())
    max_y = max(p[1] for p in cave.keys())

    board = []
    for y in range(min_y - 1, max_y + 1):
        row = []
        for x in range(min_x - 1, max_x + 1):
            p = cave.get((x, y), Type.AIR)
            if p == Type.ROCK:
                row.append("#")
            elif p == Type.SAND:
                row.append("o")
            else:
                row.append(".")
        board.append("".join(row))

    print("\n".join(board))


def main():
    cave: dict[Point, Type] = {}
    start: Point = (500, 0)
    x, y = start
    deepest_y = y

    with open("day14.input.txt", "r") as f:
        for line in f:
            for point in points_from_line(line.strip()):
                cave[point] = Type.ROCK
                x, y = point
                deepest_y = max(deepest_y, y)

    count = 0
    while True:
        next_sand = next_sand_pos(cave, start, floor_y=deepest_y + 2)

        cave[next_sand] = Type.SAND
        count += 1

        if next_sand == start:
            break

        if DEBUG:
            print_sand(cave)
            input()

    print(count)


if __name__ == "__main__":

    res = list(points_from_line("503,4 -> 502,4 -> 502,9"))
    assert res == [
        (503, 4),
        (502, 4),
        (502, 4),
        (502, 5),
        (502, 6),
        (502, 7),
        (502, 8),
        (502, 9),
    ], res
    res = list(points_from_line("1,1 -> 2,1"))
    assert res == [(1, 1), (2, 1)], res

    res = list(points_from_line("1,1 -> 4,1"))
    assert res == [(1, 1), (2, 1), (3, 1), (4, 1)], res

    res = list(points_from_line("1,1 -> 1,4"))
    assert res == [(1, 1), (1, 2), (1, 3), (1, 4)], res

    res = list(points_from_line("1,1 -> 1,1"))
    assert res == [(1, 1)], res

    main()
