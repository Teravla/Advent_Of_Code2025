import os


def load_grid(filename="resources.txt"):
    """
    Load the grid from a text file.

    Each line in the file represents a row in the grid.
    Each character in the line represents a cell:
        - '.' : empty space where a tachyon can propagate
        - '^' : a splitter that divides the tachyon into left and right
        - 'S' : starting point of the tachyon

    Args:
        filename (str): Path to the input file.

    Returns:
        list[list[str]]: 2D grid representing the tachyon manifold.
    """
    with open(filename, "r") as f:
        return [list(line.rstrip("\n")) for line in f]


def find_start(grid):
    """
    Find the coordinates of the starting point 'S' in the grid.

    Args:
        grid (list[list[str]]): The 2D grid.

    Returns:
        tuple[int, int]: Row and column of the starting point.

    Raises:
        ValueError: If 'S' is not found in the grid.
    """
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == "S":
                return r, c
    raise ValueError("Start 'S' not found")


def propagate_timeline(grid, dp, r, c, count, rows, cols):
    """
    Propagate the number of active timelines from cell (r, c)
    to the next row according to the tachyon rules.

    Rules:
        - If the cell is '.' (empty space), the timeline continues straight down.
        - If the cell is '^' (splitter), the timeline splits into left and right.
        - Boundaries are respected to avoid indexing outside the grid.

    Args:
        grid (list[list[str]]): The 2D grid.
        dp (list[list[int]]): DP table storing the number of timelines reaching each cell.
        r (int): Current row index.
        c (int): Current column index.
        count (int): Number of active timelines at this cell.
        rows (int): Total number of rows in the grid.
        cols (int): Total number of columns in the grid.
    """
    cell = grid[r][c]
    if cell == "." and r + 1 < rows:
        # Timeline continues straight down
        dp[r + 1][c] += count
    elif cell == "^" and r + 1 < rows:
        # Timeline splits into left and right
        if c - 1 >= 0:
            dp[r + 1][c - 1] += count
        if c + 1 < cols:
            dp[r + 1][c + 1] += count


def count_timelines_dp(grid):
    """
    Count the total number of possible timelines using dynamic programming.

    Dynamic programming approach:
        - dp[r][c] stores the number of timelines reaching cell (r, c)
        - Start with 1 timeline directly below 'S'
        - Iterate row by row, propagating timelines according to the rules
        - Sum all timelines in the last row for the final count

    Args:
        grid (list[list[str]]): The 2D grid.

    Returns:
        int: Total number of timelines that reach the bottom of the grid.
    """
    rows, cols = len(grid), len(grid[0])
    # Initialize DP table with zeros
    dp = [[0] * cols for _ in range(rows)]

    # Locate starting point 'S'
    start_r, start_c = find_start(grid)

    # Initialize the first active timeline directly below 'S'
    dp[start_r + 1][start_c] = 1

    # Iterate through each row starting from the row below 'S'
    for r in range(start_r + 1, rows):
        for c in range(cols):
            count = dp[r][c]
            if count > 0:
                # Propagate the timelines from this cell to the next row
                propagate_timeline(grid, dp, r, c, count, rows, cols)

    # Total timelines reaching the bottom row
    total = sum(dp[rows - 1][c] for c in range(cols))
    return total


if __name__ == "__main__":
    # Construct the path to resources.txt in the parent directory
    resources_file = os.path.join(os.path.dirname(__file__), "..", "resources.txt")

    # Load the tachyon manifold grid
    grid = load_grid(resources_file)

    # Count total timelines using DP
    total = count_timelines_dp(grid)

    # Output the result
    print("Total timelines:", total)
