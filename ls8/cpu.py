"""CPU functionality."""

import sys

HLT = 0b00000001
PRN = 0b01000111
LDI = 0b10000010
MUL = 0b10100010
PSH = 0b01000101
POP = 0b01000110


class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256
        self.pc = 0
        self.reg = [0] * 8
        self.branchtable = {HLT: self.op_hlt,
                            PRN: self.op_prn,
                            LDI: self.op_ldi,
                            MUL: self.op_mul,
                            PSH: self.op_push,
                            POP: self.op_pop
                            }
        self.running = True
        self.sp = -1

    def load(self, file):
        """Load a program into memory."""
        address = 0
        with open(file) as f:
            for instruction in f:
                li = instruction.strip().split('#')
                line = li[0].strip()
                if line == '':
                    continue
                else:
                    instruction = int(line, 2)
                    self.ram[address] = instruction
                    address += 1

        program = []

        # For now, we've just hardcoded a program:

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

    def ram_read(self, address):
        value = self.ram[address]
        return value

    def ram_write(self, address, value):
        self.ram[address] = value

    def op_prn(self, operand_a, operand_b):
        value = self.reg[operand_a]
        print(value, "From op prn")
        self.pc += 2
        return value

    def op_mul(self, operand_a, operand_b):
        value = self.reg[operand_a] * self.reg[operand_b]
        self.pc += 3
        print(value)
        return value

    def op_ldi(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        self.pc += 3

    def op_hlt(self, operand_a, operand_b):
        print('Stopping')
        self.running = False

    def op_push(self, operand_a, operand_b):
        self.sp -= 1
        self.ram[self.sp] = self.reg[operand_a]
        self.pc += 2

    def op_pop(self, operand_a, operand_b):
        value = self.ram[self.sp]
        self.sp += 1
        self.reg[operand_a] = value
        self.pc += 2

    def run(self):
        """Run the CPU."""
        while self.running:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if int(bin(IR), 2) in self.branchtable:
                self.branchtable[IR](operand_a, operand_b)
            else:
                print("Not valid")
                # print(self.ram)
                self.running = False
