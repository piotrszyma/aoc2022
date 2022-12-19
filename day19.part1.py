# Day 19
from dataclasses import dataclass, field
from io import TextIOWrapper
import re
from typing import Iterable


@dataclass
class Cost:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0


@dataclass
class Blueprint:
    idx: int
    ore_robot: Cost
    clay_robot: Cost
    obsidian_robot: Cost
    geode_robot: Cost


def grouped(items: list[str], size=1) -> Iterable[list[str]]:
    idx = 0
    while idx + size < len(items) + 1:
        yield items[idx : idx + size]
        idx += size


RE_NUMBER = re.compile("\d+")


def read_blueprints(f: TextIOWrapper) -> Iterable[Blueprint]:
    items = []
    for l in f:
        for chunk in l.strip().split("Each"):
            items.append(chunk)

    for blueprint in grouped(items, 5):
        try:
            raw_idx, raw_ore, raw_clay, raw_obsidian, raw_geode = blueprint
        except:
            breakpoint()
            raise

        result = RE_NUMBER.findall(raw_idx)
        idx = int(result[0])

        [ore_cost] = RE_NUMBER.findall(raw_ore)
        ore_cost = int(ore_cost)

        [clay_ore] = RE_NUMBER.findall(raw_clay)
        clay_ore = int(clay_ore)

        [obs_ore, obs_clay] = [int(x) for x in RE_NUMBER.findall(raw_obsidian)]

        [geo_ore, geo_obs] = [int(x) for x in RE_NUMBER.findall(raw_geode)]

        yield Blueprint(
            idx=idx,
            ore_robot=Cost(ore=ore_cost),
            clay_robot=Cost(ore=clay_ore),
            obsidian_robot=Cost(ore=obs_ore, clay=obs_clay),
            geode_robot=Cost(ore=geo_ore, obsidian=geo_obs),
        )


@dataclass
class State:
    ore: int
    ore_robot: int

    clay: int
    clay_robot: int

    obsidian: int
    obsidian_robot: int

    geode: int
    geode_robot: int

    minute_left: int

    history: tuple[tuple["State", str], ...] = field(default=tuple(), repr=False)


