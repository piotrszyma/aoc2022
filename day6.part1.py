# Day 6


def start_of_marker(line: str) -> int:
    idx = 0
    shift = 14
    while True:
        chars = line[idx : idx + shift]
        if len(set(chars)) == shift:
            return idx + shift
        idx += 1


def main():
    with open("day6.input.txt", "r") as f:
        for line in f:
            print(start_of_marker(line))
            return


if __name__ == "__main__":
    main()
