# Day 4
# Day 4
import dataclasses


@dataclasses.dataclass
class Range:
    section_ids: set[int]

    def __contains__(self, other: "Range") -> bool:
        return self.section_ids | other.section_ids == self.section_ids

    def overlap(self, other: "Range") -> bool:
        return len(self.section_ids & other.section_ids) > 0


def parse_range(raw: str) -> Range:
    start, end = (int(idx) for idx in raw.split("-"))
    return Range(section_ids=set(idx for idx in range(start, end + 1)))


def parse_ranges(line: str) -> tuple[Range, Range]:
    line = line.strip()
    first, second = line.split(",")
    return parse_range(first), parse_range(second)


def main():
    with open("day4.input.txt", "r") as f:
        overlapped = 0
        for line in f:
            range1, range2 = parse_ranges(line)
            if range1.overlap(range2):
                overlapped += 1

        print(overlapped)


if __name__ == "__main__":
    main()
