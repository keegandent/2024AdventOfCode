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


@cache
def offsets():
    global grid
    return np.vstack([dir * np.eye(grid.ndim, dtype=int) for dir in [-1, 1]])


def is_offgrid(position) -> bool:
    global grid
    return any(
        [
            (position[dim] < 0) or (position[dim] >= grid.shape[dim])
            for dim in range(grid.ndim)
        ]
    )


def calculate_region_cost(region_type: str) -> int:
    plots = np.array(np.where(grid == region_type))
    regions_lu = {}
    sides_lu = {}
    num_regions = 0
    for plot in plots.T:
        # only houses keys for border directions, val is whether "original"
        sides = dict()
        for offset in offsets():
            position = plot + offset
            if is_offgrid(position) or grid[tuple(position)] != region_type:
                sides[tuple(offset)] = 1

        candidate_regions = set()
        # determine side uniqueness
        # doing region candidacy here to prevent branching in prev loop
        for offset in offsets():
            position = plot + offset
            if (not is_offgrid(position)) and grid[tuple(position)] == region_type:
                try:
                    candidate_regions.add(regions_lu[tuple(position)])
                    for side in sides_lu[tuple(position)]:
                        if side in sides.keys():
                            # not original plot for side
                            sides[side] = 0
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
        regions_lu[tuple(plot)] = candidate_regions.pop()
        sides_lu[tuple(plot)] = sides

    # invert the regions lookup table
    regions = {}
    for k, v in regions_lu.items():
        if v not in regions:
            regions[v] = []
        regions[v].append(k)

    cost = 0
    for region in regions.values():
        area = len(region)
        sides = sum([sum(sides_lu[p].values()) for p in region])
        cost += area * sides
    return cost


def main():
    global grid
    lines = sys.stdin.readlines()
    f = io.StringIO(
        "\n".join([",".join([char for char in line.rstrip()]) for line in lines])
    )
    grid = np.loadtxt(f, dtype="U1", comments=None, delimiter=",")
    region_types = set(grid.ravel())
    price = 0
    for region_type in region_types:
        price += calculate_region_cost(region_type)
    print(price)


if __name__ == "__main__":
    main()
