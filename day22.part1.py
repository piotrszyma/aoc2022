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

def _get_next_wrapped(
    points_in_row: dict[int, list[Point]],
    points_in_col: dict[int, list[Point]],
    curr_point: Point,
    dir: Direction,
) -> Point:
    curr_row_idx, curr_col_idx = curr_point

    if dir == '>':
        return points_in_row[curr_row_idx][0]
    elif dir == '<':
        return points_in_row[curr_row_idx][-1]
    elif dir == '^':
        return points_in_col[curr_col_idx][-1]
    elif dir == 'v':
        return points_in_col[curr_col_idx][0]
    else:
        raise ValueError("unexpected")

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
            return pos, dir
        elif on_next_pos == '.':
            return next_pos, dir
        else:
            raise ValueError("unexpected")

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
                pos, dir = _handle_wrap(fields, pos, dir)
            elif on_next_pos == '#':
                continue
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


if __name__ == "__main__":
    main()
