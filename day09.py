# Copyright (c) 2024 Keegan Dent
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys


def main():
    inp = "".join([line.rstrip() for line in sys.stdin])
    disk = []
    # parse
    for i, char in enumerate(inp):
        file_id = i // 2 if i % 2 == 0 else None
        disk.extend([file_id] * int(char))
    # compress
    while True:
        try:
            new_idx = disk.index(None)
        except ValueError:
            break
        disk[new_idx] = disk.pop()
    # checksum
    print(sum([i * file_id for i, file_id in enumerate(disk)]))


if __name__ == "__main__":
    main()
