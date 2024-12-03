# Copyright (c) 2024 Keegan Dent
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import re
import sys


def main():
    cols = [[], []]
    for line in sys.stdin:
        line = line.rstrip()
        m = re.search(r"(\d+)\s+(\d+)", line)
        cols[0].append(int(m.group(1)))
        cols[1].append(int(m.group(2)))
    cols[0].sort()
    cols[1].sort()
    print(sum([abs(a - b) for a, b in zip(cols[0], cols[1])]))


if __name__ == "__main__":
    main()
