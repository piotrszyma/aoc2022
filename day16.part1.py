# Day 16
import re
from dataclasses import dataclass
from typing import TypeAlias


RE_LINE = re.compile(
    r"Valve (?P<name>[A-Z]{2}).+=(?P<rate>\d+)\;.+valves?\ (?P<leads_to>.+)\n"
)


@dataclass
class Valve:
    name: str
    flow_rate: int

    neighbours: list["Valve"]
    openable_neighbours_costs: dict[str, int]

    all_neighbour_names: list[str]


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
                all_neighbour_names=leads_to,
            )

            if rate > 0:
                openable_valves_count += 1
    return valves


def simplify_graph(valves: dict[str, Valve]) -> dict[str, Valve]:
    for name, valve in valves.items():
        valve.neighbours = [valves[name] for name in valve.all_neighbour_names]

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
        valve.all_neighbour_names = list(x for x in neighbours.keys())

        new_valves[valve_name] = valve

    return new_valves


ValveName: TypeAlias = str
Cost: TypeAlias = int


def get_costs_to_get(
    valves: dict[str, Valve],
    current_name: str,
):
    to_visit = [valves[current_name]]
    visited: set[ValveName] = set()
    valve_name_to_cost: dict[ValveName, Cost] = {}

    while to_visit:
        # print(f"{[x.name for x in to_visit]=}")
        # print(f"{list(visited)=}")
        curr = to_visit.pop(0)
        if curr.name in visited:
            continue
        assert curr.name not in visited
        # print(f"{curr.name=}")
        visited.add(curr.name)

        for neighbour in curr.neighbours:
            if neighbour.name in visited:
                continue

            visited.add(curr.name)
            to_visit.append(neighbour)

            if neighbour.name in valve_name_to_cost:
                continue
                # breakpoint()
                # breakpoint()

            valve_name_to_cost[neighbour.name] = curr.openable_neighbours_costs[
                neighbour.name
            ] + valve_name_to_cost.get(curr.name, 0)

    return valve_name_to_cost


def main():
    valves: dict[str, Valve] = read_valves()
    MINUTES_TOTAL = 30

    valves = simplify_graph(valves)

    visited: set[str] = set()
    for valve in valves.values():
        for n in valve.all_neighbour_names:
            idx = ",".join(tuple(sorted([valve.name, n])))
            if idx in visited:
                continue
            visited.add(idx)
            other = valves[n]
            other_cost = valve.openable_neighbours_costs[other.name]
            print(
                f'{valve.name}_{valve.flow_rate} -- {other.name}_{other.flow_rate} [label="{other_cost}"];'
            )

    minutes_left = 30
    current_name = "AA"
    opened = set(["AA"])
    path = []
    total_disposed = 0
    while minutes_left > 0:
        costs_to_get = get_costs_to_get(valves, current_name)
        costs_to_get_valves = (
            (valves[name], cost_to_get)
            for (name, cost_to_get) in costs_to_get.items()
            if name not in opened
        )
        effect_per_valves = tuple(
            (v.name, ((minutes_left - cost - 1) * v.flow_rate))
            for v, cost in costs_to_get_valves
        )

        if len(effect_per_valves) == 0:
            break

        name, max_effect = max(effect_per_valves, key=lambda e: e[1])

        if costs_to_get[name] + 1 > minutes_left:
            break

        total_disposed += max_effect
        opened.add(name)
        minutes_left -= costs_to_get[name] + 1
        path.append(name)
        current_name = name

    print(f"{total_disposed=} {path=}")
    return


if __name__ == "__main__":
    main()
