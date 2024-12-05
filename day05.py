# Copyright (c) 2024 Keegan Dent
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import re
import sys
from functools import cmp_to_key


def validate(updates: list[int], lo, hi) -> bool:
    try:
        lo_idx = updates.index(lo)
        hi_idx = updates.index(hi)
    except ValueError:
        return True
    return lo_idx < hi_idx


def main():
    checks = []
    for line in sys.stdin:
        m = re.match(r"(\d+)\|(\d+)", line)
        if not m:
            # end of ordering directions
            break
        lo = int(m.group(1))
        hi = int(m.group(2))

        checks.append((lo, hi))

    result = 0

    def compare(a: int, b: int) -> int:
        for check in checks:
            if not validate([a, b], *check):
                return 1
        return -1

    for line in sys.stdin:
        updates = [int(s) for s in re.findall(r"\d+", line)]
        passed = True
        for check in checks:
            if not validate(updates, *check):
                passed = False
                break
        if not passed:
            updates = sorted(updates, key=cmp_to_key(compare))
            result += updates[(len(updates) - 1) // 2]
    print(result)


if __name__ == "__main__":
    main()
