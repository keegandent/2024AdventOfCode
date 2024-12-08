# Copyright (c) 2024 Keegan Dent
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import io
import sys
from itertools import permutations

import numpy as np
import tqdm

RIGHT = np.array([[0, 1], [-1, 0]], dtype=int)


def is_offgrid(grid, position) -> bool:
    return any(
        [
            (position[dim][0] < 0) or (position[dim][0] >= grid.shape[dim])
            for dim in range(grid.ndim)
        ]
    )


def find_antinodes_freq(grid, freq):
    antinodes = set()
    nodes = np.array(np.where(grid == freq))
    if len(nodes.T) < 2:
        return antinodes
    for n1, n2 in permutations(nodes.T, r=2):
        antinode = 2 * n2 - n1
        if not is_offgrid(grid, antinode[:, np.newaxis]):
            antinodes.add(tuple(antinode))
    return antinodes


def main():
    lines = sys.stdin.readlines()
    f = io.StringIO(
        "\n".join([",".join([char for char in line.rstrip()]) for line in lines])
    )
    grid = np.loadtxt(f, dtype="U1", comments=None, delimiter=",")
    freqs = set(grid.ravel().tolist()) - set(".")

    antinodes = set()
    for freq in freqs:
        antinodes |= find_antinodes_freq(grid, freq)

    print(len(antinodes))


if __name__ == "__main__":
    main()
