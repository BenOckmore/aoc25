from collections.abc import Generator, Iterable
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

    split_input = inputs["puzzle.txt"].split("\n\n")
    fresh_ranges = sorted(
        (int(str_range[0]), int(str_range[1]))
        for x in split_input[0].split("\n")
        if len(str_range := x.split("-")) == 2
    )
    available_ingredients = [int(x) for x in split_input[1].split("\n")]

    count = 0
    for ingredient in available_ingredients:
        for fresh_range in fresh_ranges:
            if fresh_range[0] <= ingredient <= fresh_range[1]:
                count += 1
                break

    print(count)

    return 0


def main() -> int:
    raw_inputs = read_inputs()
    inputs = {k: v.decode("ascii").rstrip("\n") for k, v in raw_inputs.items()}

    split_input = inputs["puzzle.txt"].split("\n\n")
    fresh_ranges = sorted(
        (int(str_range[0]), int(str_range[1]))
        for x in split_input[0].split("\n")
        if len(str_range := x.split("-")) == 2
    )

    def simplify_ranges(
        in_ranges: Iterable[tuple[int, int]],
    ) -> Generator[tuple[int, int]]:
        last_yielded = None
        in_range_iter = iter(in_ranges)
        last_range = next(in_range_iter)
        for in_range in in_range_iter:
            if in_range[0] <= last_range[1]:
                if in_range[1] > last_range[1]:
                    # latest range is continuous with previous range, extend rather than add
                    last_range = (last_range[0], in_range[1])
            else:
                yield last_range
                last_range, last_yielded = in_range, last_range

        if last_range != last_yielded:
            yield last_range

    simple_ranges = list(simplify_ranges(fresh_ranges))

    all_fresh_count = sum(
        (fresh_range[1] - fresh_range[0]) for fresh_range in simple_ranges
    ) + len(simple_ranges)

    print(all_fresh_count)

    return 0


if __name__ == "__main__":
    sys.exit(main())
