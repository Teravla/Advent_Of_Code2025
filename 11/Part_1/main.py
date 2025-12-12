import os
from collections import defaultdict


def load_graph(file_path: str) -> dict:
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
            left, right = line.split(":")
            src = left.strip()
            dests = [x.strip() for x in right.split() if x.strip()]
            graph[src] = dests
    return graph


def count_paths(graph: dict, start: str, end: str) -> int:
    """
    Count the number of directed paths from start to end in the graph.
    
    :param graph: The directed graph represented as a dictionary
    :param start: The starting node for path counting
    :param end: The ending node for path counting
    :return: The number of directed paths from start to end
    """
    memo = {}

    def dfs(node):
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

    answer = count_paths(graph, "you", "out")
    print("Number of paths from 'you' to 'out' :", answer)
