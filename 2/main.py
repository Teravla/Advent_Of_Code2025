import os
import time

# Determine the absolute directory of the current script
actual_dir = os.path.dirname(os.path.abspath(__file__))

# Record the total start time for performance measurement
start_total = time.time()


def is_repeated_pattern(n: int) -> bool:
    """
    Determines whether the integer n can be expressed as a repeated pattern.

    A repeated pattern means the number's digits can be split into equal-sized
    chunks that repeat at least twice to form the original number.

    For example:
        1212 -> True  (pattern "12" repeated)
        123123123 -> True  (pattern "123" repeated)
        1234 -> False (no repeated pattern)

    Parameters:
        n (int): The number to check for repeated digit patterns.

    Returns:
        bool: True if n has a repeated pattern, False otherwise.
    """
    s = str(n)  # Convert the number to a string for pattern checking
    L = len(s)  # Length of the number in digits

    # Try all possible chunk sizes from 1 up to half the number length
    for k in range(1, L // 2 + 1):
        if L % k == 0:  # Only consider chunk sizes that divide the number length evenly
            chunk = s[:k]  # Take the first chunk
            if s == chunk * (
                L // k
            ):  # Check if repeating the chunk reconstructs the number
                return True

    # If no repeated pattern is found, return False
    return False


def sum_invalid_ids_from_file(path: str) -> int:
    """
    Reads ranges of numbers from a file and sums all numbers that contain repeated patterns.

    The input file is expected to contain a single line with comma-separated ranges,
    each in the format "low-high". For example:
        10-20,100-120,200-202

    For each range, all numbers are tested using is_repeated_pattern. The sum of
    numbers with repeated patterns is accumulated and returned.

    Performance is measured per range and for the total computation.

    Parameters:
        path (str): The path to the input file containing number ranges.

    Returns:
        int: The total sum of all numbers with repeated digit patterns in all ranges.
    """
    # Read the input file as a single line
    with open(path, "r", encoding="utf-8") as f:
        input_line = f.read().strip()

    total = 0  # Total sum of all numbers with repeated patterns
    ranges = input_line.split(",")  # Split the line into individual ranges

    # Process each range separately
    for r in ranges:
        if not r.strip():  # Skip empty entries
            continue

        # Split range into lower and upper bounds
        low_str, high_str = r.split("-")
        low, high = int(low_str), int(high_str)

        # Measure time taken to process this range
        start_range = time.time()
        range_sum = 0  # Sum of repeated-pattern numbers within this range

        # Iterate through all numbers in the range, inclusive
        for n in range(low, high + 1):
            if is_repeated_pattern(n):
                range_sum += n  # Accumulate if number has repeated pattern

        total += range_sum
        # Print performance and partial sum for this range
        print(
            f"Range {low}-{high} processed in {time.time() - start_range:.4f}s, sum={range_sum}"
        )

    # Print total sum and overall execution time
    print(f"Total sum={total}, executed in {time.time() - start_total:.4f}s")

    return total


if __name__ == "__main__":
    input_file_path = os.path.join(actual_dir, "resources.txt")
    print(sum_invalid_ids_from_file(input_file_path))
