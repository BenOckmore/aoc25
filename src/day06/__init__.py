from collections.abc import Generator
import math
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


def part1() -> int:
    raw_inputs = read_inputs()
    inputs = {k: v.decode("ascii").rstrip("\n") for k, v in raw_inputs.items()}

    my_input = inputs["puzzle.txt"].splitlines()
    nums = [[int(y) for y in x.strip().split()] for x in my_input[:-1]]
    op = [x for x in my_input[-1].strip().split()]

    nums_T = list(map(tuple, zip(*nums, strict=True)))
    total = sum(
        math.prod(expr[0]) if expr[1] == "*" else sum(expr[0])
        for expr in zip(nums_T, op)
    )

    print(total)

    return 0


def yield_results(puzzle_input: list[str]) -> Generator[int]:
    ops = iter(x for x in puzzle_input[-1].strip().split())
    op = next(ops)

    accum = 0 if op == "+" else 1
    break_tuple = (" ",) * (len(puzzle_input) - 1)
    nums = list(map(tuple, zip(*puzzle_input[:-1], strict=True)))
    for num in nums:
        if num == break_tuple:
            op = next(ops)
            yield accum
            accum = 0 if op == "+" else 1
        else:
            accum = (
                accum + int("".join(num)) if op == "+" else accum * int("".join(num))
            )

    yield accum


def main() -> int:
    raw_inputs = read_inputs()
    inputs = {k: v.decode("ascii").rstrip("\n") for k, v in raw_inputs.items()}

    my_input = inputs["puzzle.txt"].splitlines()

    print(sum(yield_results(my_input)))

    return 0


if __name__ == "__main__":
    part1()
    sys.exit(main())

# Started: Sat  6 Dec 09:30:01 GMT 2025
# Solved: Sat  6 Dec 10:27:36 GMT 2025
