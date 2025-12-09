import os
import time
from copy import deepcopy
from flask import Flask, Response, render_template_string
from collections import deque

app = Flask(__name__)
TIME_DELAY = 0.001  # Delay between frames in seconds


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


def process_cell(g, r, c, stack, prioritize_right):
    """Process a single cell and add next states to stack."""
    cell = g[r][c]
    if cell == "^":
        moves = (
            [(r + 1, c + 1), (r + 1, c - 1)]
            if prioritize_right
            else [(r + 1, c - 1), (r + 1, c + 1)]
        )
        for nr, nc in moves:
            if in_bounds(g, nr, nc):
                stack.append((deepcopy(g), nr, nc))
    elif cell == ".":
        g[r][c] = "|"
        if in_bounds(g, r + 1, c):
            stack.append((g, r + 1, c))


def generate_timelines(grid, prioritize_right=False):
    start_r, start_c = find_start(grid)
    stack = [(deepcopy(grid), start_r + 1, start_c)]
    while stack:
        g, r, c = stack.pop()
        if not in_bounds(g, r, c):
            yield g
            continue
        process_cell(g, r, c, stack, prioritize_right)
        yield g


def display_timelines_merged(grid):
    left_gen = generate_timelines(deepcopy(grid), prioritize_right=False)
    right_gen = generate_timelines(deepcopy(grid), prioritize_right=True)
    count = 0

    while True:
        try:
            left = next(left_gen)
            right = next(right_gen)
            count += 1
        except StopIteration:
            break
        merged = []
        for lr, rr, original in zip(left, right, grid):
            row = []
            for lcell, rcell, ocell in zip(lr, rr, original):
                if ocell in ("S", "^"):
                    row.append(ocell)
                elif lcell == "|" or rcell == "|":
                    row.append("|")
                else:
                    row.append(".")
            merged.append(row)
        html_grid = "<br>".join("".join(row) for row in merged)
        yield f"data: DISPLAY:{html_grid}\n\n"
        time.sleep(TIME_DELAY)

    yield f"data: FINAL_COUNT:{count}\n\n"


# --- Flask routes ---
HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
<title>Quantum Tachyon Beam - Merged Timelines</title>
<style>
  body { font-family: monospace; white-space: pre; }
  .grid { line-height: 1.1; }
</style>
</head>
<body>
<h2>Quantum Tachyon Beam - Merged Timelines</h2>
<div class="grid" id="timeline"></div>
<p id="count"></p>
<script>
var evtSource = new EventSource("/stream");
evtSource.onmessage = function(e) {
    if(e.data.startsWith("DISPLAY:")) {
        document.getElementById("timeline").innerHTML = e.data.slice(8);
    } else if(e.data.startsWith("FINAL_COUNT:")) {
        document.getElementById("count").textContent = "Total timelines: " + e.data.slice(12);
        evtSource.close();
    }
};
</script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/stream")
def stream():
    try:
        resources_file = os.path.join(os.path.dirname(__file__), "..", "resources.txt")
        grid = load_grid(resources_file)
    except FileNotFoundError:
        return "Missing resources.txt", 404

    return Response(display_timelines_merged(grid), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
