import os
import webbrowser
from typing import List, Dict


class Point:
    def __init__(self, s: str):
        self.x, self.y = [int(p) for p in s.split(",")]

    def __repr__(self) -> str:
        return f"Pt({self.x}, {self.y})"


def read_points(file_path: str) -> List[Point]:
    """Reads points from a file and returns a list of Point objects"""
    with open(file_path, "r") as file:
        return [Point(line.strip()) for line in file if line.strip()]


def compress_axis(all_t: List[int]) -> Dict[int, int]:
    """Compresses coordinates to a smaller range while preserving order"""
    all_t = sorted(set(all_t))
    mapping = {all_t[0]: 0}
    idx = 1
    for i in range(1, len(all_t)):
        if all_t[i] > all_t[i - 1] + 1:
            idx += 1
        mapping[all_t[i]] = idx
        idx += 1
    return mapping


def create_canvas(points: List[Point], width: int, height: int, xx_by_x: Dict[int, int], yy_by_y: Dict[int, int]):
    """Creates and fills the canvas with polygon edges"""
    canvas = [[0] * width for _ in range(height)]
    
    for i in range(len(points)):
        a = points[i]
        b = points[(i + 1) % len(points)]
        if a.x == b.x:
            x = xx_by_x[a.x]
            y0, y1 = sorted([yy_by_y[a.y], yy_by_y[b.y]])
            for y in range(y0, y1 + 1):
                canvas[y][x] = 1
        elif a.y == b.y:
            y = yy_by_y[a.y]
            x0, x1 = sorted([xx_by_x[a.x], xx_by_x[b.x]])
            for x in range(x0, x1 + 1):
                canvas[y][x] = 1
    return canvas


def fill_interior(canvas, height: int, width: int):
    """Fills interior using scanline algorithm"""
    for y in range(height):
        inside = 0
        for x in range(width):
            if canvas[y][x] != 0:
                inside = 1 - inside
            if inside:
                canvas[y][x] = 1


def compute_prefix_sum(canvas, height: int, width: int):
    """Computes 2D prefix sum array"""
    prefix_sum = [[0] * (width + 1) for _ in range(height + 1)]
    for y in range(1, height + 1):
        for x in range(1, width + 1):
            prefix_sum[y][x] = (
                prefix_sum[y][x - 1]
                + prefix_sum[y - 1][x]
                - prefix_sum[y - 1][x - 1]
                + canvas[y - 1][x - 1]
            )
    return prefix_sum


def find_largest_rectangle(points: List[Point], prefix_sum, xx_by_x: Dict[int, int], yy_by_y: Dict[int, int]):
    """Finds the largest rectangle within filled region"""
    def is_filled(x0, x1, y0, y1):
        xx0 = xx_by_x[x0]
        xx1 = xx_by_x[x1]
        yy0 = yy_by_y[y0]
        yy1 = yy_by_y[y1]
        filled = (
            prefix_sum[yy1 + 1][xx1 + 1]
            - prefix_sum[yy0][xx1 + 1]
            - prefix_sum[yy1 + 1][xx0]
            + prefix_sum[yy0][xx0]
        )
        area = (yy1 - yy0 + 1) * (xx1 - xx0 + 1)
        return filled == area

    max_area = 0
    max_rect = None
    n = len(points)
    for i, a in enumerate(points):
        for j in range(i + 1, n):
            b = points[j]
            x0, x1 = sorted([a.x, b.x])
            y0, y1 = sorted([a.y, b.y])
            area = (x1 - x0 + 1) * (y1 - y0 + 1)
            if area > max_area and is_filled(x0, x1, y0, y1):
                max_area = area
                max_rect = (x0, y0, x1, y1)
    return max_rect


def generate_svg_lines(points: List[Point], xx_by_x: Dict[int, int], yy_by_y: Dict[int, int], scale: float) -> str:
    """Generates SVG lines for polygon edges"""
    svg_lines = ""
    for i in range(len(points)):
        a = points[i]
        b = points[(i + 1) % len(points)]
        x1 = xx_by_x[a.x] * scale + scale / 2
        y1 = yy_by_y[a.y] * scale + scale / 2
        x2 = xx_by_x[b.x] * scale + scale / 2
        y2 = yy_by_y[b.y] * scale + scale / 2
        svg_lines += f'<line class="line" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"></line>\n'
    return svg_lines


def generate_svg_points(points: List[Point], xx_by_x: Dict[int, int], yy_by_y: Dict[int, int], scale: float, point_size: float) -> str:
    """Generates SVG rectangles for points"""
    svg_points = ""
    for p in points:
        nx = xx_by_x[p.x] * scale
        ny = yy_by_y[p.y] * scale
        svg_points += f'<rect class="tile" x="{nx}" y="{ny}" width="{point_size}" height="{point_size}"></rect>\n'
    return svg_points


