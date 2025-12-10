import math
import sys
from pathlib import Path
import numpy as np
from collections import Counter


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

    nodes = [[int(y) for y in x.split(",")] for x in my_input]
    edges = np.array(
        list(
            {
                tuple(min(y[0], y[1]) + max(y[0], y[1]) + [0])
                for x in nodes
                for y in zip([x] * len(nodes), nodes)
                if y[0] != y[1]
            }
        )
    ).transpose()

    edges[6] = (
        (edges[3] - edges[0]) * (edges[3] - edges[0])
        + (edges[4] - edges[1]) * (edges[4] - edges[1])
        + (edges[5] - edges[2]) * (edges[5] - edges[2])
    )

    sorted_edges = edges.transpose()[edges[6].argsort()]

    node_circuits: dict[tuple[int, int, int], int] = {}
    connections = 0
    for edge in sorted_edges:
        a = tuple(edge[:3].tolist())
        b = tuple(edge[3:6].tolist())

        connections += 1
        if a in node_circuits and b in node_circuits:
            if node_circuits[a] == node_circuits[b]:
                continue
            else:
                source = node_circuits[b]
                target = node_circuits[a]
                for k, v in node_circuits.items():
                    if v == source:
                        node_circuits[k] = target
        elif a in node_circuits:
            node_circuits[b] = node_circuits[a]
        elif b in node_circuits:
            node_circuits[a] = node_circuits[b]
        else:
            node_circuits[a] = node_circuits[b] = len(node_circuits)

        counts = Counter(node_circuits.values())

        if connections >= 1000:
            break

    print(math.prod(x[1] for x in counts.most_common(3)))

    return 0


def main() -> int:
    raw_inputs = read_inputs()
    inputs = {k: v.decode("ascii").rstrip("\n") for k, v in raw_inputs.items()}

    my_input = inputs["puzzle.txt"].splitlines()

    nodes = [[int(y) for y in x.split(",")] for x in my_input]
    edges = np.array(
        list(
            {
                tuple(min(y[0], y[1]) + max(y[0], y[1]) + [0])
                for x in nodes
                for y in zip([x] * len(nodes), nodes)
                if y[0] != y[1]
            }
        )
    ).transpose()

    edges[6] = (
        (edges[3] - edges[0]) * (edges[3] - edges[0])
        + (edges[4] - edges[1]) * (edges[4] - edges[1])
        + (edges[5] - edges[2]) * (edges[5] - edges[2])
    )

    sorted_edges = edges.transpose()[edges[6].argsort()]

    node_circuits: dict[tuple[int, int, int], int] = {}
    connections = 0
    for edge in sorted_edges:
        a = tuple(edge[:3].tolist())
        b = tuple(edge[3:6].tolist())

        connections += 1
        if a in node_circuits and b in node_circuits:
            if node_circuits[a] == node_circuits[b]:
                continue
            else:
                source = node_circuits[b]
                target = node_circuits[a]
                for k, v in node_circuits.items():
                    if v == source:
                        node_circuits[k] = target
        elif a in node_circuits:
            node_circuits[b] = node_circuits[a]
        elif b in node_circuits:
            node_circuits[a] = node_circuits[b]
        else:
            node_circuits[a] = node_circuits[b] = len(node_circuits)

        if len(set(node_circuits.values())) == 1 and len(node_circuits) == len(nodes):
            print(a, b, a[0] * b[0])
            break

    return 0


if __name__ == "__main__":
    part1()
    sys.exit(main())

# On train today, so will be a little slower!
# Started: Mon Dec  8 07:21:02 GMT 2025
# Part 1: Mon Dec  8 09:06:52 GMT 2025
# Part 2: Mon Dec  8 09:11:36 GMT 2025
# Would've been much faster if the puzzle had mentioned that skipping an extension counts as adding a connection!!!
