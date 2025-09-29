#!/usr/bin/python

import subprocess
from pathlib import Path


def test_output_matches():
    here = Path(__file__).parent
    result = subprocess.run(["python", f"{here}/main.py"], stdout=subprocess.PIPE)  # noqa: S603, S607
    if result.stdout == b"Hello, world.\n":
        print("Tests passed")
    else:
        raise ValueError(result.stdout)


if __name__ == "__main__":
    test_output_matches()
