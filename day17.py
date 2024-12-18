# Copyright (c) 2024 Keegan Dent
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import re
import sys


class Processor:
    def _combo_operand(self, operand) -> int:
        if operand in range(0, 4):
            return operand
        elif operand in range(4, 7):
            return self._registers[operand - 4]
        else:
            raise RuntimeError("Invalid program!")

    def _adv(self, operand):
        self._registers[0] = self._registers[0] // (1 << self._combo_operand(operand))
        self._instr_ptr += 2

    def _bxl(self, operand):
        self._registers[1] = self._registers[1] ^ operand
        self._instr_ptr += 2

    def _bst(self, operand):
        self._registers[1] = 7 & self._combo_operand(operand)
        self._instr_ptr += 2

    def _jnz(self, operand):
        if not self._registers[0]:
            self._instr_ptr += 2
            return
        self._instr_ptr = operand

    def _bxc(self, _):
        self._registers[1] = self._registers[1] ^ self._registers[2]
        self._instr_ptr += 2

    def _out(self, operand) -> int:
        self._instr_ptr += 2
        return 7 & self._combo_operand(operand)

    def _bdv(self, operand):
        self._registers[1] = self._registers[0] // (1 << self._combo_operand(operand))
        self._instr_ptr += 2

    def _cdv(self, operand):
        self._registers[2] = self._registers[0] // (1 << self._combo_operand(operand))
        self._instr_ptr += 2

    _INSTR_MAP = [_adv, _bxl, _bst, _jnz, _bxc, _out, _bdv, _cdv]

    def __init__(self, registers: list[int], program: list[int]):
        self._registers = registers
        self._program = program
        self._instr_ptr = 0

    def run(self, num_outs: int = None):
        while True:
            if self._instr_ptr >= len(self._program) or (
                num_outs is not None and num_outs == 0
            ):
                return
            fn = self._INSTR_MAP[self._program[self._instr_ptr]]
            out = fn(self, self._program[self._instr_ptr + 1])
            if out is not None:
                yield out
                if num_outs is not None:
                    num_outs -= 1


def main():
    registers = []
    for line in sys.stdin:
        if "Register" in line:
            m = re.search(r"\d+", line)
            registers.append(int(m.group()))
        elif "Program" in line:
            m = re.findall(r"\d+", line)
            program = [int(p) for p in m]
    rega = 0
    for o in range(len(program)):
        rega = rega << 3
        while True:
            print(f"\rOutput: {o:>2} \tRegister A: {rega}", end="", file=sys.stderr)
            proc = Processor([rega, registers[1], registers[2]], program)
            out = list(proc.run(o + 1))
            if len(out) == o + 1 and out == program[-(o + 1) :]:
                break
            rega += 1
    print("", file=sys.stderr)
    print(rega)


if __name__ == "__main__":
    main()
