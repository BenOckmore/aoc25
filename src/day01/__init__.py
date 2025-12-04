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


START = 50


def part1() -> int:
    raw_inputs = read_inputs()
    inputs = {k: v.decode("ascii") for k, v in raw_inputs.items()}

    sample_input = inputs["puzzle.txt"]
    sample_input_list = [
        int(x) for x in sample_input.replace("L", "-").replace("R", "").split("\n")
    ]

    tracker = START
    zero_counter = 0
    for i in sample_input_list:
        tracker += i
        if (tracker % 100) == 0:
            zero_counter += 1

    print(zero_counter)

    return 0


# slow, but accurate - used for testing
def sim_clicks(start: int, clicks: int, increment: int) -> tuple[int, int]:
    zero_counter = 0
    for i in range(clicks):
        start += increment
        if start % 100 == 0:
            zero_counter += 1

    return (start % 100), zero_counter


def main() -> int:
    raw_inputs = read_inputs()
    inputs = {k: v.decode("ascii") for k, v in raw_inputs.items()}

    sample_input = inputs["puzzle.txt"]
    sample_input_list = [
        int(x) for x in sample_input.replace("L", "-").replace("R", "").split("\n")
    ]

    tracker = START
    zero_counter = 0

    for i in sample_input_list:
        next_tracker = tracker + i

        zero_counter += abs(tracker // 100 - next_tracker // 100)

        next_tracker = next_tracker % 100
        if i < 0:
            if tracker == 0:
                zero_counter -= 1
            if next_tracker == 0:
                zero_counter += 1

        tracker = next_tracker

    print(zero_counter)

    return 0


if __name__ == "__main__":
    sys.exit(main())
