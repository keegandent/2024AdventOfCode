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
global cost_grid
global seats

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


def calculate_costs(start_cost, start_pos, start_dir):
    global cost_grid
    cost_grid[tuple(start_pos)] = start_cost
    for offset in offsets():
        cost = start_cost + DOTP_COST_MAP[np.dot(start_dir, offset)]
        pos = start_pos + offset
        if grid[tuple(pos)] != "#" and cost_grid[tuple(pos)] >= cost:
            calculate_costs(cost, pos, offset)


def find_seats(end_cost, end_pos, end_dir=None):
    global cost_grid
    global seats
    seats.add(tuple(end_pos))
    end_dirs = [end_dir] if end_dir is not None else offsets()
    for end_dir in end_dirs:
        for offset in offsets():
            cost = end_cost - DOTP_COST_MAP[np.dot(end_dir, offset)]
            pos = end_pos + offset
            if grid[tuple(pos)] != "#" and cost_grid[tuple(pos)] <= cost:
                find_seats(cost, pos, offset)


def main():
    sys.setrecursionlimit(int(1e9))
    global grid
    global cost_grid
    global seats
    lines = sys.stdin.readlines()
    f = io.StringIO(
        "\n".join([",".join([char for char in line.rstrip()]) for line in lines])
    )
    grid = np.loadtxt(f, dtype="U1", comments=None, delimiter=",")
    cost_grid = np.full_like(grid, dtype=int, fill_value=(1 << 31) - 1)
    seats = set()
    start_pos = np.array(np.where(grid == "S"), dtype=int).T[0]
    start_dir = np.array([0, 1], dtype=int)
    end_pos = np.array(np.where(grid == "E"), dtype=int).T[0]
    calculate_costs(0, start_pos, start_dir)
    end_cost = cost_grid[tuple(end_pos)]
    find_seats(end_cost, end_pos)
    print(len(seats))


if __name__ == "__main__":
    main()
