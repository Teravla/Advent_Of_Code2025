# Part One and Two


def count_zeros_during_file(filename):
    """
    Reads a file containing rotation instructions and counts how many times
    the dial points at 0 during the rotations.

    The dial is assumed to have positions from 0 to 99 (total 100 positions),
    starting at position 50.

    Parameters:
        filename (str): The path to the input file. Each line should be a rotation
                        instruction in the format "<direction><value>", where
                        <direction> is 'R' for right or 'L' for left, and
                        <value> is the number of steps to rotate.

    Returns:
        int: The total number of times the dial points at 0 during all rotations.
    """

    pos = 50  # Initial position of the dial
    zero_count = 0  # Counter for how many times the dial reaches position 0

    # Open the input file for reading
    with open(filename, "r") as file:
        # Process the file line by line
        for line in file:
            rotation = line.strip()  # Remove leading/trailing whitespace
            if not rotation:
                continue  # Skip empty lines

            direction = rotation[0]  # First character indicates rotation direction
            try:
                value = int(
                    rotation[1:]
                )  # Remaining characters are the number of steps
            except ValueError:
                # If the line cannot be converted to an integer, skip it
                print(f"Skipping invalid line: {rotation}")
                continue

            # Rotate to the right
            if direction == "R":
                for _ in range(value):
                    pos = (
                        pos + 1
                    ) % 100  # Increment position and wrap around using modulo 100
                    if pos == 0:
                        zero_count += (
                            1  # Increment zero counter whenever position reaches 0
                        )

            # Rotate to the left
            elif direction == "L":
                for _ in range(value):
                    pos = (
                        pos - 1
                    ) % 100  # Decrement position and wrap around using modulo 100
                    if pos == 0:
                        zero_count += (
                            1  # Increment zero counter whenever position reaches 0
                        )

            # If the direction is not recognized, skip the line
            else:
                print(f"Skipping unknown direction: {rotation}")
                continue

    return zero_count  # Return the total count of zeros encountered


if __name__ == "__main__":
    filename = (
        "rotations.txt"  # Path to the input file containing rotation instructions
    )
    password = count_zeros_during_file(filename)
    print(f"The Part Two password is: {password}")  # Print the final count of zeros
