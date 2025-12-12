import os
from collections import defaultdict
from typing import Dict, List


def load_graph(file_path: str) -> Dict[str, List[str]]:
    """
    Load a directed graph from a file.

    :param file_path: Path to the file containing the graph data
    :return: A dictionary representing the directed graph
    """
    graph = defaultdict(list)
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            src, dests_raw = line.split(":")
            src = src.strip()
            dests = [d.strip() for d in dests_raw.split() if d.strip()]
            graph[src] = dests
    return graph


def count_paths(graph: Dict[str, List[str]], start: str, end: str) -> int:
    """
    Count the number of directed paths from start to end in the graph.

    :param graph: The directed graph represented as a dictionary
    :param start: The starting node for path counting
    :param end: The ending node for path counting
    :return: The number of directed paths from start to end
    """
    memo = {}

    def dfs(node: str) -> int:
        if node == end:
            return 1
        if node in memo:
            return memo[node]

        total = 0
        for nxt in graph.get(node, []):
            total += dfs(nxt)

        memo[node] = total
        return total

    return dfs(start)


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "..", "resources.txt")
    graph = load_graph(file_path)

    start = "svr"
    end = "out"
    must1 = "dac"
    must2 = "fft"

    for needed in (start, end, must1, must2):
        if needed not in graph and not any(needed in v for v in graph.values()):
            raise ValueError(
                f"Le nœud requis '{needed}' est introuvable dans le graphe."
            )

    svr_to_dac = count_paths(graph, start, must1)
    svr_to_fft = count_paths(graph, start, must2)

    dac_to_fft = count_paths(graph, must1, must2)
    fft_to_dac = count_paths(graph, must2, must1)

    dac_to_out = count_paths(graph, must1, end)
    fft_to_out = count_paths(graph, must2, end)

    path_count_dac_fft = svr_to_dac * dac_to_fft * fft_to_out

    path_count_fft_dac = svr_to_fft * fft_to_dac * dac_to_out

    total_valid_paths = path_count_dac_fft + path_count_fft_dac

    print(
        "Nombre total de chemins svr → out qui passent par dac et fft :",
        total_valid_paths,
    )
