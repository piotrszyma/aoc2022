# Day 8


def print_visibility(v):
    for row in v:
        print(row)


def get_score(
    matrix: list[list[int]], row_idx: int, col_idx: int, row_diff: int, col_diff: int
):
    tree_height = matrix[row_idx][col_idx]
    trees_count = 0
    while True:
        row_idx += row_diff
        col_idx += col_diff

        if row_idx < 0 or col_idx < 0:
            return trees_count

        if row_idx > len(matrix) - 1 or col_idx > len(matrix[0]) - 1:
            return trees_count

        shifted_tree = matrix[row_idx][col_idx]

        if shifted_tree >= tree_height:
            return trees_count + 1
        trees_count += 1


def main():
    with open("day8.input.txt", "r") as f:
        matrix: list[list[int]] = []

        line = []

        for line in f:
            line = line.strip()
            row = [int(cell) for cell in line]
            matrix.append(row)

        assert line

        scenic_score = -1

        for row_idx, row in enumerate(matrix):
            for col_idx, _ in enumerate(row):
                up_score = get_score(matrix, row_idx, col_idx, -1, 0)
                left_score = get_score(matrix, row_idx, col_idx, 0, -1)
                right_score = get_score(matrix, row_idx, col_idx, 0, 1)
                down_score = get_score(matrix, row_idx, col_idx, 1, 0)

                this_scenic_score = left_score * right_score * up_score * down_score

                scenic_score = max(scenic_score, this_scenic_score)

        print(scenic_score)


if __name__ == "__main__":
    main()
