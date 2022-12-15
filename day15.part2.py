# Day 15
import collections
import re
from typing import NamedTuple, cast


class Point(NamedTuple):
    x: int
    y: int


class Scan(NamedTuple):
    sensor: Point
    closest_beacon: Point


class Range(NamedTuple):
    start: int
    end: int

    def __contains__(self, x: int) -> bool:
        return self.start <= x <= self.end


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


def add_range(ranges: list[Range], range: Range) -> list[Range]:
    if len(ranges) == 0:
        return [range]

    ranges_smaller = []
    ranges_bigger = []
    colliding_start = range.start
    colliding_end = range.end
    has_colliding = False

    for r in ranges:
        if r.end < range.start:
            ranges_smaller.append(r)
        elif r.start > range.end:
            ranges_bigger.append(r)
        else:
            has_colliding = True
            colliding_start = min(colliding_start, r.start)
            colliding_end = max(colliding_end, r.end)

    new_ranges = [*ranges_smaller]

    if not has_colliding:
        new_ranges.append(range)
    else:
        new_ranges.append(Range(colliding_start, colliding_end))

    new_ranges.extend(ranges_bigger)

    return new_ranges


def dist_manh(a: Point, b: Point) -> int:
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)


def in_any(ranges: list[Range], x: int) -> bool:
    for r in ranges:
        if x in r:
            return True
    return False


def main():
    scans: list[Scan] = []
    coord_min, coord_max = 0, 4_000_000
    # coord_min, coord_max = 0, 20

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

    marked_ranges: dict[int, list[Range]] = collections.defaultdict(list)

    for idx, scan in enumerate(scans):
        print("scan", idx + 1)
        sensor, beacon = scan.sensor, scan.closest_beacon

        dist = dist_manh(sensor, beacon)

        highest_y = sensor.y - dist  # highest = smallest
        lowest_y = sensor.y + dist  # lowerst = biggest

        leftest_x = sensor.x - dist  # leftest = smallest
        rightest_x = sensor.x + dist  # rightest = biggest

        mid_y = sensor.y
        mid_x = sensor.x

        marked_ranges[mid_y] = add_range(
            marked_ranges[mid_y], Range(leftest_x, rightest_x)
        )

        shift = 0
        while True:
            leftest_x += 1
            rightest_x -= 1

            if leftest_x > rightest_x:
                break

            shift += 1

            if coord_min <= mid_y + shift <= coord_max:
                marked_ranges[mid_y + shift] = add_range(
                    marked_ranges[mid_y + shift], Range(leftest_x, rightest_x)
                )

            if coord_min <= mid_y - shift <= coord_max:
                marked_ranges[mid_y - shift] = add_range(
                    marked_ranges[mid_y - shift], Range(leftest_x, rightest_x)
                )

    for y, x_ranges in marked_ranges.items():
        if len(x_ranges) > 1:
            assert len(x_ranges) == 2
            r1, _ = x_ranges
            x = r1.end + 1
            print(x * 4000000 + y)


if __name__ == "__main__":
    main()
