import sys
from pathlib import Path
import numpy as np
from shapely import Polygon


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

    nodes = [[int(y) for y in x.split(",")] for x in my_input]
    diffs = np.array(
        list(
            {
                tuple(min(y[0], y[1]) + max(y[0], y[1]) + [0])
                for x in nodes
                for y in zip([x] * len(nodes), nodes)
                if y[0] != y[1]
            }
        )
    ).transpose()

    diffs[4] = (np.abs(diffs[2] - diffs[0]) + 1) * (np.abs(diffs[3] - diffs[1]) + 1)

    print(np.max(diffs[4]))

    return 0


def main() -> int:
    raw_inputs = read_inputs()
    inputs = {k: v.decode("ascii").rstrip("\n") for k, v in raw_inputs.items()}

    my_input = inputs["puzzle.txt"].splitlines()

    nodes = [[int(y) for y in x.split(",")] for x in my_input]
    polygon = Polygon(nodes)

    diffs = np.array(
        list(
            {
                tuple(min(y[0], y[1]) + max(y[0], y[1]) + [0, 0])
                for x in nodes
                for y in zip([x] * len(nodes), nodes)
                if y[0] != y[1]
            }
        )
    ).transpose()

    diffs[4] = (np.abs(diffs[2] - diffs[0]) + 1) * (np.abs(diffs[3] - diffs[1]) + 1)

    def in_polygon(p: Polygon, a: tuple[int, int], b: tuple[int, int]) -> int:
        rect = Polygon([a, (a[0], b[1]), b, (b[0], a[1])])
        return p.covers(rect)

    diffs_T = diffs.transpose()
    valids = [in_polygon(polygon, row[0:2], row[2:4]) for row in diffs_T]
    diffs[5] = valids

    diffs_T = diffs_T[diffs[5] == 1]

    sorted_diffs = diffs_T[diffs_T.transpose()[4].argsort()]
    print(sorted_diffs[sorted_diffs[:, 5] == 1][-1][4])

    return 0


if __name__ == "__main__":
    part1()
    sys.exit(main())

# Started: Tue Dec  9 08:20:38 GMT 2025
# Part 1: Tue Dec  9 08:25:33 GMT 2025
# Part 2: Tue Dec  9 09:20:39 GMT 2025
