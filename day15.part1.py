# Day 15
import re
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Scan(NamedTuple):
    sensor: Point
    closest_beacon: Point


RE_LINE = re.compile(
    r"x=(?P<x1>-?\d+).+y=(?P<y1>-?\d+).+x=(?P<x2>-?\d+).+y=(?P<y2>-?\d+)", flags=re.A
)

# Manhattan metric
# dist((x1, y1), (x2, y2)) = abs(x1 - x2) + abs(y1 - y2)

#      2
#    |   |
#  1 2 3 4
# 1        1
# 2  a     2   -
# 3        3     2
# 4      x 4   -
# 5        5


def dist_manh(a: Point, b: Point) -> int:
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)


def main():
    scans: list[Scan] = []
    # SEARCHED_Y = 10
    SEARCHED_Y = 2_000_000

    with open("day15.input.txt", "r") as f:
        for line in f:
            line = line.strip()
            match = RE_LINE.search(line)
            assert match

            x1 = int(match["x1"])
            y1 = int(match["y1"])

            x2 = int(match["x2"])
            y2 = int(match["y2"])

            sensor = Point(x=x1, y=y1)
            beacon = Point(x=x2, y=y2)

            scans.append(Scan(sensor, beacon))

    marked_points: set[Point] = set()

    for scan in scans:
        sensor, beacon = scan.sensor, scan.closest_beacon

        dist = dist_manh(sensor, beacon)

        highest_y = sensor.y - dist  # highest = smallest
        lowest_y = sensor.y + dist  # lowerst = biggest

        if not (highest_y <= SEARCHED_Y <= lowest_y):
            continue

        leftest_x = sensor.x - dist
        rightest_x = sensor.x + dist

        for x in range(leftest_x, rightest_x + 1):
            point_on_y = Point(x, SEARCHED_Y)

            if point_on_y == beacon:
                continue

            dist_x = dist_manh(sensor, point_on_y)
            if dist_x <= dist:
                marked_points.add(point_on_y)

    print(len(marked_points))


if __name__ == "__main__":
    main()
