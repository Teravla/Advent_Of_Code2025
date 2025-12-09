import os
from math import dist
from itertools import combinations

# Load data
file_path = os.path.join(os.path.dirname(__file__), "..", "resources.txt")
with open(file_path) as f:
    points = [tuple(map(int, line.strip().split(","))) for line in f.readlines()]

print(f"Loaded {len(points)} junction boxes.")

# Union-Find setup
parent = list(range(len(points)))
size = [1] * len(points)


def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])
    return parent[x]


def union(x, y):
    xr, yr = find(x), find(y)
    if xr == yr:
        return False
    if size[xr] < size[yr]:
        xr, yr = yr, xr
    parent[yr] = xr
    size[xr] += size[yr]
    return True


# Compute all pairwise distances
edges = [
    (dist(points[i], points[j]), i, j) for i, j in combinations(range(len(points)), 2)
]
edges.sort(key=lambda x: x[0])

# Connect pairs until all are in one circuit
total_circuits = len(points)
last_pair = None

for d, i, j in edges:
    if union(i, j):
        total_circuits -= 1
        last_pair = (i, j)  # update last pair that merged circuits
        if total_circuits == 1:
            break

i, j = last_pair
result = points[i][0] * points[j][0]
print(f"Last connected junctions: {points[i]} and {points[j]}")
print("Result (X coordinates multiplied):", result)
