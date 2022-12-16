# Day 16
import re
from dataclasses import dataclass


RE_LINE = re.compile(
    r"Valve (?P<name>[A-Z]{2}).+=(?P<rate>\d+)\;.+valves?\ (?P<leads_to>.+)\n"
)


@dataclass
class Valve:
    name: str
    flow_rate: int

    neighbours: list["Valve"]
    openable_neighbours_costs: dict[str, int]

    leads_to: list[str]


@dataclass
class State:
    current_name: str
    opened_names: set[str]
    minutes_left: int
    pressure_total: int
    just_visited: str
    previous_step: str
    # history: list[str]  # for debug
    visited_without_open: set[str]


def get_openable_neighbours(
    valve: Valve,
    is_root: bool,
    visited_names: set[str] = set(),
) -> dict[str, int]:

    if (valve.flow_rate > 0 or valve.name == "AA") and not is_root:
        return {}

    neighbours_to_cost: dict[str, int] = {}

    if valve.name in visited_names:
        return {}

    for other_valve in valve.neighbours:
        if other_valve.name in visited_names:
            continue

        if other_valve.flow_rate > 0 or other_valve.name == "AA":
            neighbours_to_cost[other_valve.name] = 1
            continue

        other_neighbours = get_openable_neighbours(
            other_valve, visited_names={*visited_names, valve.name}, is_root=False
        )

        for other_neighbour_name, cost in other_neighbours.items():
            neighbours_to_cost[other_neighbour_name] = cost + 1

    return neighbours_to_cost


def read_valves() -> dict[str, Valve]:
    valves: dict[str, Valve] = {}
    openable_valves_count = 0

    with open("day16.input.test.txt", "r") as f:
        for line in f:
            match = RE_LINE.search(line)
            assert match, line

            raw_name = match["name"]
            raw_rate = match["rate"]
            raw_leads_to = match["leads_to"]

            name = raw_name
            rate = int(raw_rate)
            leads_to = raw_leads_to.split(", ")

            valves[name] = Valve(
                name,
                flow_rate=rate,
                neighbours=[],
                openable_neighbours_costs={},
                leads_to=leads_to,
            )

            if rate > 0:
                openable_valves_count += 1
    return valves


def main():
    valves: dict[str, Valve] = read_valves()
    MINUTES_TOTAL = 30

    for name, valve in valves.items():
        valve.neighbours = [valves[name] for name in valve.leads_to]

    all_neighbours: dict[str, dict[str, int]] = {}
    for name, valve in valves.items():
        if valve.name == "AA" or valve.flow_rate > 0:
            openable_neighbours = get_openable_neighbours(valve, is_root=True)
            all_neighbours[name] = openable_neighbours

    new_valves: dict[str, Valve] = {}
    for valve_name, neighbours in all_neighbours.items():
        valve = valves[valve_name]
        valve.neighbours = list(valves[x] for x in neighbours.keys())
        valve.openable_neighbours_costs = neighbours
        valve.leads_to = list(x for x in neighbours.keys())

        new_valves[valve_name] = valve

    visited: set[str] = set()
    for valve in new_valves.values():
        for n in valve.leads_to:
            idx = ",".join(tuple(sorted([valve.name, n])))
            if idx in visited:
                continue
            visited.add(idx)
            other = valves[n]
            other_cost = valve.openable_neighbours_costs[other.name]
            print(
                f'{valve.name}_{valve.flow_rate} -> {other.name}_{other.flow_rate} [label="{other_cost}"];'
            )

    states = [
        State(
            current_name="AA",
            opened_names=set(),
            minutes_left=MINUTES_TOTAL,
            pressure_total=0,
            just_visited="",
            previous_step="",
            visited_without_open=set(),
        )
    ]

    final_states: list[State] = []
    openable_valves_count = len(new_valves) - 1

    while states:
        state = states.pop()

        if state.minutes_left == 0:
            final_states.append(state)
            continue

        if len(state.opened_names) == openable_valves_count:
            assert state.minutes_left >= 0
            final_states.append(state)
            continue

        new_states = []

        current_valve = valves[state.current_name]

        is_current_opened = state.current_name in state.opened_names

        if not is_current_opened and current_valve.flow_rate > 0:  # Case when opening.
            new_opened = {*state.opened_names, state.current_name}
            new_total = (
                state.pressure_total
                + (state.minutes_left - 1) * current_valve.flow_rate
            )

            assert state.minutes_left - 1 >= 0
            new_states.append(
                State(
                    current_name=state.current_name,
                    opened_names=new_opened,
                    minutes_left=state.minutes_left - 1,
                    pressure_total=new_total,
                    just_visited=state.just_visited,
                    previous_step="open",
                    visited_without_open=set(),
                )
            )

        for next_valve_name in current_valve.leads_to:
            if next_valve_name in state.visited_without_open:
                continue

            if state.just_visited == next_valve_name and state.previous_step == "move":
                continue

            move_cost = current_valve.openable_neighbours_costs[next_valve_name]

            if state.minutes_left - move_cost < 0:
                continue

            new_states.append(
                State(
                    current_name=next_valve_name,
                    opened_names=state.opened_names,
                    minutes_left=state.minutes_left - move_cost,
                    pressure_total=state.pressure_total,
                    just_visited=state.current_name,
                    previous_step="move",
                    visited_without_open={*state.visited_without_open, next_valve_name},
                )
            )

        states.extend(new_states)

    max_state = max(final_states, key=lambda s: s.pressure_total)

    # for minute, entry in enumerate(max_state.history):
    #     print(f"== Minute {minute} ==")
    #     print(entry)

    print("total", max_state.pressure_total)


if __name__ == "__main__":
    main()
