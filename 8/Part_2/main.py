import os
from math import dist
from itertools import combinations

# ---------------------------
# Load the junction box data
# ---------------------------

# Construct the path to the input file "resources.txt"
# It is assumed to be one level above this script's directory
file_path = os.path.join(os.path.dirname(__file__), "..", "resources.txt")

# Read the file and parse each line as a tuple of integers (X, Y, Z coordinates)
with open(file_path) as f:
    points = [tuple(map(int, line.strip().split(","))) for line in f.readlines()]

print(f"Loaded {len(points)} junction boxes.")

# ---------------------------
# Union-Find (Disjoint Set) setup
# ---------------------------

# parent[i] points to the representative of the set containing i
parent = list(range(len(points)))

# size[i] keeps track of the number of junction boxes in the set rooted at i
size = [1] * len(points)


def find(x):
    """
    Find the root of the set containing x.
    Implements path compression to flatten the tree for efficiency.
    """
    if parent[x] != x:
        parent[x] = find(parent[x])  # recursive call and path compression
    return parent[x]


def union(x, y):
    """
    Merge the sets containing x and y.
    Uses union by size to keep trees shallow.

    Returns:
        True if a union was performed (sets were separate)
        False if x and y were already in the same set
    """
    xr, yr = find(x), find(y)  # find roots of both sets
    if xr == yr:
        return False  # already in the same set, nothing to do
    # Union by size: attach smaller tree under the larger one
    if size[xr] < size[yr]:
        xr, yr = yr, xr
    parent[yr] = xr
    size[xr] += size[yr]
    return True


# ---------------------------
# Compute all pairwise distances
# ---------------------------

# Generate all unique pairs of junction boxes (i, j)
# Compute the Euclidean distance between each pair
edges = [
    (dist(points[i], points[j]), i, j) for i, j in combinations(range(len(points)), 2)
]

# Sort the pairs by distance in ascending order
# The closest junction boxes will appear first
edges.sort(key=lambda x: x[0])

# ---------------------------
# Connect pairs until a single circuit is formed
# ---------------------------

total_circuits = len(points)  # initially, each junction box is its own circuit
last_pair = None  # will store the last pair that merges the final two circuits

for d, i, j in edges:
    # Attempt to merge the circuits of junction boxes i and j
    if union(i, j):
        total_circuits -= 1  # one less separate circuit now
        last_pair = (i, j)  # update the last pair that caused a merge

        # Stop as soon as all junction boxes are in one circuit
        if total_circuits == 1:
            break

# ---------------------------
# Compute the final answer
# ---------------------------

# The last two junction boxes connected are in last_pair
i, j = last_pair

# The puzzle asks for the product of their X coordinates
result = points[i][0] * points[j][0]

# Print detailed information
print(f"Last connected junctions: {points[i]} and {points[j]}")
print("Result (X coordinates multiplied):", result)
