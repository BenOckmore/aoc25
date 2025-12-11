from typing import cast
import networkx as nx
import sys
from pathlib import Path


def read_inputs() -> dict[str, bytes]:
    inputs = Path(__file__).parent.glob("./*.txt")
    result = {}
    for in_file in inputs:
        with in_file.open("rb") as f_obj:
            result[in_file.name] = f_obj.read()

    return result


def part1() -> int:
    raw_inputs = read_inputs()
    inputs = {k: v.decode("ascii").rstrip("\n") for k, v in raw_inputs.items()}

    my_input = inputs["puzzle.txt"].splitlines()
    G: "nx.DiGraph[str]" = nx.DiGraph()
    for row in my_input:
        src, dsts_str = row.split(":")
        for dst in dsts_str.split():
            G.add_edge(src.strip(), dst.strip())

    if nx.has_path(G, "you", "out"):
        print(len(list(nx.all_simple_paths(G, "you", "out"))))

    return 0


def main() -> int:
    raw_inputs = read_inputs()
    inputs = {k: v.decode("ascii").rstrip("\n") for k, v in raw_inputs.items()}

    my_input = inputs["puzzle.txt"].splitlines()
    G: "nx.DiGraph[str]" = nx.DiGraph()
    for row in my_input:
        src, dsts_str = row.split(":")
        for dst in dsts_str.split():
            G.add_edge(src.strip(), dst.strip())

    G = cast(
        "nx.DiGraph[str]",
        G.subgraph(
            (nx.ancestors(G, "fft") | nx.descendants(G, "fft") | {"fft"})
            & (nx.ancestors(G, "dac") | nx.descendants(G, "dac") | {"dac"})
        ),
    )

    G.nodes["svr"]["paths"] = 1
    gen = nx.topological_sort(G)
    next(gen)  # first node will be svr, which  already has paths=1
    for node in gen:
        G.nodes[node]["paths"] = sum(G.nodes[x]["paths"] for x in G.predecessors(node))

    print(G.nodes["out"]["paths"])

    return 0


if __name__ == "__main__":
    part1()
    sys.exit(main())

# Started: Thu 11 Dec 07:53:09 GMT 2025
# Part 1: Thu 11 Dec 07:57:05 GMT 2025
# Part 2: Thu 11 Dec 09:06:19 GMT 2025