def maximize_goedes(
    blueprint: Blueprint,
    minutes_left: int,
    state: State,
) -> State:
    states: list[tuple[Blueprint, int, State]] = [(blueprint, minutes_left, state)]

    final_states: list[State] = []

    while states:
        blueprint, minutes_left, state = states.pop()

        if minutes_left == 0:
            final_states.append(state)
            continue

        # print((state.ore, state.clay, state.geode, state.obsidian, minutes_left))

        obsidian_full = state.obsidian > blueprint.geode_robot.obsidian
        clay_full = state.clay > blueprint.obsidian_robot.clay
        ore_full = state.ore > max(
            blueprint.ore_robot.ore,
            blueprint.clay_robot.ore,
            blueprint.obsidian_robot.ore,
            blueprint.geode_robot.ore,
        )

        if ore_full:
            continue

        if obsidian_full and clay_full and ore_full:
            continue

        # Decide which robot to build in this minute and add it to state (if can).

        built = 0

        if (
            state.ore >= blueprint.geode_robot.ore
            and state.obsidian >= blueprint.geode_robot.obsidian
        ):
            # Case when building geode robot
            new_state = State(
                ore=state.ore
                + state.ore_robot
                - blueprint.geode_robot.ore,  # Geode - remove ore.
                clay=state.clay + state.clay_robot,
                obsidian=state.obsidian
                + state.obsidian_robot
                - blueprint.geode_robot.obsidian,  # Geode - remove obsidian.
                geode=state.geode + state.geode_robot,
                ore_robot=state.ore_robot,
                clay_robot=state.clay_robot,
                obsidian_robot=state.obsidian_robot,
                geode_robot=state.geode_robot + 1,  # Add one geode robot.
                minute_left=minutes_left,
            )
            new_state.history = (*state.history, (state, "build geode"))
            states.append((blueprint, minutes_left - 1, new_state))
            built += 1

        if (
            state.ore >= blueprint.obsidian_robot.ore
            and state.clay >= blueprint.obsidian_robot.clay
        ):
            # Case when building obsidian robot
            new_state = State(
                ore=state.ore
                + state.ore_robot
                - blueprint.obsidian_robot.ore,  # Obsidian - remove ore.
                clay=state.clay
                + state.clay_robot
                - blueprint.obsidian_robot.clay,  # Obsidian - remove clay.
                obsidian=state.obsidian + state.obsidian_robot,
                geode=state.geode + state.geode_robot,
                ore_robot=state.ore_robot,
                clay_robot=state.clay_robot,
                obsidian_robot=state.obsidian_robot + 1,  # Add one obsidian robot.
                geode_robot=state.geode_robot,
                minute_left=minutes_left,
            )
            new_state.history = (*state.history, (new_state, "build obsidian"))
            states.append((blueprint, minutes_left - 1, new_state))
            built += 1

        if state.ore >= blueprint.clay_robot.ore:
            # Case when building clay robot
            new_state = State(
                ore=state.ore
                + state.ore_robot
                - blueprint.clay_robot.ore,  # Clay robot - remove ore.
                clay=state.clay + state.clay_robot,
                obsidian=state.obsidian + state.obsidian_robot,
                geode=state.geode + state.geode_robot,
                ore_robot=state.ore_robot,
                clay_robot=state.clay_robot + 1,  # Add one clay robot.
                obsidian_robot=state.obsidian_robot,
                geode_robot=state.geode_robot,
                minute_left=minutes_left,
            )
            new_state.history = (*state.history, (new_state, "build clay"))
            states.append((blueprint, minutes_left - 1, new_state))
            built += 1

        if state.ore >= blueprint.ore_robot.ore:
            # Case when building ore robot.
            new_state = State(
                ore=state.ore
                + state.ore_robot
                - blueprint.ore_robot.ore,  # Ore robot - remove ore.
                clay=state.clay + state.clay_robot,
                obsidian=state.obsidian + state.obsidian_robot,
                geode=state.geode + state.geode_robot,
                ore_robot=state.ore_robot + 1,
                clay_robot=state.clay_robot,
                obsidian_robot=state.obsidian_robot,
                geode_robot=state.geode_robot,
                minute_left=minutes_left,
            )
            new_state.history = (*state.history, (new_state, "build ore"))
            states.append((blueprint, minutes_left - 1, new_state))
            built += 1

        all_built = built == 4
        if all_built:
            continue

        # Case when nothing was built in this round - collect resources.
        # Each robot gives +1 resource.
        new_state = State(
            ore=state.ore + state.ore_robot,
            clay=state.clay + state.clay_robot,
            obsidian=state.obsidian + state.obsidian_robot,
            geode=state.geode + state.geode_robot,
            ore_robot=state.ore_robot,
            clay_robot=state.clay_robot,
            obsidian_robot=state.obsidian_robot,
            geode_robot=state.geode_robot,
            minute_left=minutes_left,
        )
        new_state.history = (*state.history, (new_state, "build nothing"))

        # if new_state.ore > max(
        #     blueprint.ore_robot.ore,
        #     blueprint.clay_robot.ore,
        #     blueprint.obsidian_robot.ore,
        #     blueprint.geode_robot.ore,
        # ):
        #     continue

        # if new_state.clay > blueprint.obsidian_robot.clay:
        #     continue

        # if new_state.obsidian > blueprint.geode_robot.obsidian:
        #     continue

        states.append((blueprint, minutes_left - 1, new_state))

    return max(final_states, key=lambda s: s.geode)


def main():
    with open("day19.input.txt", "r") as f:
        blueprints = list(read_blueprints(f))

    minutes_left = 24
    quality_levels = 0

    for blueprint in blueprints:
        max_state = maximize_goedes(
            blueprint,
            minutes_left=minutes_left,
            state=State(
                ore=0,
                ore_robot=1,
                clay=0,
                clay_robot=0,
                obsidian=0,
                obsidian_robot=0,
                geode=0,
                geode_robot=0,
                minute_left=minutes_left,
            ),
        )
        quality_levels += blueprint.idx * max_state.geode
        print(f"{blueprint.idx=} {max_state.geode=}")

        # print("\n".join(h[1] + " " + str(h[0]) for h in max_goedes.history))

    # 943 too small
    print(f"{quality_levels=}")


if __name__ == "__main__":
    main()
