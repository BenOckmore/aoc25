import re
import sys
from pathlib import Path


def read_inputs() -> dict[str, bytes]:
    inputs = Path(__file__).parent.glob("./*.txt")
    print(Path(__file__).parent)
    result = {}
    for in_file in inputs:
        with in_file.open("rb") as f_obj:
            result[in_file.name] = f_obj.read()

    return result


def main() -> int:
    raw_inputs = read_inputs()
    inputs = {k: v.decode("ascii").rstrip("\n") for k, v in raw_inputs.items()}

    my_input = inputs["puzzle.txt"].splitlines()

    shapes: dict[int, tuple[tuple[str, ...], ...]] = {}
    trees = []
    next_shape_id = None
    next_shape: list[list[str]] = []
    for line in my_input:
        line = line.strip()
        if not line:
            assert next_shape_id is not None and next_shape
            shapes[next_shape_id] = tuple(tuple(x) for x in next_shape)
            next_shape_id = None
        elif ma := re.match(r"(\d+):", line):
            next_shape_id = int(ma[1])
            next_shape = []
        elif ma := re.match(r"(\d+)x(\d+): (.+)", line):
            trees.append((int(ma[1]), int(ma[2]), tuple(int(x) for x in ma[3].split())))
        elif next_shape is not None:
            next_shape.append(list(line))

    occupied_counts = {k: sum(x.count("#") for x in v) for k, v in shapes.items()}

    # Upper bound - if there are more spaces occupied by present than spaces available,
    # the "tree" can't be solved. For a more robust solution, proceed to explore solution
    # space for each feasible tree by iterating over different packing solutions. One way of
    # doing this is by combining pairs of presents into single larger presents until only
    # one present remains (with a bunch of different resulting shapres in a number of parallel
    # solutions)
    solved = 0
    for tree in trees:
        available_space = tree[0] * tree[1]
        occupied_space = sum(
            occupied_counts[idx] * count for idx, count in enumerate(tree[2])
        )
        if occupied_space <= available_space:
            solved += 1

    print(solved)

    return 0


if __name__ == "__main__":
    sys.exit(main())


# Started: Fri 12 Dec 07:51:42 GMT 2025
# Solved: Fri 12 Dec 09:50:10 GMT 2025
# This was a bit unsatisfactory - I may come back to the packing-based solution rather than relying on upper bound at some point!
