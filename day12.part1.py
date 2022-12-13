# Day 12
from typing import Iterable

Coord = tuple[int, int]

SYMBOL_START = "S"
SYMBOL_END = "E"
DEBUG = False


def debug_print(rows: list[list[str]], visited: set[Coord]):
    if not DEBUG:
        return

    data = []
    for row_idx, row in enumerate(rows):
        for col_idx, cell in enumerate(row):
            c = cell if (row_idx, col_idx) in visited else "."
            data.append(c)
        data.append("\n")

    print("".join(data), end="")


def can_move_up(rows: list[list[str]], from_: Coord, into: Coord) -> bool:
    frx, fry = from_
    inx, iny = into
    from_symb = rows[frx][fry]
    into_symb = rows[inx][iny]

    assert ord("a") <= ord(from_symb) <= ord("z"), from_symb
    assert ord("a") <= ord(into_symb) <= ord("z"), into_symb

    if ord(from_symb) >= ord(into_symb):
        return True

    return ord(into_symb) - ord(from_symb) == 1


def _is_valid_coord(coord: Coord, rows: list[list[str]]) -> bool:
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


def visitable_around(rows: list[list[str]], curr: Coord) -> Iterable[Coord]:
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


def main():
    with open("day12.input.txt", "r") as f:
        rows: list[list[str]] = []

        start: Coord = (0, 0)
        end: Coord = (0, 0)

        for row_idx, raw_row in enumerate(f):
            row = [e for e in raw_row.strip()]
            for col_idx, cell in enumerate(row):
                if cell == SYMBOL_START:
                    row[col_idx] = "a"
                    start = (row_idx, col_idx)
                elif cell == SYMBOL_END:
                    row[col_idx] = "z"
                    end = (row_idx, col_idx)

            rows.append(row)

    to_visit: set[Coord] = {start}
    visited: set[Coord] = set()
    parents: dict[Coord, Coord] = {}

    while True:
        current = to_visit.pop()

        if current == end:
            break

        for el in visitable_around(rows, current):
            if el in visited:
                continue

            visited.add(el)
            to_visit.add(el)
            parents[el] = current

    path = [current]
    curr = current
    while True:
        path.append(parents[curr])
        curr = parents[curr]
        if curr == start:
            break

    path = list(reversed(path))

    debug_print(rows, {*path})

    print(len(path) - 1)


if __name__ == "__main__":
    main()
