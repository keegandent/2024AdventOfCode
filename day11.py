# Copyright (c) 2024 Keegan Dent
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import re
import sys

import tqdm


def blink(stone: int) -> tuple[int]:
    stone_str = str(stone)
    if stone == 0:
        return (1,)
    elif len(stone_str) % 2 == 0:
        return (
            int(stone_str[: len(stone_str) // 2]),
            int(stone_str[-len(stone_str) // 2 :]),
        )
    else:
        return (int(stone) * 2024,)


def main():
    line = "".join([ln.rstrip() for ln in sys.stdin])
    stones = [int(m) for m in re.findall(r"\d+", line)]
    stone_counts = {}
    for stone in stones:
        if stone not in stone_counts.keys():
            stone_counts[stone] = 0
        stone_counts[stone] += 1
    for _ in tqdm.tqdm(range(75)):
        new_stone_counts = {}
        for stone, count in stone_counts.items():
            new_stones = blink(stone)
            for new_stone in new_stones:
                if new_stone not in new_stone_counts.keys():
                    new_stone_counts[new_stone] = 0
                new_stone_counts[new_stone] += count
        stone_counts = new_stone_counts
    print(sum(stone_counts.values()))


if __name__ == "__main__":
    main()
