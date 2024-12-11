# Copyright (c) 2024 Keegan Dent
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import re
import sys


def blink(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    elif len(str(stone)) % 2 == 0:
        stone_str = str(stone)
        return [
            int(stone_str[: len(stone_str) // 2]),
            int(stone_str[-len(stone_str) // 2 :]),
        ]
    else:
        return [stone * 2024]


def main():
    line = "".join([ln.rstrip() for ln in sys.stdin])
    stones = [int(m) for m in re.findall(r"\d+", line)]
    for _ in range(25):
        new_stones = []
        [new_stones.extend(blink(stone)) for stone in stones]
        stones = new_stones
    print(len(stones))


if __name__ == "__main__":
    main()
