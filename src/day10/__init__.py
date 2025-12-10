import math
import sys
from pathlib import Path
import networkx as nx
import numpy as np
from scipy.optimize import linprog


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

    total = 0
    my_inputs = inputs["puzzle.txt"].splitlines()
    for machine in my_inputs:
        indicators, _, other = machine.partition(" ")
        buttons, _, _ = other.rpartition(" ")
        indicator_num = int(
            indicators[1:][:-1][::-1].replace("#", "1").replace(".", "0"), 2
        )

        indicator_max = int(math.pow(2, len(indicators) - 2))
        button_list = [x[1:][:-1] for x in buttons.split()]

        G: "nx.DiGraph[int]" = nx.DiGraph()
        G.add_nodes_from(range(indicator_max))

        for button in button_list:
            mask = 0
            for button_comp in button.split(","):
                mask |= 2 ** int(button_comp)

            for src_node in G.nodes:
                tgt_node = src_node ^ mask
                G.add_edge(src_node, tgt_node, button_set=button)

        total += len(nx.shortest_path(G, 0, indicator_num)) - 1

    print(total)

    return 0


def main() -> int:
    raw_inputs = read_inputs()
    inputs = {k: v.decode("ascii").rstrip("\n") for k, v in raw_inputs.items()}

    total = 0
    my_inputs = inputs["puzzle.txt"].splitlines()
    for machine in my_inputs:
        _, _, other = machine.partition(" ")
        buttons, _, joltage = other.rpartition(" ")

        joltage_vector = np.array([int(x) for x in joltage[1:][:-1].split(",")])
        button_list = [x[1:][:-1] for x in buttons.split()]

        button_matrix = np.zeros((joltage_vector.shape[0], len(button_list)))
        for col, button in enumerate(button_list):
            for button_comp in button.split(","):
                button_matrix[int(button_comp)][col] = 1

        c = np.ones(len(button_list))

        res = linprog(c, A_eq=button_matrix, b_eq=joltage_vector, integrality=1)

        if res.fun is None:
            raise RuntimeError("Couldn't solve the puzzle!")
        else:
            total += int(round(res.fun))

    print(total)

    return 0


if __name__ == "__main__":
    part1()
    sys.exit(main())

# Started: Wed 10 Dec 08:37:17 GMT 2025
# Part 1: Wed 10 Dec 09:08:06 GMT 2025
# Part 2: Wed 10 Dec 12:23:39 GMT 2025 (with 15 minute break in middle)
