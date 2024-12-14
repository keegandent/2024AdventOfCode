# Copyright (c) 2024 Keegan Dent
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import re
import sys
from functools import cache

import numpy as np

GRID_SHAPE = np.array([101, 103])
BLOB_THRESHOLD = 4**2

global grid
grid = np.ndarray(GRID_SHAPE, dtype=int)


@cache
def offsets():
    global grid
    return np.vstack([dir * np.eye(grid.ndim, dtype=int) for dir in [-1, 1]])


@cache
def is_offgrid(position: tuple) -> bool:
    global grid
    return any(
        [
            (position[dim] < 0) or (position[dim] >= grid.shape[dim])
            for dim in range(grid.ndim)
        ]
    )


def largest_blob() -> int:
    dots = np.array(np.where(grid > 0))
    regions_lu = {}
    num_regions = 0

    for dot in dots.T:
        candidate_regions = set()
        for offset in offsets():
            position = dot + offset
            if (not is_offgrid(tuple(position))) and grid[tuple(position)] > 0:
                try:
                    candidate_regions.add(regions_lu[tuple(position)])
                except KeyError:
                    pass
        if not candidate_regions:
            candidate_regions.add(num_regions)
            num_regions += 1
        elif len(candidate_regions) > 1:
            new_region = min(candidate_regions)
            for k, v in regions_lu.items():
                if v in candidate_regions:
                    regions_lu[k] = new_region
            candidate_regions = set([new_region])
            # we do NOT update num_regions because we don't want to manage indices
            # empty regions will be pruned at the end
        regions_lu[tuple(dot)] = candidate_regions.pop()

    regions = [0] * num_regions
    for v in regions_lu.values():
        regions[v] += 1
    return max(regions)


def main():
    pos = []
    vel = []
    for line in sys.stdin:
        m = re.match(r"^p=(\d+),(\d+)\s*v=(-?\d+),(-?\d+)$", line)
        pos.append([int(m.group(1)), int(m.group(2))])
        vel.append([int(m.group(3)), int(m.group(4))])
    count = 0
    while True:
        grid[...] = 0
        print(f"Count: {count:>6}")
        for p, v in zip(pos, vel, strict=True):
            p = (count * np.array(v) + np.array(p)) % GRID_SHAPE
            grid[tuple(p)] += 1
        blob = largest_blob()
        print(f"Largest blob: {blob:>4}")
        if blob > BLOB_THRESHOLD:

            for row in grid:
                print("".join(["#" if p else "." for p in row]))
        print("", flush=True)
        count += 1


if __name__ == "__main__":
    main()
