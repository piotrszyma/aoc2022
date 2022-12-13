# Day 12
from typing import Iterable

Rows = list[list[str]]
Coord = tuple[int, int]

SYMBOL_START = "S"
SYMBOL_END = "E"
DEBUG = False


def debug_print(rows: Rows, visited: set[Coord]):
    if not DEBUG:
        return

    data = []
    for row_idx, row in enumerate(rows):
        for col_idx, cell in enumerate(row):
            c = cell if (row_idx, col_idx) in visited else "."
            data.append(c)
        data.append("\n")

    print("".join(data), end="")


def can_move_up(rows: Rows, from_: Coord, into: Coord) -> bool:
    frx, fry = from_
    inx, iny = into
    from_symb = rows[frx][fry]
    into_symb = rows[inx][iny]

    assert ord("a") <= ord(from_symb) <= ord("z"), from_symb
    assert ord("a") <= ord(into_symb) <= ord("z"), into_symb

    if ord(from_symb) >= ord(into_symb):
        return True

    return ord(into_symb) - ord(from_symb) == 1


def _is_valid_coord(coord: Coord, rows: Rows) -> bool:
    x, y = coord
    if x < 0:
        return False
    if y < 0:
        return False
    try:
        rows[x][y]
    except IndexError:
        return False
    else:
        return True


def visitable_around(rows: Rows, curr: Coord) -> Iterable[Coord]:
    row_id_s, col_id_s = curr

    # Up
    coord = (row_id_s - 1, col_id_s)
    if _is_valid_coord(coord, rows) and can_move_up(rows, curr, coord):
        yield coord

    # Right
    coord = (row_id_s, col_id_s + 1)
    if _is_valid_coord(coord, rows) and can_move_up(rows, curr, coord):
        yield coord

    # Down
    coord = (row_id_s + 1, col_id_s)
    if _is_valid_coord(coord, rows) and can_move_up(rows, curr, coord):
        yield coord

    # Left
    coord = (row_id_s, col_id_s - 1)
    if _is_valid_coord(coord, rows) and can_move_up(rows, curr, coord):
        yield coord


def calc_shortest_path(rows: Rows, start: Coord, end: Coord) -> int | None:
    to_visit: set[Coord] = {start}
    visited: set[Coord] = set()
    parents: dict[Coord, Coord] = {}

    current = None
    found = False

    while to_visit:
        current = to_visit.pop()

        if current == end:
            found = True
            break

        for el in visitable_around(rows, current):
            if el in visited:
                continue

            visited.add(el)
            to_visit.add(el)
            parents[el] = current

    if not found:
        return None

    assert current is not None

    curr = current
    steps_count = 0

    while True:
        curr = parents[curr]
        steps_count += 1
        if curr == start:
            break

    return steps_count


def main():
    with open("day12.input.txt", "r") as f:
        rows: Rows = []

        end: Coord = (0, 0)
        starts: list[Coord] = []

        for row_idx, raw_row in enumerate(f):
            row = [e for e in raw_row.strip()]
            for col_idx, cell in enumerate(row):
                if cell == SYMBOL_START:
                    row[col_idx] = "a"
                    # start = (row_idx, col_idx)
                elif cell == SYMBOL_END:
                    row[col_idx] = "z"
                    end = (row_idx, col_idx)

                if cell == "a" or cell == SYMBOL_START:
                    coord = (row_idx, col_idx)
                    starts.append(coord)

            rows.append(row)

    min_steps_count = 2**32
    for start in starts:
        steps_count = calc_shortest_path(rows, start, end)
        if steps_count is None:
            continue

        min_steps_count = min(steps_count, min_steps_count)

    print(min_steps_count)


if __name__ == "__main__":
    main()
