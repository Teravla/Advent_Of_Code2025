import os
import re
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpInteger

file_path = os.path.join(os.path.dirname(__file__), "..", "resources.txt")


def parse_machine(line):
    # Extract buttons
    buttons = [tuple(map(int, b.split(","))) for b in re.findall(r"\((.*?)\)", line)]
    # Extract target counters
    target = tuple(map(int, re.search(r"\{(.*?)\}", line).group(1).split(",")))
    return {"buttons": buttons, "target": target}


def min_button_presses_ilp(target, buttons):
    """Compute minimum total button presses using integer linear programming"""
    n_buttons = len(buttons)
    n_counters = len(target)
    # Variables: number of times each button is pressed
    x = [LpVariable(f"x{i}", lowBound=0, cat=LpInteger) for i in range(n_buttons)]

    # Define problem
    prob = LpProblem("JoltageCounters", LpMinimize)
    prob += lpSum(x)  # minimize total presses

    # Constraints: sum of button contributions = target counters
    for j in range(n_counters):
        prob += lpSum(x[i] for i in range(n_buttons) if j in buttons[i]) == target[j]

    prob.solve()
    # Return total presses
    return int(sum(v.varValue for v in x))


def main():
    total_presses = 0
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            machine = parse_machine(line)
            presses = min_button_presses_ilp(machine["target"], machine["buttons"])
            total_presses += presses

    print("Total minimal button presses for all machines:", total_presses)


if __name__ == "__main__":
    main()
