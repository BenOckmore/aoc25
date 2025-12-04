import functools
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


def factors(num: int) -> set[int]:
    return {i for i in range(1, num // 2 + 1) if num % i == 0}


@functools.cache
def invalid_id_set(num_len: int, part: int) -> set[str]:
    # get factors
    # divide num_len by factors to make fragment_len, and number fragment_length
    # long can be repeated by the factor to make an invalid id

    if part == 1 and num_len % 2 != 0:
        # in part 1, odd numbers can't have invalid ids, since they can't have a pattern repeated twice exactly
        return set()

    invalid_ids = set()
    factor_list = {num_len // 2}
    if part == 2:
        factor_list = factors(num_len)

    for factor in factor_list:
        num_repeats = num_len // factor

        invalid_ids |= {
            str(gen_num) * num_repeats
            for gen_num in range(int("1" + "0" * (factor - 1)), int("1" + "0" * factor))
        }

    return invalid_ids


def find_invalid_ids_in_range(inp_range: str, part: int) -> set[str]:
    a, b = inp_range.split("-")

    test_set = {str(x) for x in range(int(a), int(b) + 1)}
    sorted_test_set = sorted(test_set, key=lambda x: int(x))

    min_len = len(sorted_test_set[0])
    max_len = len(sorted_test_set[-1])

    # get all invalid ids
    invalid_ids = set.union(
        *[invalid_id_set(x, part) for x in range(min_len, max_len + 1)]
    )

    return test_set & invalid_ids


def main() -> int:
    inputs = read_inputs()

    PART = 2

    total = 0
    for inp_range in inputs["puzzle.txt"].decode("ascii").split(","):
        total += sum(int(x) for x in find_invalid_ids_in_range(inp_range, PART))

    print(total)

    return 0


if __name__ == "__main__":
    sys.exit(main())
