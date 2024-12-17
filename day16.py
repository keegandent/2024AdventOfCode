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
global cost_map

TURN_COST = 1000
MOVE_COST = 1
DOTP_COST_MAP = {
    1: MOVE_COST,  # straight
    0: TURN_COST + MOVE_COST,  # (counter-)clockwise
    -1: 2 * TURN_COST + MOVE_COST,  # about-face
}
RIGHT = np.array([[0, 1], [-1, 0]], dtype=int)
LEFT = -RIGHT


@cache
def offsets():
    global grid
    return np.vstack([dir * np.eye(grid.ndim, dtype=int) for dir in [-1, 1]])


def calculate_costs(start_pos, start_dir, start_cost):
    global cost_map
    for offset in offsets():
        cost = start_cost + DOTP_COST_MAP[np.dot(start_dir, offset)]
        pos = start_pos + offset
        if grid[tuple(pos)] != "#" and (
            tuple(pos) not in cost_map.keys() or cost_map[tuple(pos)] > cost
        ):
            cost_map[tuple(pos)] = cost
            calculate_costs(pos, offset, cost)


def main():
    sys.setrecursionlimit(int(1e9))
    global grid
    global cost_map
    lines = sys.stdin.readlines()
    f = io.StringIO(
        "\n".join([",".join([char for char in line.rstrip()]) for line in lines])
    )
    grid = np.loadtxt(f, dtype="U1", comments=None, delimiter=",")
    cost_map = {}
    start_pos = np.array(np.where(grid == "S"), dtype=int).T[0]
    start_dir = np.array([0, 1], dtype=int)
    calculate_costs(start_pos, start_dir, 0)
    print(cost_map[tuple(np.array(np.where(grid == "E"), dtype=int).T[0])])


if __name__ == "__main__":
    main()
