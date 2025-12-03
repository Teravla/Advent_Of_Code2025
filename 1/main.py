# Part Two: count every time dial points at 0 during rotation from a file

def count_zeros_during_file(filename):
    pos = 50  # starting position
    zero_count = 0

    with open(filename, 'r') as file:
        for line in file:
            rotation = line.strip()
            if not rotation:
                continue  # skip empty lines
            direction = rotation[0]
            try:
                value = int(rotation[1:])
            except ValueError:
                print(f"Skipping invalid line: {rotation}")
                continue

            if direction == 'R':
                for _ in range(value):
                    pos = (pos + 1) % 100
                    if pos == 0:
                        zero_count += 1
            elif direction == 'L':
                for _ in range(value):
                    pos = (pos - 1) % 100
                    if pos == 0:
                        zero_count += 1
            else:
                print(f"Skipping unknown direction: {rotation}")
                continue

    return zero_count

if __name__ == "__main__":
    filename = "rotations.txt"  # your input file
    password = count_zeros_during_file(filename)
    print(f"The Part Two password is: {password}")
