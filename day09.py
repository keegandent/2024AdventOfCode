# Copyright (c) 2024 Keegan Dent
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys


def main():
    inp = "".join([line.rstrip() for line in sys.stdin])
    disk_map = {None: []}
    file_idx = 0
    # parse
    for i, char in enumerate(inp):
        file_id = i // 2 if i % 2 == 0 else None
        space = int(char)
        if file_id not in disk_map:
            disk_map[file_id] = []
        disk_map[file_id].append((file_idx, space))
        file_idx += space
    num_files = file_id + 1
    # compress
    for file_id in reversed(range(num_files)):
        # real file ids have only one entry
        orig_idx, space = disk_map[file_id][0]
        for free_id, tup in enumerate(disk_map[None]):
            file_idx, free_space = tup
            if file_idx > orig_idx:
                break
            if free_space >= space:
                disk_map[file_id][0] = (file_idx, space)
                disk_map[None][free_id] = (file_idx + space, free_space - space)
                if free_space == space:
                    disk_map[None].pop(free_id)
                disk_map[None].append((orig_idx, space))
                break
    # checksum
    s = 0
    for file_id in range(num_files):
        file_idx, space = disk_map[file_id][0]
        s += sum([file_id * (file_idx + sub_idx) for sub_idx in range(space)])
    print(s)


if __name__ == "__main__":
    main()
