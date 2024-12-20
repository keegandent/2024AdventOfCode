# Copyright (c) 2024 Keegan Dent
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import heapq
import re
import sys

global towels


def is_possible(pattern: str):
    if not len(pattern):
        return True
    for size, towel in towels:
        possible = False
        if re.match(towel, pattern) is not None:
            possible = is_possible(pattern[size:])
        if possible:
            break
    return possible


def main():
    global towels
    towels = []
    num_possible = 0
    for line in sys.stdin:
        if "," in line:
            [
                heapq.heappush(towels, (len(towel), towel))
                for towel in re.findall(r"\w+", line)
            ]
        elif line.rstrip():
            num_possible += is_possible(line.rstrip())
    print(num_possible)


if __name__ == "__main__":
    main()
