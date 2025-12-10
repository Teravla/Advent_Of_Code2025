import os
import re
from itertools import combinations


def parse_machine(line: str) -> tuple[list[int], list[list[int]]]:
    """Parse a machine line into target state and button definitions."""
    diagram_match = re.search(r"\[([.#]+)\]", line)
    buttons_matches = re.findall(r"\(([\d,]+)\)", line)

    target = [1 if c == "#" else 0 for c in diagram_match.group(1)]
    buttons = []
    for b in buttons_matches:
        buttons.append([int(x) for x in b.split(",")])
    return target, buttons


def convert_to_vectors(buttons: list[list[int]], n: int) -> list[list[int]]:
    """Convert button definitions to binary vectors."""
    btn_vecs = []
    for b in buttons:
        vec = [0] * n
        for idx in b:
            vec[idx] = 1
        btn_vecs.append(vec)
    return btn_vecs


def calculate_state(combo: tuple[int, ...], btn_vecs: list[list[int]], n: int) -> list[int]:
    """Calculate the resulting state from a combination of button presses."""
    state = [0] * n
    for i in combo:
        for j in range(n):
            state[j] ^= btn_vecs[i][j]
    return state


def min_presses(target, buttons):
    n = len(target)
    m = len(buttons)
    btn_vecs = convert_to_vectors(buttons, n)
    for k in range(1, m + 1):
        for combo in combinations(range(m), k):
            state = calculate_state(combo, btn_vecs, n)
            if state == target:
                return k
    return 0


def main():
    total = 0
    file = os.path.join(os.path.dirname(__file__), "..", "resources.txt")
    with open(file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            target, buttons = parse_machine(line)
            presses = min_presses(target, buttons)
            total += presses
    print("Fewest total button presses:", total)


if __name__ == "__main__":
    main()
