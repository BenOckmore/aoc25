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
    inputs = {k: x.decode("ascii").split("\n") for k, x in raw_inputs.items()}

    total_joltage = 0
    for x in inputs["puzzle.txt"]:
        if not x.strip():
            continue
        # TODO: convert input and test vals to ints - faster compare?
        a = "0"
        b = "0"
        for digit in x[:-1]:
            if digit > a:
                a = digit
                b = "0"
            elif digit > b:
                b = digit

        if x[-1] > b:
            b = x[-1]

        bank_joltage = int(a + b)
        total_joltage += bank_joltage

    print(total_joltage)

    return 0


def main() -> int:
    raw_inputs = read_inputs()
    inputs = {k: x.decode("ascii").split("\n") for k, x in raw_inputs.items()}

    total_joltage = 0
    for x in inputs["puzzle.txt"]:
        if not x.strip():
            continue
        # TODO: convert input and test vals to ints - faster compare?
        activated = ["0"] * 12
        for digit in x[:-11]:
            for i in range(12):
                if digit > activated[i]:
                    activated[i] = digit
                    activated[i + 1 :] = ["0"] * (11 - i)
                    break

        for i, digit in enumerate(x[-11:], start=1):
            for j in range(i, 12):
                if digit > activated[j]:
                    activated[j] = digit
                    activated[j + 1 :] = ["0"] * (11 - j)
                    break

        bank_joltage = int("".join(activated))
        total_joltage += bank_joltage

    print(total_joltage)

    return 0


if __name__ == "__main__":
    sys.exit(main())
