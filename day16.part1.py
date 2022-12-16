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

    openable_neighbours: list["Valve"]
    openable_neighbours_costs: dict[str, int]

    leads_to: list[str]
    leads_to_costs: dict[str, int]


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
    valves: dict[str, Valve], valve: Valve, visited_names=set()
) -> list[tuple[Valve, int]]:

    openable_neighbours = []

    for other_valve in valve.openable_neighbours:
        if other_valve.name in visited_names:
            continue

        if other_valve.flow_rate > 0:
            openable_neighbours.append((other_valve, 1))
            continue

        # other_valve.flow_rate == 0

        other_neighbours = get_openable_neighbours(
            valves, other_valve, visited_names={*visited_names, valve.name}
        )

        for n_valve, cost in other_neighbours:
            openable_neighbours.append((n_valve, cost + 1))

    return openable_neighbours


def main():
    valves: dict[str, Valve] = {}
    openable_valves_count = 0
    MINUTES_TOTAL = 30

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
                openable_neighbours=[],
                openable_neighbours_costs={},
                leads_to=leads_to,
                leads_to_costs={},
            )

            if rate > 0:
                openable_valves_count += 1

    # for name, valve in valves.items():
    #     valve.openable_neighbours = [valves[name] for name in valve.leads_to]

    # for name, valve in valves.items():
    #     openable_neighbours = get_openable_neighbours(valves, valve)
    #     valve.openable_neighbours = [n for n, _ in openable_neighbours]
    #     valve.openable_neighbours_costs = {
    #         n.name: cost for (n, cost) in openable_neighbours
    #     }

    # valves = {
    #     name: v for name, v in valves.items() if v.flow_rate > 0 or v.name == "AA"
    # }

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

    while states:
        state = states.pop()

        if state.minutes_left == 0:
            final_states.append(state)
            continue

        if len(state.opened_names) == openable_valves_count:
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

            new_states.append(
                State(
                    current_name=next_valve_name,
                    opened_names=state.opened_names,
                    minutes_left=state.minutes_left - 1,
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
