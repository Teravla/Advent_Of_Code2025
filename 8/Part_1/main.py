import os
from math import dist
from itertools import combinations
import json

MAX_CONNECTIONS = 1000

# Load data
file_path = os.path.join(os.path.dirname(__file__), "..", "resources.txt")
with open(file_path) as f:
    points = [tuple(map(int, line.strip().split(","))) for line in f.readlines()]

print(f"Loaded {len(points)} junction boxes.")

# Union-Find (Disjoint Set Union) setup
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
    # Union by size
    if size[xr] < size[yr]:
        xr, yr = yr, xr
    parent[yr] = xr
    size[xr] += size[yr]
    return True


# Compute all pairwise distances
edges = []
for i, j in combinations(range(len(points)), 2):
    d = dist(points[i], points[j])
    edges.append((d, i, j))

print(f"Computed {len(edges)} pairwise distances.")

# Sort by distance
edges.sort(key=lambda x: x[0])

# Connect 1000 closest pairs
connections = 0
edges_to_connect = MAX_CONNECTIONS
for idx, (d, i, j) in enumerate(edges):
    union(i, j)  # merge circuits if needed
    if idx + 1 == edges_to_connect:
        break

# Compute sizes of all circuits
circuit_sizes = {}
for i in range(len(points)):
    root = find(i)
    circuit_sizes[root] = circuit_sizes.get(root, 0) + 1

print(f"Total circuits after connections: {len(circuit_sizes)}")
# Multiply the sizes of the three largest circuits (handle <3 circuits)
largest_sizes = sorted(circuit_sizes.values(), reverse=True)
result = 1
for s in largest_sizes[:3]:
    print("Circuit size:", s)
    result *= s

print("Result:", result)

# Prepare connections (for visualization, take first 1000 edges)
visual_edges = [(i, j) for _, i, j in edges[:MAX_CONNECTIONS]]

# Save to JSON
json_path = os.path.join(os.path.dirname(__file__), "circuit_data.json")
if not os.path.exists(os.path.dirname(json_path)):
    os.makedirs(os.path.dirname(json_path))
with open(json_path, "w") as f:
    json.dump({"points": points, "edges": visual_edges}, f)
