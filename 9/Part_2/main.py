import os
import webbrowser
from typing import List, Tuple
from shapely.geometry import Polygon


def read_points(file_path: str) -> List[Tuple[int, int, str]]:
    points = []
    with open(file_path, "r") as f:
        for line in f:
            if line.strip():
                x_str, y_str = line.strip().split(",")
                points.append((int(x_str), int(y_str), "R"))
    return points


def generate_html_zone(points: List[Tuple[int, int, str]], file_name="zone.html"):
    if not points:
        return

    # min/max pour normalisation
    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)
    width = max_x - min_x + 1
    height = max_y - min_y + 1

    scale = 1000 / max(width, height)

    # Polygon vert et zone azure
    poly_points = [
        ((x - min_x) * scale + scale / 2, (y - min_y) * scale + scale / 2)
        for x, y, _ in points
    ]
    polygon = Polygon(poly_points)

    html_head = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Zone</title>
        <style>
            body {{ text-align:center; font-family:Arial; }}
            svg {{ border:1px solid black; width:90vw; height:90vh; cursor: grab; }}
            .tile {{ fill:red; stroke:black; stroke-width:0.5; }}
            .line {{ stroke:green; stroke-width:{scale*20}; fill:none; }}
            .zone {{ fill:azure; stroke:none; fill-opacity:0.3; }}
        </style>
    </head>
    <body>
        <h1>Zone délimitée</h1>
        <p>Zoom avec molette et déplacement clic-glisser</p>
        <svg id="grid" viewBox="0 0 {width*scale} {height*scale}">
    """

    html_body = ""

    # Dessiner zone délimitée (azure)
    points_str = " ".join([f"{x},{y}" for x, y in poly_points])
    html_body += f'<polygon class="zone" points="{points_str}"></polygon>\n'

    # Tuiles rouges
    for x, y, _ in points:
        nx = (x - min_x) * scale
        ny = (y - min_y) * scale
        html_body += f'<rect class="tile" x="{nx}" y="{ny}" width="{scale}" height="{scale}"></rect>\n'

    # Lignes vertes
    for i in range(len(points)):
        x1 = (points[i][0] - min_x) * scale + scale / 2
        y1 = (points[i][1] - min_y) * scale + scale / 2
        x2 = (points[(i + 1) % len(points)][0] - min_x) * scale + scale / 2
        y2 = (points[(i + 1) % len(points)][1] - min_y) * scale + scale / 2
        html_body += (
            f'<line class="line" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"></line>\n'
        )

    html_foot = """
        </svg>
        <script>
            const svg = document.getElementById('grid');
            let viewBox = svg.getAttribute('viewBox').split(' ').map(Number);
            svg.addEventListener('wheel', function(e){
                e.preventDefault();
                const cx = viewBox[0]+viewBox[2]/2;
                const cy = viewBox[1]+viewBox[3]/2;
                if(e.deltaY<0){ viewBox[2]*=0.9; viewBox[3]*=0.9; }
                else{ viewBox[2]*=1.1; viewBox[3]*=1.1; }
                viewBox[0]=cx-viewBox[2]/2;
                viewBox[1]=cy-viewBox[3]/2;
                svg.setAttribute('viewBox',viewBox.join(' '));
            });
            let isDragging=false;
            let start={};
            svg.addEventListener('mousedown', function(e){
                isDragging=true;
                start={x:e.clientX, y:e.clientY, vb:viewBox.slice()};
                svg.style.cursor='grabbing';
            });
            svg.addEventListener('mousemove', function(e){
                if(isDragging){
                    const dx=(start.x-e.clientX)*(viewBox[2]/svg.clientWidth);
                    const dy=(start.y-e.clientY)*(viewBox[3]/svg.clientHeight);
                    viewBox[0]=start.vb[0]+dx;
                    viewBox[1]=start.vb[1]+dy;
                    svg.setAttribute('viewBox',viewBox.join(' '));
                }
            });
            svg.addEventListener('mouseup', function(e){ isDragging=false; svg.style.cursor='grab'; });
            svg.addEventListener('mouseleave', function(e){ isDragging=false; svg.style.cursor='grab'; });
        </script>
    </body>
    </html>
    """

    with open(file_name, "w", encoding="utf-8") as f:
        f.write(html_head + html_body + html_foot)
    webbrowser.open_new_tab(file_name)


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "..", "resources.txt")
    points = read_points(file_path)
    generate_html_zone(points)
