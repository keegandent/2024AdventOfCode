# Copyright (c) 2024 Keegan Dent
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import io
import sys
from itertools import product

import numpy as np

global grid


def grid_find(pattern: str, center: tuple, dir: tuple = None) -> int:
    if any([c < 0 or c >= grid.shape[i] for i, c in enumerate(center)]):
        return 0
    if grid[center] != pattern[0]:
        return 0
    if len(pattern) == 1:
        return 1
    result = 0
    if dir:
        return grid_find(
            pattern[1:], tuple([c + o for c, o in zip(center, dir, strict=True)]), dir
        )
    for offset in product((-1, 1), repeat=grid.ndim):
        coord = tuple([c + o for c, o in zip(center, offset, strict=True)])
        result += grid_find(pattern[1:], coord, offset)
    return result


def main():
    global grid
    lines = sys.stdin.readlines()
    f = io.StringIO("".join([",".join([char for char in line]) for line in lines]))
    grid = np.loadtxt(f, dtype="U1", delimiter=",")
    count = 0
    for index, _ in np.ndenumerate(grid):
        if grid_find("AS", index) == 2 and grid_find("AM", index) == 2:
            lt_corner = grid[tuple([i - 1 for i in index])]
            rb_corner = grid[tuple([i + 1 for i in index])]
            if lt_corner != rb_corner:
                count += 1
    print(count)


if __name__ == "__main__":
    main()
