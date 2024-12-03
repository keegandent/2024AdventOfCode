# Copyright (c) 2024 Keegan Dent
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys

import numpy as np
from numpy.typing import ArrayLike

ABS_DIFF_MAX = 3
ABS_DIFF_MIN = 1
NUM_SKIPS = 1


def check(arr: ArrayLike, skips_left: int = NUM_SKIPS, dir=0) -> bool:
    if skips_left < 0:
        return False
    diff = np.diff(arr)
    dir = dir if dir != 0 else np.sign(diff[0])
    for i, d in enumerate(diff):
        d_abs = np.abs(d)
        if np.sign(d) != dir or d_abs > ABS_DIFF_MAX or d_abs < ABS_DIFF_MIN:
            return check(
                np.concatenate((arr[:i], arr[i + 1 :])), skips_left - 1, dir
            ) or check(
                np.concatenate((arr[: i + 1], arr[i + 2 :])), skips_left - 1, dir
            )
    return True


def main():
    count = 0
    for line in sys.stdin:
        line = line.rstrip()
        arr = np.fromstring(line, dtype=int, sep=" ")
        # count += check(arr)
        # brute force check
        bfc = check(arr, 0)
        if bfc:
            count += 1
        else:
            for i in range(arr.size):
                if check(np.concatenate((arr[:i], arr[i + 1 :])), 0):
                    count += 1
                    break
    print(count)


if __name__ == "__main__":
    main()
