import sys
from pathlib import Path
import numpy as np
from scipy.signal import convolve2d


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
    inputs = {k: x.decode("ascii") for k, x in raw_inputs.items()}

    rows = inputs["puzzle.txt"].split("\n")
    grid = [[y == "@" for y in x] for x in rows]

    arr = np.array(grid, dtype=int)
    window = np.ones((3, 3), dtype=int)
    window[1, 1] = 0

    y = convolve2d(arr, window, mode="same", boundary="fill", fillvalue=0)
    roll_counts = y[grid]

    print(np.count_nonzero(roll_counts < 4))

    return 0


def main() -> int:
    raw_inputs = read_inputs()
    inputs = {k: x.decode("ascii") for k, x in raw_inputs.items()}

    rows = inputs["puzzle.txt"].split("\n")
    grid = [[y == "@" for y in x] for x in rows]

    arr = np.array(grid, dtype=int)
    window = np.ones((3, 3), dtype=int)
    window[1, 1] = 0

    start_rolls_left = next_rolls_left = np.count_nonzero(arr)
    rolls_left = next_rolls_left + 1
    while next_rolls_left < rolls_left:
        rolls_left = next_rolls_left
        roll_counts = convolve2d(arr, window, mode="same", boundary="fill", fillvalue=0)
        arr[roll_counts < 4] = 0
        next_rolls_left = np.count_nonzero(arr)

    print(start_rolls_left - np.count_nonzero(arr))

    return 0


if __name__ == "__main__":
    sys.exit(main())
