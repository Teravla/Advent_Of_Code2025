import os
import time
from collections import deque
from flask import Flask, Response, render_template_string

app = Flask(__name__)


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


def process_beam(grid, r, c, beams):
    """Process a single beam and return division count and whether line was updated."""
    if not in_bounds(grid, r, c):
        return 0, False

    cell = grid[r][c]
    divisions = 0
    line_updated = False

    if cell == "^":
        divisions = 1
        if in_bounds(grid, r + 1, c - 1):
            beams.append((r + 1, c - 1))
        if in_bounds(grid, r + 1, c + 1):
            beams.append((r + 1, c + 1))
    elif cell == "." and in_bounds(grid, r + 1, c):
        beams.append((r + 1, c))

    # Mark the beam but preserve ^ and S
    if grid[r][c] == ".":
        grid[r][c] = "|"
        line_updated = True

    return divisions, line_updated


def simulate_beams(grid):
    beams = deque()
    start_r, start_c = find_start(grid)
    beams.append((start_r + 1, start_c))
    divisions = 0

    # Yield initial full grid
    html_grid = "<br>".join("".join(row) for row in grid)
    yield f"data: {html_grid}\n\n"
    time.sleep(0.1)

    while beams:
        # Track lines that changed this iteration
        lines_to_update = set()

        # Process current size of queue to avoid partial line updates
        for _ in range(len(beams)):
            r, c = beams.popleft()
            div_count, line_updated = process_beam(grid, r, c, beams)
            divisions += div_count
            if line_updated:
                lines_to_update.add(r)

        # Yield full line(s) that changed this round
        for row_index in sorted(lines_to_update):
            line_html = "".join(grid[row_index])
            yield f"data: LINE:{row_index}:{line_html}\n\n"

        time.sleep(0.05)  # small delay for animation

    # Final divisions
    yield f"data: FINAL_DIVISIONS:{divisions}\n\n"


HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
<title>Tachyon Beam Simulation</title>
<style>
  body { font-family: monospace; white-space: pre; }
  .grid { line-height: 1.1; }
</style>
</head>
<body>
<h2>Tachyon Beam Simulation</h2>
<div class="grid" id="grid"></div>
<p id="divisions"></p>
<script>
  var gridDiv = document.getElementById("grid");
  var gridLines = [];
  var evtSource = new EventSource("/stream");

  evtSource.onmessage = function(e) {
    if (e.data.startsWith("FINAL_DIVISIONS:")) {
      document.getElementById("divisions").textContent = 
        "Total divisions: " + e.data.split(":")[1];
      evtSource.close();
    } else if (e.data.startsWith("LINE:")) {
      var parts = e.data.split(":");
      var index = parseInt(parts[1]);
      var content = parts.slice(2).join(":");
      gridLines[index] = content;
      gridDiv.innerHTML = gridLines.join("<br>");
    } else {
      gridLines = e.data.split("<br>");
      gridDiv.innerHTML = gridLines.join("<br>");
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

    return Response(simulate_beams(grid), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
