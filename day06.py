# Copyright (c) 2024 Keegan Dent
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import io
import sys

import numpy as np

global grid

RIGHT = np.array([[0, 1], [-1, 0]], dtype=int)


def is_offgrid(position) -> bool:
    return any(
        [
            (position[dim][0] < 0) or (position[dim][0] > grid.shape[dim])
            for dim in range(grid.ndim)
        ]
    )


def main():
    global grid
    lines = sys.stdin.readlines()
    f = io.StringIO("".join([",".join([char for char in line]) for line in lines]))
    grid = np.loadtxt(f, dtype="U1", comments=None, delimiter=",")
    direction = np.array([[-1], [0]], dtype=int)
    position = np.array(np.where(grid == "^"), dtype=int)
    visited = set()
    while True:
        visited.add(tuple([int(pos[0]) for pos in position]))
        while True:
            new_position = position + direction
            if is_offgrid(new_position):
                print(len(visited))
                return
            if grid[tuple(new_position)] == ".":
                break
            direction = RIGHT @ direction
            new_position = position + direction
        position = new_position


if __name__ == "__main__":
    main()
