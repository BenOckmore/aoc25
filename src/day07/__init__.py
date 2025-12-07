import sys
from pathlib import Path
import networkx as nx


def read_inputs() -> dict[str, bytes]:
    inputs = Path(__file__).parent.glob("./*.txt")
    print(Path(__file__).parent)
    result = {}
    for in_file in inputs:
        with in_file.open("rb") as f_obj:
            result[in_file.name] = f_obj.read()

    return result


def part1() -> int:
    raw_inputs = read_inputs()
    inputs = {k: v.decode("ascii").rstrip("\n") for k, v in raw_inputs.items()}

    my_input = inputs["puzzle.txt"].splitlines()

    active_beams: set[int] = set()
    for idx, chr in enumerate(my_input[0]):
        if chr == "S":
            active_beams.add(idx)

    splits = 0
    for line in my_input[1:]:
        for idx, chr in enumerate(line):
            if chr == "^" and idx in active_beams:
                splits += 1
                active_beams.remove(idx)
                active_beams.update((idx - 1, idx + 1))

    print(splits)

    return 0


def main() -> int:
    raw_inputs = read_inputs()
    inputs = {k: v.decode("ascii").rstrip("\n") for k, v in raw_inputs.items()}

    my_input = inputs["puzzle.txt"].splitlines()

    graph: "nx.DiGraph[tuple[int, int]]" = nx.DiGraph()
    graph.add_nodes_from((0, idx) for idx, chr in enumerate(my_input[0]) if chr == "S")

    for row, line in enumerate(my_input[1:], start=1):
        for idx, chr in enumerate(line):
            if (row - 1, idx) in graph:
                if chr == "^":
                    graph.add_edge((row - 1, idx), (row, idx - 1))
                    graph.add_edge((row - 1, idx), (row, idx + 1))
                else:
                    graph.add_edge((row - 1, idx), (row, idx))

    active_nodes = [n for n in graph.nodes if n[0] == 0]
    sink_nodes = [n for n in graph.nodes if n[0] == row]

    for node in graph.nodes:
        graph.nodes[node]["paths"] = 0

    for node in active_nodes:
        graph.nodes[node]["paths"] = 1

    # bfs, but don't optimized by stopping at visited nodes
    while active_nodes:
        active_edges = {
            succ
            for active_node in active_nodes
            for succ in graph.out_edges(active_node)
        }
        active_nodes = []
        for in_node, out_node in active_edges:
            active_nodes.append(out_node)
            graph.nodes[out_node]["paths"] += graph.nodes[in_node]["paths"]

    print(sum(graph.nodes[n]["paths"] for n in sink_nodes))

    return 0


if __name__ == "__main__":
    part1()
    sys.exit(main())

# Started: Sun  7 Dec 08:35:57 GMT 2025
# Part 1 Solved: Sun  7 Dec 08:44:40 GMT 2025
# Part 2 Solved: Sun  7 Dec 09:19:39 GMT 2025
