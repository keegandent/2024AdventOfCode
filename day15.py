# Copyright (c) 2024 Keegan Dent
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import io
import sys
from functools import cache

import numpy as np

global grid


MOVE_MAP = {
    "^": np.array([-1, 0], dtype=int),
    "<": np.array([0, -1], dtype=int),
    "v": np.array([1, 0], dtype=int),
    ">": np.array([0, 1], dtype=int),
}


@cache
def is_offgrid(position: tuple) -> bool:
    global grid
    return any(
        [
            (position[dim] < 0) or (position[dim] >= grid.shape[dim])
            for dim in range(grid.ndim)
        ]
    )


def attempt_move(pos, move, replace="."):
    moved = True
    if grid[tuple(pos + move)] == "#":
        moved = False
    elif grid[tuple(pos + move)] == "O":
        moved = np.any(attempt_move(pos + move, move, "O") != pos + move)

    if moved:
        grid[tuple(pos + move)] = grid[tuple(pos)]
        grid[tuple(pos)] = replace
        return pos + move
    return pos


def main():
    global grid
    grid_lines = []
    move_lines = []
    for line in sys.stdin:
        if line[0] == "#":
            grid_lines.append(line)
        elif line[0] in ["v", "<", ">", "^"]:
            move_lines.append(line.rstrip())

    f = io.StringIO(
        "\n".join([",".join([char for char in line.rstrip()]) for line in grid_lines])
    )
    grid = np.loadtxt(f, dtype="U1", comments=None, delimiter=",")
    moves = np.array([MOVE_MAP[m] for move in move_lines for m in move])
    pos = np.array(np.where(grid == "@"), dtype=int).T[0]
    grid[tuple(pos)] = "."
    for move in moves:
        pos = attempt_move(pos, move)

    boxes = np.array(np.where(grid == "O"), dtype=int).T
    print(np.sum(np.array([100, 1]) * boxes))


if __name__ == "__main__":
    main()