def generate_svg_rectangle(max_rect, xx_by_x: Dict[int, int], yy_by_y: Dict[int, int], scale: float) -> str:
    """Generates SVG for the largest rectangle"""
    if not max_rect:
        return ""
    
    x0, y0, x1, y1 = max_rect
    nx = xx_by_x[x0] * scale
    ny = yy_by_y[y0] * scale
    w = (xx_by_x[x1] - xx_by_x[x0] + 1) * scale
    h = (yy_by_y[y1] - yy_by_y[y0] + 1) * scale
    
    area = (x1 - x0 + 1) * (y1 - y0 + 1)
    print(f"Aire du plus grand rectangle: {area}")
    
    return f'<rect class="rect" x="{nx}" y="{ny}" width="{w}" height="{h}"></rect>\n'


def get_html_template(width_scale: float, height_scale: float) -> tuple:
    """Returns HTML template parts (head, foot)"""
    html_head = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Zone + Rectangle</title>
        <style>
            body {{ text-align:center; font-family:Arial; }}
            svg {{ border:1px solid black; width:90vw; height:90vh; cursor: grab; }}
            .tile {{ fill:red; stroke:black; stroke-width:0.5; }}
            .line {{ stroke:green; stroke-width:1; fill:none; }}
            .rect {{ fill:blue; stroke:blue; stroke-width:0.5; fill-opacity:0.5; }}
        </style>
    </head>
    <body>
        <h1>Zone + Plus grand rectangle</h1>
        <p>Zoom avec molette et déplacement clic-glisser</p>
        <svg id="grid" viewBox="0 0 {width_scale} {height_scale}">
    """

    html_foot = """
        </svg>
        <script>
            const svg = document.getElementById('grid');
            let viewBox = svg.getAttribute('viewBox').split(' ').map(Number);
            let isDragging = false;
            let start = {};

            svg.addEventListener('wheel', function(e){
                e.preventDefault();
                const cx = viewBox[0]+viewBox[2]/2;
                const cy = viewBox[1]+viewBox[3]/2;
                const scaleFactor = e.deltaY < 0 ? 0.9 : 1.1;
                viewBox[2] *= scaleFactor;
                viewBox[3] *= scaleFactor;
                viewBox[0] = cx - viewBox[2]/2;
                viewBox[1] = cy - viewBox[3]/2;
                svg.setAttribute('viewBox', viewBox.join(' '));
            });

            svg.addEventListener('mousedown', function(e){
                isDragging = true;
                start = {x:e.clientX, y:e.clientY, vb:viewBox.slice()};
                svg.style.cursor='grabbing';
            });

            svg.addEventListener('mousemove', function(e){
                if(isDragging){
                    const dx = (start.x - e.clientX)*(viewBox[2]/svg.clientWidth);
                    const dy = (start.y - e.clientY)*(viewBox[3]/svg.clientHeight);
                    viewBox[0] = start.vb[0]+dx;
                    viewBox[1] = start.vb[1]+dy;
                    svg.setAttribute('viewBox', viewBox.join(' '));
                }
            });

            svg.addEventListener('mouseup', function(e){
                isDragging = false;
                svg.style.cursor='grab';
            });

            svg.addEventListener('mouseleave', function(e){
                isDragging = false;
                svg.style.cursor='grab';
            });
        </script>
    </body>
    </html>
    """
    return html_head, html_foot


def generate_html_zone(points: List[Point]):
    file_name = os.path.join(os.path.dirname(__file__), "zone_rectangle.html")
    if not points:
        return

    all_x = sorted({p.x for p in points})
    all_y = sorted({p.y for p in points})
    xx_by_x = compress_axis(all_x)
    yy_by_y = compress_axis(all_y)

    width = xx_by_x[all_x[-1]] + 1
    height = yy_by_y[all_y[-1]] + 1
    scale = 1000 / max(width, height)
    point_size = scale * 0.8

    canvas = create_canvas(points, width, height, xx_by_x, yy_by_y)
    fill_interior(canvas, height, width)
    prefix_sum = compute_prefix_sum(canvas, height, width)
    max_rect = find_largest_rectangle(points, prefix_sum, xx_by_x, yy_by_y)

    html_head, html_foot = get_html_template(width * scale, height * scale)
    html_head += generate_svg_lines(points, xx_by_x, yy_by_y, scale)
    html_body = generate_svg_points(points, xx_by_x, yy_by_y, scale, point_size)
    html_body += generate_svg_rectangle(max_rect, xx_by_x, yy_by_y, scale)

    with open(file_name, "w", encoding="utf-8") as f:
        f.write(html_head + html_body + html_foot)

    webbrowser.open_new_tab(file_name)


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "..", "resources.txt")
    points = read_points(file_path)
    generate_html_zone(points)
