# Copyright (c) 2024 Keegan Dent
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import io
import sys
from concurrent.futures import ProcessPoolExecutor as executor
from concurrent.futures import as_completed

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


def check_path(
    grid,
    position,
    direction,
    new_obstructions=[],
):
    visited = set()
    while True:
        entry = tuple(
            [int(pos[0]) for pos in position] + [int(d[0]) for d in direction]
        )
        if entry in visited:
            return True
        visited.add(entry)
        while True:
            new_position = position + direction
            if is_offgrid(grid, new_position):
                return False
            new_position_tup = tuple([int(pos[0]) for pos in new_position])
            if (
                new_position_tup not in new_obstructions
                and grid[new_position_tup] != "#"
            ):
                break
            direction = RIGHT @ direction
            new_position = position + direction
        position = new_position


def main():
    lines = sys.stdin.readlines()
    f = io.StringIO("".join([",".join([char for char in line]) for line in lines]))
    grid = np.loadtxt(f, dtype="U1", comments=None, delimiter=",")
    direction = np.array([[-1], [0]], dtype=int)
    position = np.array(np.where(grid == "^"), dtype=int)
    s = 0

    with executor() as exe:
        fs = []
        for coord in np.ndindex(grid.shape):
            if grid[coord] != ".":
                continue
            fs.append(exe.submit(check_path, grid, position, direction, [coord]))
        for future in tqdm.tqdm(as_completed(fs), total=len(fs), unit="path"):
            s += future.result()
    print(s)


if __name__ == "__main__":
    main()
