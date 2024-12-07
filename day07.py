# Copyright (c) 2024 Keegan Dent
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import operator
import re
import sys
from itertools import product

import tqdm


def intcat(a: int, b: int) -> int:
    return int(f"{a:d}{b:d}")


OPSET = [operator.add, operator.mul, intcat]


def check_feasibility(result: int, operands: list[int]) -> bool:
    for ops in product(OPSET, repeat=len(operands) - 1):
        test_result = operands[0]
        for op, operand in zip(ops, operands[1:], strict=True):
            if test_result > result:
                break
            test_result = op(test_result, operand)
        if test_result == result:
            return True
    return False


def main():
    output = 0
    for line in tqdm.tqdm(sys.stdin.readlines()):
        m = re.match(r"^(\d+):\s*(.*?)$", line)
        result = int(m.group(1))
        line = m.group(2)
        operands = [int(m) for m in re.findall(r"\d+", line)]
        if check_feasibility(result, operands):
            output += result
    print(output)


if __name__ == "__main__":
    main()
