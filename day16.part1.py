# Day 16
from typing import NamedTuple
import re


class Valve(NamedTuple):
    name: str
    flow_rate: int
    leads_to: list[str]


RE_LINE = re.compile(
    r"Valve (?P<name>[A-Z]{2}).+=(?P<rate>\d+)\;.+valves\ (?P<leads_to>.+)\n"
)


def main():
    valves: list[Valve] = []
    with open("day16.input.test.txt", "r") as f:
        for line in f:
            match = RE_LINE.search(line)
            assert match

            raw_name = match["name"]
            raw_rate = match["rate"]
            raw_leads_to = match["leads_to"]

            name = raw_name
            rate = int(raw_rate)
            leads_to = raw_leads_to.split(", ")

            valves.append(Valve(name, rate, leads_to))


if __name__ == "__main__":
    main()
