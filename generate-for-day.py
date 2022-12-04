import argparse
import pathlib


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("day", type=int)
    args = parser.parse_args()
    day: int = args.day

    template = f"""# Day {day}

def main():
    with open("day{day}.input.test.txt", "r") as f:
        ...

if __name__ == "__main__":
    main()
"""

    py_day1 = pathlib.Path(f"day{day}.part1.py")
    py_day1.write_text(template)

    py_day2 = pathlib.Path(f"day{day}.part2.py")
    py_day2.write_text(template)

    txt_input_test = pathlib.Path(f"day{day}.input.test.txt")
    txt_input_test.touch()

    txt_input = pathlib.Path(f"day{day}.input.txt")
    txt_input.touch()


if __name__ == "__main__":
    main()
