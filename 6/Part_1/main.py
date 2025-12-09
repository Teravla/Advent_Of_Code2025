import os


def load_grid(filename="resources.txt"):
    with open(filename, "r") as f:
        lines = [line.rstrip("\n") for line in f]
    width = max(len(line) for line in lines)
    return [line.ljust(width) for line in lines]


def split_into_blocks(grid):
    height = len(grid)
    width = len(grid[0])

    blocks = []
    current_cols = []

    def flush():
        if current_cols:
            blocks.append(current_cols[:])

    for c in range(width):
        if all(grid[r][c] == " " for r in range(height)):
            flush()
            current_cols = []
        else:
            current_cols.append(c)

    flush()
    return blocks


def extract_problem(grid, cols):
    height = len(grid)

    numbers = []

    # Rows except last = numbers
    for r in range(height - 1):
        row = grid[r]
        # Keep only chars inside block columns
        segment = "".join(row[c] for c in cols)
        # Extract digits
        digits = "".join(ch for ch in segment if ch.isdigit())
        if digits:
            numbers.append(int(digits))

    # Last row = operator
    op_row = grid[-1]
    op = None
    for c in cols:
        if op_row[c] in "+*":
            op = op_row[c]
            break

    return numbers, op


def solve_problem(numbers, op):
    if op == "+":
        return sum(numbers)
    else:  # op == "*"
        prod = 1
        for n in numbers:
            prod *= n
        return prod


def main():
    try:
        resources_file = os.path.join(os.path.dirname(__file__), "..",  "resources.txt")
        grid = load_grid(resources_file)
    except FileNotFoundError:
        print("Missing resources.txt")
        return

    blocks = split_into_blocks(grid)
    total = 0

    for cols in blocks:
        nums, op = extract_problem(grid, cols)
        total += solve_problem(nums, op)

    print("Grand total:", total)


if __name__ == "__main__":
    main()
