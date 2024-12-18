# Copyright (c) 2024 Keegan Dent
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import heapq
import re
import sys
from collections import deque
from functools import cache

import numpy as np

global grid
global cost_grid


NUM_OBSTACLES = 1024


@cache
def is_offgrid(position: tuple) -> bool:
    global grid
    return any(
        [
            (position[dim] < 0) or (position[dim] >= grid.shape[dim])
            for dim in range(grid.ndim)
        ]
    )


@cache
def offsets():
    global grid
    return np.vstack([dir * np.eye(grid.ndim, dtype=int) for dir in [-1, 1]])


def calculate_costs(start_cost, start_pos):
    global cost_grid
    cost_grid[tuple(start_pos)] = start_cost
    heap = [(start_cost, *[int(p) for p in start_pos])]
    while heap:
        h = heapq.heappop(heap)
        current_cost = h[0]
        current_pos = np.array(h[1:])
        for offset in offsets():
            cost = current_cost + 1
            pos = current_pos + offset
            if (
                not is_offgrid(tuple(pos))
                and grid[tuple(pos)] != "#"
                and cost_grid[tuple(pos)] >= cost
            ):
                cost_grid[tuple(pos)] = cost
                heapq.heappush(heap, (cost, *[int(p) for p in pos]))


def main():
    global grid
    global cost_grid
    grid = np.full((71, 71), dtype="U1", fill_value=".")
    blocks = deque([])
    for line in sys.stdin:
        m = re.findall(r"\d+", line)
        block = tuple([int(coord) for coord in m])
        grid[block] = "#"
        blocks.append(block)
    cost_grid = np.full_like(grid, dtype=int, fill_value=(1 << 31) - 1)
    start_pos = np.array([0, 0])
    end_pos = np.array([dim - 1 for dim in grid.shape])
    while cost_grid[tuple(end_pos)] == (1 << 31) - 1:
        block = blocks.pop()
        grid[block] = "."
        calculate_costs(0, start_pos)
    print(",".join([str(b) for b in block]))


if __name__ == "__main__":
    main()
