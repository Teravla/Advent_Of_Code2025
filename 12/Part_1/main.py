import os


def is_region_valid(region: str, shapes: list[tuple[int, int]]) -> bool:
    """
    Check if a region can fit all required shapes based on area.

    :param region: The region string in the format "WxH: n1 n2 n3 ..."
    :param shapes: List of shapes as (bitmask, area) tuples
    :return: True if the region can fit all required shapes based on area, False otherwise
    """
    dimensions_str, requirements_str = region.split(": ")
    width, height = map(int, dimensions_str.split("x"))

    available_area = width * height
    required_counts = list(map(int, requirements_str.split(" ")))

    # Each shape is stored as (bitmask, area)
    required_area = sum(
        count * shape[1] for count, shape in zip(required_counts, shapes)
    )

    return available_area >= required_area


def solver(data: str) -> int:
    """
    Solve the problem by counting valid regions.

    :param data: Input data containing shape and region descriptions
    :return: Number of valid regions
    """
    chunks = data.strip().split("\n\n")
    shape_chunks = chunks[:-1]
    region_chunk = chunks[-1]

    shapes = []
    for chunk in shape_chunks:
        lines = chunk.split("\n")
        shape_lines = lines[1:]  # skip index line
        flattened_shape = "".join(shape_lines)
        bitmask = int(flattened_shape.translate(str.maketrans("#.", "10")), 2)
        area = flattened_shape.count("#")
        shapes.append((bitmask, area))

    valid_region_count = sum(
        is_region_valid(region_line, shapes) for region_line in region_chunk.split("\n")
    )

    return valid_region_count


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "..", "resources.txt")

    with open(file_path, "r") as f:
        data = f.read()

    print("Part 1 solution:", solver(data))
