import os
from functools import lru_cache


def load_grid(filename="resources.txt"):
    with open(filename, "r") as f:
        return [list(line.rstrip("\n")) for line in f]


def find_start(grid):
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == "S":
                return r, c
    raise ValueError("Start 'S' not found")


def in_bounds(grid, r, c):
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])


def count_timelines(grid):
    @lru_cache(maxsize=None)
    def dfs(r, c):
        if not in_bounds(grid, r, c):
            return 1
        cell = grid[r][c]
        if cell == "^":
            left = dfs(r + 1, c - 1)
            right = dfs(r + 1, c + 1)
            return left + right
        elif cell == "." or cell == "S":
            return dfs(r + 1, c)
        else:
            return 0

    start_r, start_c = find_start(grid)
    return dfs(start_r + 1, start_c)


if __name__ == "__main__":
    resources_file = os.path.join(os.path.dirname(__file__), "..", "resources.txt")
    if not os.path.isfile(resources_file):
        raise FileNotFoundError(f"Resources file not found: {resources_file}")
    grid = load_grid(resources_file)
    total = count_timelines(grid)
    print("Total timelines:", total)
