import os
from collections import defaultdict


def load_grid(filename="resources.txt"):
    with open(filename, "r") as f:
        return [list(line.rstrip("\n")) for line in f]


def find_start(grid):
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == "S":
                return r, c
    raise ValueError("Start 'S' not found")


def count_timelines_super_fast(grid):
    rows, cols = len(grid), len(grid[0])
    start_r, start_c = find_start(grid)
    current = {start_c: 1}

    for r in range(start_r + 1, rows):
        next_line = defaultdict(int)
        for c, count in current.items():
            cell = grid[r][c]
            if cell == ".":
                next_line[c] += count
            elif cell == "^":
                if c - 1 >= 0:
                    next_line[c - 1] += count
                if c + 1 < cols:
                    next_line[c + 1] += count
        current = next_line
    return sum(current.values())


if __name__ == "__main__":
    resources_file = os.path.join(os.path.dirname(__file__), "..", "resources.txt")
    grid = load_grid(resources_file)
    total = count_timelines_super_fast(grid)
    print("Total timelines:", total)
