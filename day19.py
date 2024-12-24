# Copyright (c) 2024 Keegan Dent
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import heapq
import re
import sys
from functools import cache

from tqdm import tqdm

global towels


@cache
def num_ways(pattern: str):
    if not len(pattern):
        return 1
    possible_sum = 0
    for size, towel in towels:
        possible = 0
        if re.match(towel, pattern) is not None:
            possible = num_ways(pattern[size:])
        possible_sum += possible
    return possible_sum


def main():
    global towels
    towels = []
    num_possible = 0
    for line in tqdm(sys.stdin.readlines()):
        if "," in line:
            [
                heapq.heappush(towels, (len(towel), towel))
                for towel in re.findall(r"\w+", line)
            ]
        elif line.rstrip():
            num_possible += num_ways(line.rstrip())
    print(num_possible)


if __name__ == "__main__":
    main()
