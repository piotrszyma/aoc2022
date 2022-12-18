# Day 18

from typing import NamedTuple


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
def main():
    cubes: set[Point] = set()
    with open("day18.input.txt", "r") as f:
        for line in f:
            x, y, z = line.strip().split(",")
            cubes.add(Point(int(x), int(y), int(z)))

    count = 0
    for cube in cubes:
        x, y, z = cube
        # Above
        if not Point(x, y, z + 1) in cubes:
            count += 1

        # Below
        if not Point(x, y, z - 1) in cubes:
            count += 1
        # Left
        if not Point(x - 1, y, z) in cubes:
            count += 1

        # Right
        if not Point(x + 1, y, z) in cubes:
            count += 1
        # Behind
        if not Point(x, y - 1, z) in cubes:
            count += 1
        # In front

        if not Point(x, y + 1, z) in cubes:
            count += 1

    print(count)


if __name__ == "__main__":
    main()
