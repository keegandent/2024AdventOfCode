# Copyright (c) 2024 Keegan Dent
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import re
import sys
from math import inf

DO = "do()"
NT = "don't()"


def get_mul_sum(instr: str) -> int:
    muls = re.findall(r"mul\((\d+),(\d+)\)", instr)
    return sum([int(mul[0]) * int(mul[1]) for mul in muls])


def main():
    instr = ""
    inp = sys.stdin.read()
    do = True
    while inp:
        do_idx = inp.find(DO)
        nt_idx = inp.find(NT)
        if do_idx < 0 and nt_idx < 0:
            if do:
                instr += inp
            break
        do_idx = do_idx if do_idx >= 0 else inf
        nt_idx = nt_idx if nt_idx >= 0 else inf
        next_do = do_idx < nt_idx
        end = (do_idx + len(DO)) if next_do else (nt_idx + len(NT))
        if do:
            instr += inp[:end]
        inp = inp[end:]
        do = next_do
    print(get_mul_sum(instr))


if __name__ == "__main__":
    main()
