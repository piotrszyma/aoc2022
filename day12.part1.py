# Day 12
import sys
from typing import Iterable

Coord = tuple[int, int]

SYMBOL_START = "S"
SYMBOL_END = "E"
DEBUG = True


def debug_print(rows: list[list[str]], visited: set[Coord]):
    if not DEBUG:
        return

    data = []
    for row_idx, row in enumerate(rows):
        for col_idx, cell in enumerate(row):
            c = cell if (row_idx, col_idx) in visited else "."
            # print(c, end="")
            data.append(c)
        data.append("\n")

    print("".join(data), end="")
    # input()


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


def can_move_down(rows: list[list[str]], from_: Coord, into: Coord) -> bool:
    return can_move_up(rows, into, from_)
    frx, fry = from_
    inx, iny = into
    from_symb = rows[frx][fry]
    into_symb = rows[inx][iny]

    assert ord("a") <= ord(from_symb) <= ord("z"), from_symb
    assert ord("a") <= ord(into_symb) <= ord("z"), into_symb

    # if from_symb == "x" and into_symb == "t":
    #     breakpoint()

    if ord(from_symb) - ord(into_symb) == 0:
        return True

    if ord(from_symb) - ord(into_symb) == 1:
        return True

    return False


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


def visitable_around_end(rows: list[list[str]], curr: Coord) -> Iterable[Coord]:
    row_id_s, col_id_s = curr

    # Up
    coord = (row_id_s - 1, col_id_s)
    if _is_valid_coord(coord, rows) and can_move_down(rows, curr, coord):
        yield coord

    # Right
    coord = (row_id_s, col_id_s + 1)
    if _is_valid_coord(coord, rows) and can_move_down(rows, curr, coord):
        yield coord

    # Down
    coord = (row_id_s + 1, col_id_s)
    if _is_valid_coord(coord, rows) and can_move_down(rows, curr, coord):
        yield coord

    # Left
    coord = (row_id_s, col_id_s - 1)
    if _is_valid_coord(coord, rows) and can_move_down(rows, curr, coord):
        yield coord


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
    to_visit_end: set[Coord] = {end}
    visited: set[Coord] = set()
    visited_end: set[Coord] = set()
    parents: dict[Coord, Coord] = {}
    parents_end: dict[Coord, Coord] = {}

    current = list(to_visit)[0]
    current_end = list(to_visit_end)[0]

    while True:
        current = to_visit.pop()
        visited.add(current)

        # current_end = to_visit_end.pop()
        # visited_end.add(current_end)

        # if current in visited_end or current_end in visited:
        #     break

        if current == end:
            break

        for el in visitable_around(rows, current):
            if el not in visited:
                to_visit.add(el)
                parents[el] = current

        # for el in visitable_around_end(rows, current_end):
        #     if el not in visited_end:
        #         to_visit_end.add(el)
        #         parents_end[el] = current_end

    # debug_print(rows, {*visited, *visited_end})
    # return

    # path_end = [current_end]
    # curr = current_end
    # while parents_end[curr] != end:
    #     path_end.append(parents_end[curr])
    #     curr = parents_end[curr]
    #     assert curr in parents_end

    path = [current]
    curr = current
    while parents[curr] != start:
        path.append(parents[curr])
        curr = parents[curr]
        assert curr in parents

    # debug_print(rows, {*path, *path_end})
    debug_print(rows, set(path))
    print(len(path))
    # breakpoint()

    # path = list(reversed(path))

    # for idx, el in path:
    #     if el in path_end:
    #         breakpoint()

    # debug_print(rows, set(path))

    # debug_print(rows, set(path_end))

    # print(len(path))
    # 399 is too high :(
    # 398 is too high :(


if __name__ == "__main__":
    main()
