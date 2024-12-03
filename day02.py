# Copyright (c) 2024 Keegan Dent
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys

import numpy as np

ABS_DIFF_MAX = 3
ABS_DIFF_MIN = 1



def main():
    count = 0
    for line in sys.stdin:
        line = line.rstrip()
        arr = np.fromstring(line, dtype=int, sep=" ")
        diff = np.diff(arr)
        if diff[0] == 0:
            continue
        diff_sign = np.sign(diff)
        if np.any(diff_sign != diff_sign[0]):
            continue
        diff_abs = np.abs(diff)
        if np.any(diff_abs > ABS_DIFF_MAX) or np.any(diff_abs < ABS_DIFF_MIN):
            continue
        count += 1
    print(count)


if __name__ == "__main__":
    main()
