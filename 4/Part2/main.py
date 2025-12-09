import os


def count_neighbors(grid, r, c):
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    count = 0
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "@":
            count += 1
    return count


def simulate_removal(grid):
    total_removed = 0
    rows, cols = len(grid), len(grid[0])
    grid = [list(row) for row in grid]

    while True:
        to_remove = []
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "@" and count_neighbors(grid, r, c) < 4:
                    to_remove.append((r, c))
        if not to_remove:
            break
        for r, c in to_remove:
            grid[r][c] = "."

        total_removed += len(to_remove)

    return total_removed


def main():
    try:
        resource_file = os.path.join(os.path.dirname(__file__), "..", "resources.txt")
        with open(resource_file, "r") as f:
            grid = [line.rstrip("\n") for line in f]
    except FileNotFoundError:
        print("Erreur : fichier 'resources.txt' introuvable.")
        return

    result = simulate_removal(grid)
    print("Total de rouleaux retirés :", result)


if __name__ == "__main__":
    main()
