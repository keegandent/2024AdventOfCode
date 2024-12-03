# Copyright (c) 2024 Keegan Dent
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import re
import sys


def main():
    left = {}
    right = {}
    for line in sys.stdin:
        line = line.rstrip()
        m = re.search(r"(\d+)\s+(\d+)", line)
        l = int(m.group(1))
        r = int(m.group(2))
        if l in left:
            left[l] += 1
        else:
            left[l] = 1
        if r in right:
            right[r] += 1
        else:
            right[r] = 1
    print(sum([k * v * right[k] for k, v in left.items() if k in right]))


if __name__ == "__main__":
    main()
