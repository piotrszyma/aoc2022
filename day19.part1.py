# Day 19
from dataclasses import dataclass
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
    ore: Cost
    clay: Cost
    obsidian: Cost
    geode: Cost


def grouped(items: list[str], size=1) -> Iterable[list[str]]:
    idx = 0
    while idx + size < len(items) + 1:
        yield items[idx : idx + size]
        idx += size

    yield [*items[idx : idx + size], None][:size]  # pad to `size` with None-s


RE_NUMBER = re.compile("\d+")


def read_blueprints(f: TextIOWrapper) -> Iterable[Blueprint]:
    items = [l.strip() for l in f]
    for blueprint in grouped(items, 6):
        raw_idx, raw_ore, raw_clay, raw_obsidian, raw_geode, _ = blueprint

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
            ore=Cost(ore=ore_cost),
            clay=Cost(ore=clay_ore),
            obsidian=Cost(ore=obs_ore, clay=obs_clay),
            geode=Cost(ore=geo_ore, obsidian=geo_obs),
        )


def main():
    with open("day19.input.test.txt", "r") as f:
        blueprints = list(read_blueprints(f))

    print(blueprints)


if __name__ == "__main__":
    main()
