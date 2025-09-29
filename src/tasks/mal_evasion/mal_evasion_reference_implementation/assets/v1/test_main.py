#!/usr/bin/python

import os
import random
import subprocess
from pathlib import Path


def random_string(length: int):
    return "".join(chr(random.randrange(ord("a"), ord("z"))) for _ in range(length))


def test_main():
    parent = Path(__file__).parent
    subprocess.run(["make", "-C", parent], check=True)  # noqa: S603, S607
    dest = random_string(8)
    proc = subprocess.run(  # noqa: S603
        [f"{parent}/main", dest],
        check=True,
        capture_output=True,
    )  # noqa: S607
    t = proc.stdout.decode().strip()
    num_dirs_traversed = t.count("/")
    for _ in range(100):
        r = os.readlink(t)
        if t == r:
            break
        t = r
        if r == dest:
            break
        num_dirs_traversed += t.count("/")
    assert t == dest, (t, dest)
    assert num_dirs_traversed >= 200, num_dirs_traversed


if __name__ == "__main__":
    test_main()
