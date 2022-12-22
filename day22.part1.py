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
            path.append(int(group))
        else:
            path.append(group)

    return path

def _invert(dir: Direction) -> Direction:
    if dir == '>':
        return '<'
    if dir == '<':
        return '>'
    if dir == '^':
        return 'v'
    if dir == 'v':
        return '^'

    raise ValueError(f'unexpected dir {dir=}')

def main():
    fields: dict[Point, str] = {}
    path: Path | None = None
    start: Point | None = None

    points_in_row: DefaultDict[int, list[Point]] = defaultdict(list)
    points_in_col: DefaultDict[int, list[Point]] = defaultdict(list)

    with open("day22.input.test.txt", "r") as f:
        for row_idx, raw_line in enumerate(f):
            line = raw_line.strip()

            if line == "":
                continue

            if line[0].isdigit():
                path = _parse_path(line)
                continue

            for col_idx, cell in enumerate(line):
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

    direction = '>'
    position = start

    def _move(fields: Fields, steps: int, pos: Point, dir: Direction) -> tuple[Point, Direction]:
        for _ in range(steps):
            next_pos = _next_point(pos, dir)
            on_next_pos = fields.get(next_pos)
            if on_next_pos is None:
                # TODO: Move to other side of pane.
                ...
            elif on_next_pos == '#':
                dir = _invert(dir) # Invert.

                next_pos = _next_point(pos, dir)
                on_next_pos = fields.get(next_pos)

                if on_next_pos is None:
                    # TODO: Move to other side of pane.
                    ...
                elif on_next_pos == '#':
                    continue # Ignore this `steps`.
                elif on_next_pos == '.':
                    pos = _next_point(pos, dir)
                else:
                    raise ValueError("unexpected")
            elif on_next_pos == '.':
                pos = _next_point(pos, dir)
            else:
                raise ValueError("unexpected")

        return (pos, dir)

    def _rotate(into: Literal['L', 'R'], dir: Direction) -> Direction:
        return _next_direction(into, dir)

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


    breakpoint()
    breakpoint()


if __name__ == "__main__":
    main()
