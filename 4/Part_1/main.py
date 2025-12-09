import os


def count_neighbors(grid, r, c):
    rows = len(grid)
    cols = len(grid[0])
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    count = 0
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "@":
            count += 1
    return count


def count_accessible_rolls(grid):
    rows = len(grid)
    cols = len(grid[0])
    accessible = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "@" and count_neighbors(grid, r, c) < 4:
                accessible += 1

    return accessible


def main():
    try:
        resource_file = os.path.join(os.path.dirname(__file__), "..", "resources.txt")
        with open(resource_file, "r") as f:
            grid = [line.rstrip("\n") for line in f]
    except FileNotFoundError:
        print("Erreur : le fichier 'resources.txt' n'a pas été trouvé.")
        return

    result = count_accessible_rolls(grid)
    print("Nombre de rouleaux accessibles :", result)


if __name__ == "__main__":
    main()
