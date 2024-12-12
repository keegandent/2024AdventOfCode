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
    global grid
    return any(
        [
            (position[dim] < 0) or (position[dim] >= grid.shape[dim])
            for dim in range(grid.ndim)
        ]
    )


def search_regions(regions: list[dict], position) -> set:
    result = set()
    for i, d in enumerate(regions):
        if tuple(position) in d.keys():
            result.add(i)
    return result


def calculate_region_cost(region_type: str) -> int:
    type_spots = np.array(np.where(grid == region_type))
    regions = []
    for spot in type_spots.T:
        sides = dict()
        candidates = set()
        for offset in np.vstack(
            [dir * np.eye(grid.ndim, dtype=int) for dir in [-1, 1]]
        ):
            position = spot + offset
            if is_offgrid(position) or grid[tuple(position)] != region_type:
                sides[tuple(offset)] = 1

        for offset in np.vstack(
            [dir * np.eye(grid.ndim, dtype=int) for dir in [-1, 1]]
        ):
            position = spot + offset
            if (not is_offgrid(position)) and grid[tuple(position)] == region_type:
                dict_id = search_regions(regions, position)
                candidates |= dict_id
                if dict_id:
                    for side in regions[dict_id.pop()][tuple(position)]:
                        if side in sides.keys():
                            sides[side] = 0

        if not candidates:
            regions.append({tuple(spot): sides})
        else:
            if len(candidates) > 1:
                new_dict = {}
                old_dirs = [regions[i] for i in candidates]
                for od in old_dirs:
                    new_dict.update(od)
                    regions.remove(od)
                regions.append(new_dict)
                candidates = set([len(regions) - 1])
            regions[candidates.pop()][tuple(spot)] = sides

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
