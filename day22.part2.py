# Day 22
from collections import defaultdict
import re
from typing import DefaultDict, Literal, NamedTuple, Union


class Point(NamedTuple):
    row_idx: int
    col_idx: int


Path = list[Union[int, str]]
Fields = dict[Point, str]
Direction = Literal['>', 'v', '<', '^']

RE_PATHCMD = re.compile(r"(\d+|[LR])")

def _next_point(point: Point, direction: Direction) -> Point:
    row_idx, col_idx = point
    if direction == '>':
        return Point(row_idx=row_idx, col_idx=col_idx + 1)
    elif direction == '<':
        return Point(row_idx=row_idx, col_idx=col_idx - 1)
    elif direction == 'v':
        return Point(row_idx=row_idx + 1, col_idx=col_idx)
    elif direction == '^':
        return Point(row_idx=row_idx - 1, col_idx=col_idx)
    else:
        raise ValueError(f"unexpected {direction=}")

def _next_direction(into: Literal['R', 'L'], dir: Direction) -> Direction:
    if dir == '>':
        if into == 'R':
            return 'v'
        elif into == 'L':
            return '^'
    if dir == 'v':
        if into == 'R':
            return '<'
        elif into == 'L':
            return '>'
    if dir == '<':
        if into == 'R':
            return '^'
        elif into == 'L':
            return 'v'
    if dir == '^':
        if into == 'R':
            return '>'
        elif into == 'L':
            return '<'

    raise ValueError(f"unexpected {into=} and {dir=}")

def _parse_path(line: str) -> Path:
    result: list[str] = RE_PATHCMD.findall(line)

    path: Path = []

    for group in result:
        if group.isdigit():
            for _ in range(int(group)):
                path.append(1)
        else:
            path.append(group)

    return path


def build_mapping(
    dir: Direction,
    from_: Point,
    from_inc: Point,
    into: Point,
    into_inc: Point,
    size: int
    ):
    fx, fy = from_
    fxi, fyi = from_inc
    ix, iy = into
    ixi, iyi = into_inc
    mapping = {}
    for _ in range(size):
        mapping[(fx, fy, dir)] = (ix, iy)
        fx += fxi
        fy += fyi
        ix += ixi
        iy += iyi
    return mapping

def generate_mapping(source: tuple[int, int, str], target: tuple[int, int, str], size=50) -> dict[Point, Point]:
    row_g_s, col_g_s, dir_s = source
    row_g_e, col_g_e, dir_e = target

    row_s = row_g_s * size
    if dir_s == 'v':
        row_s = row_s + size - 1

    col_s = col_g_s * size
    if dir_s == '>':
        col_s = col_s + size - 1

    row_e = row_g_e * size
    if row_e == 'v':
        row_e = row_e + size - 1

    col_e = col_g_e * size
    if col_e == '>':
        col_e = col_e + size - 1

    mapping = {}

    for _ in range(size):
        mapping[(row_s, col_s)] = (row_e, col_e)
        if dir_s in '^v':
            col_s += 1
        else:
            row_s += 1

        if dir_e in '^v':
            col_e += 1
        else:
            row_e += 1

    return mapping

def generate_all_mapping():
    #        +------+------+
    #        |  g   |   e  |
    #        |f     |     d|
    #        |      |  b   |
    #        +------+------+
    #        |      |
    #        |a    b|
    #        |      |
    # +------+------+
    # |   a  |      |
    # |f     |     d|
    # |      |   c  |
    # +------+------+
    # |      |
    # |g    c|
    # |   e  |
    # +------+
    a = (1, 1, '<'), (2, 0, '^')
    b = (0, 2, 'v'), (1, 1, '>')
    c = (2, 1, 'v'), (3, 0, '>')
    d = (2, 1, '>'), (0, 2, '>')
    e = (0, 2, '^'), (3, 0, 'v')
    f = (0, 1, '<'), (2, 0, '<')
    g = (0, 1, '^'), (3, 0, '<')

    mapping = {}

    for x in (a, b, c, d, e, f, g):
        f, s = x
        mapping.update(generate_mapping(f, s))
        mapping.update(generate_mapping(s, f))

    return mapping

MAPPING = generate_all_mapping()

def _get_next_wrapped_final(
    curr_point: Point,
) -> Point:

    row_idx, col_idx = MAPPING[(curr_point.row_idx, curr_point.col_idx)]
    return Point(row_idx=row_idx, col_idx=col_idx)


def _get_next_wrapped(
    points_in_row: dict[int, list[Point]],
    points_in_col: dict[int, list[Point]],
    curr_point: Point,
    dir: Direction,
) -> Point:
    return _get_next_wrapped_final(curr_point)

