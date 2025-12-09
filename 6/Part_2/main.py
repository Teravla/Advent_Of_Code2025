import os


def load_grid(filename="resources.txt"):
    """Load and normalize the grid."""
    with open(filename, "r") as f:
        lines = [line.rstrip("\n") for line in f]
    width = max(len(line) for line in lines)
    return [line.ljust(width) for line in lines]


def split_into_blocks(grid):
    """Split the grid into problem blocks (columns separated by fully empty columns)."""
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
    """
    Extract a problem from a block.
    For part 2: read numbers right-to-left in columns,
    top = most significant digit, bottom = least significant digit.
    """
    height = len(grid)
    operator_row = grid[-1]

    numbers = []

    # Each column in the block is a number
    # Read columns right-to-left
    for c in reversed(cols):
        # Digits in the column, top-to-bottom
        digits = "".join(grid[r][c] for r in range(height - 1) if grid[r][c].isdigit())
        if digits:
            numbers.append(int(digits))

    # Find operator (bottom row in the block)
    op = None
    for c in cols:
        if operator_row[c] in "+*":
            op = operator_row[c]
            break

    return numbers, op


def solve_problem(numbers, op):
    if op == "+":
        return sum(numbers)
    elif op == "*":
        result = 1
        for n in numbers:
            result *= n
        return result
    else:
        raise ValueError(f"Unknown operator: {op}")


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
        numbers, op = extract_problem(grid, cols)
        total += solve_problem(numbers, op)

    print("Grand total (Part 2):", total)


if __name__ == "__main__":
    main()
