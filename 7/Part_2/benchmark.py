import subprocess
import time
import os


def run_script(script_path):
    """Exécute le script et mesure le temps d'exécution"""
    start = time.time()
    result = subprocess.run(["python", script_path], capture_output=True, text=True)
    end = time.time()
    elapsed = end - start
    output = result.stdout.strip()
    return elapsed, output


def main():
    base_dir = os.path.dirname(__file__)
    scripts = ["main_lru_cache.py", "main_dynamic_programming.py", "main_sparse.py"]

    print(f"{'Script':<30} {'Time (s)':<10} Output")
    print("-" * 70)

    for script in scripts:
        path = os.path.join(base_dir, script)
        if not os.path.exists(path):
            print(f"{script:<30} {'N/A':<10} File not found")
            continue
        elapsed, output = run_script(path)
        print(f"{script:<30} {elapsed:<10.4f} {output}")


if __name__ == "__main__":
    main()
