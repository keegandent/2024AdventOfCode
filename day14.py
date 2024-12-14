# Copyright (c) 2024 Keegan Dent
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import re
import sys
from math import prod

import numpy as np

GRID_SHAPE = np.array([101, 103])
NUM_MOVES = 100


def main():
    quads = [0, 0, 0, 0]
    for line in sys.stdin:
        m = re.match(r"^p=(\d+),(\d+)\s*v=(-?\d+),(-?\d+)$", line)
        pos = np.array([int(m.group(1)), int(m.group(2))])
        vel = np.array([int(m.group(3)), int(m.group(4))])
        pos = (pos + NUM_MOVES * vel) % GRID_SHAPE
        quad = [None, None]
        if pos[0] < GRID_SHAPE[0] // 2:
            quad[0] = 0
        elif pos[0] >= GRID_SHAPE[0] - GRID_SHAPE[0] // 2:
            quad[0] = 1
        if pos[1] < GRID_SHAPE[1] // 2:
            quad[1] = 0
        elif pos[1] >= GRID_SHAPE[1] - GRID_SHAPE[1] // 2:
            quad[1] = 2
        if None in quad:
            continue
        quads[sum(quad)] += 1
    print(prod(quads))


if __name__ == "__main__":
    main()
