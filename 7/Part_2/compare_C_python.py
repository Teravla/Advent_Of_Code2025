import subprocess
import time
import os
import pandas as pd
import matplotlib.pyplot as plt


def run_python_script(script_path):
    """Exécute un script Python et mesure le temps d'exécution"""
    start = time.perf_counter()
    result = subprocess.run(["python", script_path], capture_output=True, text=True)
    end = time.perf_counter()
    elapsed = end - start
    output = result.stdout.strip()
    return elapsed, output


def main():
    base_dir = os.path.dirname(__file__)
    scripts = ["main_lru_cache.py", "main_dynamic_programming.py", "main_sparse.py"]
    results = []
    time_label = "Execution Time (s)"

    # Python scripts
    for script in scripts:
        path = os.path.join(base_dir, script)
        if not os.path.exists(path):
            continue
        elapsed, output = run_python_script(path)
        results.append({"Script": script, "Time": elapsed, "Output": output})

    c_time = 0.000136988
    c_output = "Total timelines: 3806264447357"
    results.append({"Script": "C (compiled)", "Time": c_time, "Output": c_output})

    df = pd.DataFrame(results)

    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Python vs C Execution Times", fontsize=16)
    # Horizontal bars
    axs[0, 0].barh(df["Script"], df["Time"], color="skyblue")
    axs[0, 0].set_xlabel(time_label)
    axs[0, 0].set_title("Horizontal Bars")
    axs[0, 0].set_title("Horizontal Bars")
    for i, v in enumerate(df["Time"]):
        axs[0, 0].text(v + 0.00001, i, f"{v:.6f}s", va="center")
    # Vertical bars
    axs[0, 1].bar(df["Script"], df["Time"], color="salmon")
    axs[0, 1].set_ylabel(time_label)
    axs[0, 1].set_title("Vertical Bars")
    axs[0, 1].set_title("Vertical Bars")
    for i, v in enumerate(df["Time"]):
        axs[0, 1].text(i, v + 0.00001, f"{v:.6f}s", ha="center")
    # Scatter plot
    axs[1, 0].scatter(df["Script"], df["Time"], color="green", s=100)
    axs[1, 0].set_ylabel(time_label)
    axs[1, 0].set_title("Scatter Plot")
    axs[1, 0].set_title("Scatter Plot")
    for i, v in enumerate(df["Time"]):
        axs[1, 0].text(i, v + 0.00001, f"{v:.6f}s", ha="center")
    # Line plot
    axs[1, 1].plot(df["Script"], df["Time"], marker="o", linestyle="-", color="purple")
    axs[1, 1].set_ylabel(time_label)
    axs[1, 1].set_title("Line Plot")
    axs[1, 1].set_title("Line Plot")
    for i, v in enumerate(df["Time"]):
        axs[1, 1].text(i, v + 0.00001, f"{v:.6f}s", ha="center")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()


if __name__ == "__main__":
    main()
