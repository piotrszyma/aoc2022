# Day 8


def print_visibility(v):
    for row in v:
        print(row)


def main():
    with open("day8.input.txt", "r") as f:
        matrix: list[list[int]] = []
        visibility: list[list[bool]] = []

        line = []

        for line in f:
            line = line.strip()
            row = [int(cell) for cell in line]
            row_visiblity = [False for _ in line]
            # First and last item in row always visible.
            row_visiblity[0] = True
            row_visiblity[-1] = True
            visibility.append(row_visiblity)
            matrix.append(row)

        assert line

        # First row visible.
        visibility[0] = [True for _ in line]

        # Last row visible.
        visibility[-1] = [True for _ in line]

        row_len = len(matrix)
        col_len = len(matrix[0])

        row_start_end = tuple(range(1, row_len - 1))
        row_end_start = tuple(reversed(row_start_end))

        col_start_end = tuple(range(1, col_len - 1))
        col_end_start = tuple(reversed(col_start_end))

        # from top to bottom
        for col_idx in col_start_end:
            max_before = matrix[0][col_idx]
            for row_idx in row_start_end:
                current = matrix[row_idx][col_idx]
                if current > max_before:
                    visibility[row_idx][col_idx] = True
                    max_before = current

        for col_idx in col_start_end:
            max_before = matrix[-1][col_idx]
            for row_idx in row_end_start:
                current = matrix[row_idx][col_idx]
                if current > max_before:
                    visibility[row_idx][col_idx] = True
                    max_before = current

        # from left to right
        for row_idx in row_start_end:
            max_before = matrix[row_idx][0]
            for col_idx in col_start_end:
                current = matrix[row_idx][col_idx]
                if current > max_before:
                    visibility[row_idx][col_idx] = True
                    max_before = current

        # from right to left
        for row_idx in row_start_end:
            max_before = matrix[row_idx][-1]
            for col_idx in col_end_start:
                current = matrix[row_idx][col_idx]
                if current > max_before:
                    visibility[row_idx][col_idx] = True
                    max_before = current

        count = 0
        for row in visibility:
            for visible in row:
                if visible:
                    count += 1

        print(count)


if __name__ == "__main__":
    main()
