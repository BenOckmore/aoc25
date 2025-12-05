import sys
from pprint import pprint
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
    inputs = {k: v.decode('ascii').rstrip('\n') for k, v in raw_inputs.items()}
    pprint(inputs)

    return 0


if __name__ == "__main__":
    sys.exit(main())
