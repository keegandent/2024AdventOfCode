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


def search_regions(regions: list[dict], position) -> int:
    for i, d in enumerate(regions):
        if tuple(position) in d.keys():
            return i
    return -1


def calculate_region_cost(region_type: str) -> int:
    plots = np.array(np.where(grid == region_type))
    regions = []
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
                dict_id = search_regions(regions, position)
                if dict_id != -1:
                    candidate_regions.add(dict_id)
                    for side in regions[dict_id][tuple(position)]:
                        if side in sides.keys():
                            # not original plot for side
                            sides[side] = 0

        if not candidate_regions:
            regions.append({tuple(plot): sides})
        else:
            if len(candidate_regions) > 1:
                new_dict = {}
                old_dirs = [regions[i] for i in candidate_regions]
                for od in old_dirs:
                    new_dict.update(od)
                    regions.remove(od)
                regions.append(new_dict)
                candidate_regions = set([len(regions) - 1])
            regions[candidate_regions.pop()][tuple(plot)] = sides

    cost = 0
    for region in regions:
        area = len(region)
        sides = sum([sum(s.values()) for s in region.values()])
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
