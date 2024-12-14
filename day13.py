# Copyright (c) 2024 Keegan Dent
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import re
import sys
from collections import deque

import numpy as np

BUTTON_COSTS = np.array([3, 1])


def main():
    mat = []
    cost = 0
    for line in sys.stdin:
        if "Prize" in line:
            # assume in order
            m = deque(re.findall(r"\w=\+?(-?\d+)", line))
            [row.append(int(1e13) + int(m.popleft())) for row in mat]
            arr = np.array(mat, dtype=int)
            mat = []
            # wanted to do rref but this works ig
            soln = np.linalg.solve(
                arr[:, :-1],
                arr[:, -1:],
            ).ravel()
            if np.any(soln < 0):
                continue
            if np.any(np.abs(soln - soln.round()) > 1e-3):
                continue
            cost += int(round(sum(BUTTON_COSTS * soln)))

        elif "Button" in line:
            m = re.findall(r"\w\+(-?\d+)", line)
            if not mat:
                [mat.append([]) for _ in m]
            [mat[i].append(int(val)) for i, val in enumerate(m)]

    print(cost)


if __name__ == "__main__":
    main()