def main():
    fields: dict[Point, str] = {}
    path: Path | None = None
    start: Point | None = None

    points_in_row: DefaultDict[int, list[Point]] = defaultdict(list)
    points_in_col: DefaultDict[int, list[Point]] = defaultdict(list)

    min_row, max_row = 10**12, -1
    min_col, max_col = 10**12, -1

    with open("day22.input.txt", "r") as f:
        for row_idx, raw_line in enumerate(f):
            min_row = min(min_row, row_idx)
            max_row = max(max_row, row_idx)

            line = raw_line.strip('\n')

            if line == "":
                continue

            if line[0].isdigit():
                path = _parse_path(line)
                continue

            for col_idx, cell in enumerate(line):
                min_col = min(min_col, col_idx)
                max_col = max(max_col, col_idx)

                if cell == " ":
                    continue

                point = Point(row_idx, col_idx)
                points_in_col[col_idx].append(point)
                points_in_row[row_idx].append(point)

                if cell == "#":
                    fields[point] = "#"
                    continue

                if cell == ".":
                    if start is None:
                        start = point
                    fields[point] = "."
                    continue

    assert path is not None
    assert start is not None

    def _handle_wrap(fields: Fields, pos: Point, dir: Direction) ->tuple[Point, Direction]:
        next_pos = _get_next_wrapped(points_in_row, points_in_col, pos, dir)
        on_next_pos = fields.get(next_pos)
        if on_next_pos is None:
            raise ValueError("this cannot happen - wrap found on wrap?") # remove if not raised
        elif on_next_pos == '#':
            return _handle_wall(fields, pos, dir, from_wrap=True)
        elif on_next_pos == '.':
            return next_pos, dir
        else:
            raise ValueError("unexpected")

    def _handle_wall(fields: Fields, pos: Point, dir: Direction, from_wrap=False) -> tuple[Point, Direction]:
        return pos, dir
        # if from_wrap:
        #     dir = _invert(dir) # Invert.
        #     return pos, dir
        # dir = _invert(dir) # Invert.

        # next_pos = _next_point(pos, dir)
        # on_next_pos = fields.get(next_pos)

        # if on_next_pos is None:
        #     next_pos = _get_next_wrapped(points_in_row, points_in_col, pos, dir)
        #     on_next_pos = fields.get(next_pos)
        #     if on_next_pos is None:
        #         raise ValueError("this cannot happen - wrap found on wrap?")
        #     elif on_next_pos == '#':
        #         raise ValueError("this cannot happen - wall found on wrap?")
        #     elif on_next_pos == '.':
        #         return pos, dir
        #     else:
        #         raise ValueError("unexpected")
        # elif on_next_pos == '#':
        #     # TODO: Add better handling.
        #     return _handle_wall(fields, pos, dir)
        # elif on_next_pos == '.':
        #     pos = _next_point(pos, dir)
        #     return pos, dir

        # raise ValueError(f"unexpected")

    def debug_print(pos: Point, dir: Direction):
        for row_idx in range(min_row, max_row + 1):
            for col_idx in range(min_col, max_col + 1):
                point = Point(row_idx, col_idx)
                if point == pos:
                    val = dir
                else:
                    val = fields.get(point, ' ')
                print(val, end='')
            print()


    def _move(fields: Fields, steps: int, init_pos: Point, init_dir: Direction) -> tuple[Point, Direction]:
        dir = init_dir
        pos = init_pos
        for _ in range(steps):
            next_pos = _next_point(pos, dir)
            on_next_pos = fields.get(next_pos)
            if on_next_pos is None:
                # breakpoint()
                pos, dir = _handle_wrap(fields, pos, dir)
            elif on_next_pos == '#':
                continue
                # pos, dir = _handle_wall(fields, pos, dir)
            elif on_next_pos == '.':
                pos = _next_point(pos, dir)
            else:
                raise ValueError("unexpected")

        return (pos, dir)

    def _rotate(into: Literal['L', 'R'], dir: Direction) -> Direction:
        return _next_direction(into, dir)

    direction = '>'
    position = start

    for cmd in path:
        if isinstance(cmd, int):
            steps = cmd
            position, direction = _move(fields, steps, position, direction)
        elif isinstance(cmd, str):
            into = cmd
            assert into == 'L' or into == 'R'
            direction = _rotate(into, direction)
        else:
            raise ValueError(f"unexpected cmd {cmd=}")


    dir_pt = {
        '>': 0,
        'v': 1,
        '<': 2,
        '^': 3,
    }
    row_idx, col_idx = position
    print((row_idx + 1) * 1000 + 4 * (col_idx + 1) + dir_pt[direction])
    # breakpoint()
    # breakpoint()


if __name__ == "__main__":
    main()
