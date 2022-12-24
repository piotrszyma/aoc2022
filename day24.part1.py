import collections
from dataclasses import dataclass
# Day 24
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

@dataclass
class Wind:
    dir: str
    pos: tuple[int, int]

    def __hash__(self):
        return hash((self.pos, self.dir))

WindPos = set[tuple[int, int]]

@dataclass
class PlayerState:
    pos: tuple[int, int]
    winds: frozenset[Wind]
    time: int

    def __hash__(self):
        return hash((self.pos, self.winds))

def _move_winds(winds: frozenset[Wind], size_x: int, size_y: int) -> tuple[frozenset[Wind], WindPos]:
    new_winds: set[Wind] = set()
    new_wind_pos: WindPos = set()
    for wind in winds:
        xw, yw = wind.pos
        direct = wind.dir
        if direct == '>':
            new_pos = (xw, (yw+1 - 1) % (size_y - 2) + 1)
        elif direct == '<':
            new_pos = (xw, (yw-1 - 1) % (size_y - 2) + 1)
        elif direct == '^':
            new_pos = ((xw - 1 - 1) % (size_x - 2) + 1, yw)
        elif direct == 'v':
            new_pos = ((xw + 1 - 1) % (size_x - 2) + 1, yw)
        else:
            raise ValueError('unexpected')
        xnw, ynw = new_pos
        if direct in '^v':
            if not (abs(xw - xnw) == 1 or xnw == 1 or xnw == size_x - 2):
                breakpoint()

        if direct in '<>':
            if not (abs(yw - ynw) == 1 or ynw == 1 or ynw == size_y - 2):
                breakpoint()
        new_winds.add(Wind(dir=wind.dir, pos=new_pos))
        new_wind_pos.add(new_pos)

    return frozenset(new_winds), new_wind_pos

def print_debug(walls: set[tuple[int, int]], winds: set[Wind], player_pos: tuple[int, int],size_x: int, size_y: int):
    winds_pos = {w.pos for w in winds}
    all_pos = collections.defaultdict(int)

    for wind in winds:
        all_pos[wind.pos] += 1

    for row_idx in range(size_x):
        for col_idx in range(size_y):
            pos = (row_idx, col_idx)
            if pos == player_pos:
                print(bcolors.OKBLUE + 'P' + bcolors.ENDC, end='')
            elif pos in walls:
                print('#', end='')
            elif pos in winds_pos:
                count = all_pos[pos]
                if count > 1:
                    print(count, end='')
                else:
                    wind = [w for w in winds if w.pos == pos][0]
                    print(wind.dir, end='')
            else:
                print('.', end='')
        print("")

def main():
    walls: set[tuple[int, int]] = set()
    winds: set[Wind] = set()

    start: tuple[int, int] = (0, 1)
    max_col_idx = 0
    max_row_idx = 0

    ct = 0
    with open("day24.input.txt", "r") as f:
        row_idx = -1
        col_idx = -1
        for row_idx, line in enumerate(f):
            max_row_idx = max(row_idx, max_row_idx)

            line = line.strip()

            for col_idx, c in enumerate(line):
                max_col_idx = max(col_idx, max_col_idx)

                if c == '#':
                    walls.add((row_idx, col_idx))
                elif c in '><^v':
                    dir = c
                    winds.add(Wind(dir=dir, pos=(row_idx, col_idx)))
    end = (row_idx, col_idx - 1)

    states = collections.deque([PlayerState(pos=start, winds=frozenset(winds), time=1)])

    visited_states = set()

    size_x, size_y = max_row_idx + 1, max_col_idx + 1
    state = None
    while states:
        state = states.popleft()
        # print_debug(walls, state.winds, state.pos, size_x, size_y)
        # input()

        if state in visited_states:
            continue

        visited_states.add(state)

        if state.pos == end:
            break

        next_winds, new_winds_pos = _move_winds(state.winds, size_x, size_y)
        time = state.time + 1

        x, y = state.pos
        # Stay
        states.append(PlayerState(state.pos, winds=next_winds, time=time))

        # Up
        new_pos = (x-1, y)
        if new_pos not in new_winds_pos and new_pos not in walls and new_pos != start and x - 1 > 0:
            states.append(PlayerState(new_pos, winds=next_winds, time=time))

        # Left
        new_pos = (x, y-1)
        if new_pos not in new_winds_pos and new_pos not in walls and new_pos != start:
            states.append(PlayerState(new_pos, winds=next_winds, time=time))

        # Right
        new_pos = (x, y+1)
        if new_pos not in new_winds_pos and new_pos not in walls and new_pos != start:
            states.append(PlayerState(new_pos, winds=next_winds, time=time))

        # Down
        new_pos = (x+1, y)
        if new_pos not in new_winds_pos and new_pos not in walls and new_pos != start:
            states.append(PlayerState(new_pos, winds=next_winds, time=time))

    assert state
    # 350 is too high
    print(state.time)

if __name__ == "__main__":
    ####
    #v #
    #  #
    ####
    # res = _move_winds({Wind(dir='v', pos=(1,1))}, size_x=4, size_y=4)
    # # assert res == {Wind(dir='v', pos=(2, 1))}
    # res = _move_winds(res, size_x=4, size_y=4)
    # breakpoint()
    main()
