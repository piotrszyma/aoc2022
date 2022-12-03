def get_priority(symbol: str) -> int:
    if symbol.lower() == symbol:  # is lowercase
        # ord(a - z) is from 97 to 122
        return ord(symbol) - 96
    else:  # uppercase
        # ord(A - Z) is from 65 to 90
        return ord(symbol) - 38


def main():
    with open("day3.input.txt", "r") as f:
        priority_total = 0

        for line in f:
            mid_idx = len(line) // 2
            left_box, right_box = line[:mid_idx], line[mid_idx:]

            left_uniq = set(left_box)
            right_uniq = set(right_box)

            [repeated_item] = left_uniq & right_uniq
            priority = get_priority(repeated_item)

            priority_total += priority

        print(priority_total)


if __name__ == "__main__":
    main()
