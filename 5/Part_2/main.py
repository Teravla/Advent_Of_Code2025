import os


def parse_ranges(filename="resources.txt"):
    ranges = []

    with open(filename, "r") as f:
        lines = [line.strip() for line in f]
    for line in lines:
        if line == "":
            break
        start, end = map(int, line.split("-"))
        ranges.append((start, end))

    return ranges


def merge_ranges(ranges):
    if not ranges:
        return []
    ranges.sort()

    merged = [ranges[0]]

    for start, end in ranges[1:]:
        last_start, last_end = merged[-1]

        if start <= last_end + 1:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))

    return merged


def count_fresh_ids(ranges):
    merged = merge_ranges(ranges)
    total = 0

    for start, end in merged:
        total += (end - start + 1)

    return total


def main():
    try:
        resource_file = os.path.join(os.path.dirname(__file__), "..", "resources.txt")
        ranges = parse_ranges(resource_file)
    except FileNotFoundError:
        print("Error: 'resources.txt' file not found.")
        return

    result = count_fresh_ids(ranges)
    print("Total number of fresh ingredient IDs:", result)


if __name__ == "__main__":
    main()
