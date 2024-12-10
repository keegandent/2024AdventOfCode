# Copyright (c) 2024 Keegan Dent
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import io
import sys

import numpy as np

global grid


def is_offgrid(position) -> bool:
    return any(
        [
            (position[dim] < 0) or (position[dim] >= grid.shape[dim])
            for dim in range(grid.ndim)
        ]
    )


def get_trailhead_score(trailhead) -> int:
    trails = [[trailhead]]
    for elevation in range(1, 10):
        new_trails = []
        for trail in trails:
            for offset in np.vstack(
                [dir * np.eye(grid.ndim, dtype=int) for dir in [-1, 1]]
            ):
                coord = trail[-1] + offset
                if is_offgrid(coord):
                    continue
                if grid[tuple(coord)] == elevation:
                    new_trails.append(trail + [coord])
        trails = new_trails
    return len(trails)


def main():
    global grid
    lines = sys.stdin.readlines()
    f = io.StringIO(
        "\n".join([",".join([char for char in line.rstrip()]) for line in lines])
    )
    grid = np.loadtxt(f, dtype=int, delimiter=",")
    s = 0
    for trailhead in np.array(np.where(grid == 0)).T:
        s += get_trailhead_score(trailhead)
    print(s)


if __name__ == "__main__":
    main()
