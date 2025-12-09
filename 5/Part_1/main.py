import os


def parse_input(filename="resources.txt"):
    ranges = []
    ids = []

    with open(filename, "r") as f:
        lines = [line.strip() for line in f]

    i = 0
    while i < len(lines) and lines[i] != "":
        start, end = map(int, lines[i].split("-"))
        ranges.append((start, end))
        i += 1

    i += 1

    while i < len(lines):
        if lines[i] != "":
            ids.append(int(lines[i]))
        i += 1

    return ranges, ids


def is_fresh(ingredient_id, ranges):
    for start, end in ranges:
        if start <= ingredient_id <= end:
            return True
    return False


def count_fresh_ids(ranges, available_ids):
    return sum(1 for x in available_ids if is_fresh(x, ranges))


def main():
    try:
        resource_file = os.path.join(os.path.dirname(__file__), "..", "resources.txt")
        ranges, ids = parse_input(resource_file)
    except FileNotFoundError:
        print("Error: 'resources.txt' file not found.")
        return

    result = count_fresh_ids(ranges, ids)
    print("Number of fresh ingredient IDs:", result)


if __name__ == "__main__":
    main()
