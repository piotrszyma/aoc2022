# Day 23

from dataclasses import dataclass

Pos = tuple[int, int]
Step = int
ElfPos = dict[Pos, Step]


def _get_next_pos(pos: Pos, next_dir: str) -> Pos:
    row, col = pos
    match next_dir:
        case 'N':
            return row - 1, col
        case 'S':
            return row + 1, col
        case 'W':
            return row, col - 1
        case 'E':
            return row, col + 1

    raise ValueError("unexpected")


@dataclass
class Elf:
    pos: Pos
    dirs: list[str]
    next_dir: str

    def next_pos(self):
        if self.next_dir == '':
            return self.pos
        return _get_next_pos(self.pos, self.next_dir)


def debug_print(elfs: list[Elf]):
    pos = {elf.pos for elf in elfs}
    size = 10
    min_row, max_row = -size, size
    min_col, max_col= -size, size

    print("x\t" + "".join((str(r) if 0<=r<=9 else'-')  for r in range(min_row, max_row + 1)))
    for row in range(min_row, max_row + 1):
        print(str(row) + '\t', end='')
        for col in range(min_col, max_col + 1):
            if (row, col) in pos:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print("x\t" + "".join((str(r) if 0<=r<=9 else'-')  for r in range(min_row, max_row + 1)))

def _is_any_adjacent(all_pos: set[Pos], elf: Elf) -> bool:
    xp, yp = elf.pos
    for x in range(xp - 1, xp + 2):
        for y in range(yp - 1, yp + 2):
            if (x, y) == (xp, yp):
                continue

            if (x, y) in all_pos:
                return True

    return False

def _get_next_direction(all_pos: set[Pos], elf: Elf) -> str | None:
    row, col = elf.pos
    for direct in elf.dirs:
        if direct == 'N':
            if not any(p in all_pos for p in [(row-1,col-1),(row-1, col), (row-1, col+1)]):
                return direct
        elif direct == 'S':
            if not any(p in all_pos for p in [(row+1,col-1),(row+1, col), (row+1, col+1)]):
                return direct
        elif direct == 'W':
            if not any(p in all_pos for p in [(row-1,col-1),(row, col-1), (row+1, col-1)]):
                return direct
        elif direct == 'E':
            if not any(p in all_pos for p in [(row-1,col+1),(row, col+1), (row+1, col+1)]):
                return direct
    return None





def main():
    # Maps elf pos (row, col) to idx of next step
    # 0 -> N
    # 1 -> S
    # 2 -> W
    # 3 -> E
    elfs: list[Elf] = []

    with open("day23.input.txt", "r") as f:
        for row_idx, line in enumerate(f):
            for col_idx, cell in enumerate(line):
                if cell == "#":
                    elfs.append(Elf(pos=(row_idx, col_idx), dirs=['N', 'S', 'W', 'E'], next_dir=""))

    rnd = 1

    while True:
        all_pos = {elf.pos for elf in elfs}
        for elf in elfs:
            elf.next_dir = ""
        # debug_print(elfs)
        # input()

        pos_to_make: set[Pos] = set()
        pos_to_skip: set[Pos] = set()

        for elf in elfs:
            if not _is_any_adjacent(all_pos, elf): # Nothing adjacent, keep elf here.
                elf.next_dir = ''
                pos_to_skip.add(elf.pos)
                continue

            next_dir = _get_next_direction(all_pos, elf)
            if next_dir is None: # No way to move, keep elf here.
                elf.next_dir = ''
                pos_to_skip.add(elf.pos)
                continue

            elf.next_dir = next_dir
            next_pos = elf.next_pos()

            if next_pos in pos_to_skip:
                elf.next_dir = ''
                continue

            if next_pos in pos_to_make:
                elf.next_dir = ''
                pos_to_make.remove(next_pos)
                pos_to_skip.add(next_pos)
                continue

            pos_to_make.add(next_pos)

        if len(pos_to_make) == 0:
            break

        for elf in elfs:
            next_pos = elf.next_pos()
            if next_pos in pos_to_make:
                assert next_pos not in pos_to_skip
                elf.pos = next_pos
                elf.dirs = elf.dirs[1:] + [elf.dirs[0]]
                assert len(set(elf.dirs)) == 4
            else:
                elf.dirs = elf.dirs[1:] + [elf.dirs[0]]
                assert len(set(elf.dirs)) == 4
        rnd += 1

    print(rnd)


if __name__ == "__main__":
    main()
