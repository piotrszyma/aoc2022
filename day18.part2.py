# Day 18

from typing import Iterable, NamedTuple


class Point(NamedTuple):
    x: int
    y: int
    z: int


#    ↑
#   z|
#    |
#    |   /
#    |  / y
#    | /
#    ----------> x


def all_around(point: Point) -> Iterable[Point]:
    xp, yp, zp = point
    yield Point(xp, yp, zp - 1)
    yield Point(xp, yp, zp + 1)
    yield Point(xp, yp - 1, zp)
    yield Point(xp, yp + 1, zp)
    yield Point(xp + 1, yp, zp)
    yield Point(xp - 1, yp, zp)


def main():
    cubes: set[Point] = set()
    with open("day18.input.txt", "r") as f:
        for line in f:
            x, y, z = line.strip().split(",")
            cubes.add(Point(int(x), int(y), int(z)))

    min_x = min((c.x for c in cubes)) - 1
    max_x = max((c.x for c in cubes)) + 1

    min_y = min((c.y for c in cubes)) - 1
    max_y = max((c.y for c in cubes)) + 1

    min_z = min((c.z for c in cubes)) - 1
    max_z = max((c.z for c in cubes)) + 1

    to_visit: list[Point] = [Point(min_x, min_y, min_z)]
    visited: set[Point] = set()

    while to_visit:
        p = to_visit.pop()
        assert p not in cubes

        visited.add(p)

        if p.x < min_x or p.x > max_x:
            continue

        if p.y < min_y or p.y > max_y:
            continue

        if p.z < min_z or p.z > max_z:
            continue

        for point in all_around(p):
            if point in cubes:
                # Skip cubes.
                continue
            elif point not in visited:
                to_visit.append(point)

    count = 0
    for cube in cubes:
        x, y, z = cube
        # Above
        p_above = Point(x, y, z + 1)
        if not p_above in cubes and p_above in visited:
            count += 1

        # Below
        p_below = Point(x, y, z - 1)
        if not p_below in cubes and p_below in visited:
            count += 1
        # Left
        p_left = Point(x - 1, y, z)
        if not p_left in cubes and p_left in visited:
            count += 1

        # Right
        p_right = Point(x + 1, y, z)
        if not p_right in cubes and p_right in visited:
            count += 1

        # Behind
        p_behind = Point(x, y - 1, z)
        if not p_behind in cubes and p_behind in visited:
            count += 1

        # In front
        p_in_front = Point(x, y + 1, z)
        if not p_in_front in cubes and p_in_front in visited:
            count += 1

    print(count)


if __name__ == "__main__":
    main()
