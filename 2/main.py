import os
import time

actual_dir = os.path.dirname(os.path.abspath(__file__))
start_total = time.time()

def is_repeated_pattern(n: int) -> bool:
    s = str(n)
    L = len(s)

    # Try all possible chunk sizes
    for k in range(1, L // 2 + 1):
        if L % k == 0:
            chunk = s[:k]
            if s == chunk * (L // k):  # Repeated at least twice
                return True

    return False


def sum_invalid_ids_from_file(path: str) -> int:
    # Read the single-line input from the file
    with open(path, "r", encoding="utf-8") as f:
        input_line = f.read().strip()

    total = 0
    ranges = input_line.split(",")

    for r in ranges:
        if not r.strip():
            continue

        low_str, high_str = r.split("-")
        low, high = int(low_str), int(high_str)

        start_range = time.time()
        range_sum = 0
        for n in range(low, high + 1):
            if is_repeated_pattern(n):
                range_sum += n
        total += range_sum
        print(f"Range {low}-{high} processed in {time.time() - start_range:.4f}s, sum={range_sum}")

    print(f"Total sum={total}, executed in {time.time() - start_total:.4f}s")

    return total


# -------------------------
# Solve using resources.txt
print(sum_invalid_ids_from_file(os.path.join(actual_dir, "resources.txt")))
# -------------------------
