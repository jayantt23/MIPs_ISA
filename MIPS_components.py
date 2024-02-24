class Memory:
    """Class for MIPS  memory with read and write"""

    def __init__(self):
        self.memory = {}

    def read(self, address):
        if address in self.memory:
            return self.memory[address]
        else:
            return None

    def write(self, address, value):
        if address in self.memory:
            self.memory[address] = value
        return


class Register_file:
    """Class for MIPS register file with two dictionaries containing the registers being mapped to their respective 5 bit values and their names, with class methods to read, write and get the name of the register ( for simulation purposes)"""

    def __init__(self):
        # all registers initialized with zero other than stack pointer
        self.registers = {
            "00000": 0x00000000,  # $0
            "00001": 0x00000000,  # $at
            "00010": 0x00000000,  # $v0
            "00011": 0x00000000,  # $v1
            "00100": 0x00000000,  # $a0
            "00101": 0x00000000,  # $a1
            "00110": 0x00000000,  # $a2
            "00111": 0x00000000,  # $a3
            "01000": 0x00000000,  # $t0
            "01001": 0x00000000,  # $t1
            "01010": 0x00000000,  # $t2
            "01011": 0x00000000,  # $t3
            "01100": 0x00000000,  # $t4
            "01101": 0x00000000,  # $t5
            "01110": 0x00000000,  # $t6
            "01111": 0x00000000,  # $t7
            "10000": 0x00000000,  # $s0
            "10001": 0x00000000,  # $s1
            "10010": 0x00000000,  # $s2
            "10011": 0x00000000,  # $s3
            "10100": 0x00000000,  # $s4
            "10101": 0x00000000,  # $s5
            "10110": 0x00000000,  # $s6
            "10111": 0x00000000,  # $s7
            "11000": 0x00000000,  # $t8
            "11001": 0x00000000,  # $t9
            "11010": 0x00000000,  # $k0
            "11011": 0x00000000,  # $k1
            "11100": 0x00000000,  # $gp
            "11101": 0x7FFFEFFC,  # $sp
            "11110": 0x00000000,  # $fp
            "11111": 0x00000000,  # $ra
        }

        self.register_names = {
            "00000": "$zero",
            "00001": "$at",
            "00010": "$v0",
            "00011": "$v1",
            "00100": "$a0",
            "00101": "$a1",
            "00110": "$a2",
            "00111": "$a3",
            "01000": "$t0",
            "01001": "$t1",
            "01010": "$t2",
            "01011": "$t3",
            "01100": "$t4",
            "01101": "$t5",
            "01110": "$t6",
            "01111": "$t7",
            "10000": "$s0",
            "10001": "$s1",
            "10010": "$s2",
            "10011": "$s3",
            "10100": "$s4",
            "10101": "$s5",
            "10110": "$s6",
            "10111": "$s7",
            "11000": "$t8",
            "11001": "$t9",
            "11010": "$k0",
            "11011": "$k1",
            "11100": "$gp",
            "11101": "$sp",
            "11110": "$fp",
            "11111": "$ra",
        }

    def read_register(self, register):
        if register in self.registers:
            return self.registers[register]
        else:
            return None

    def write_register(self, register, value):
        self.registers[register] = value

    def get_register_name(self, register):
        if register in self.register_names:
            return self.register_names[register]
        else:
            return None


class ALU:
    """Class for MIPS ALU with class method for executing operations"""

    def __init__(self):
        self.srcA = 0x00000000
        self.srcB = 0x00000000
        self.Zero = 0b0
        self.ALU_result = 0x00000000

    def execute_operation(self, opcode):
        if opcode == "100000":  # add operation
            self.ALU_result = self.srcA + self.srcB
        elif opcode == "100010":  # sub operation
            self.ALU_result = self.srcA - self.srcB
        elif opcode == "101010":  # slt operation
            if self.srcA < self.srcB:
                self.ALU_result = 1
            else:
                self.ALU_result = 0


class SignExtender:
    """Class for sign extending 16-bit immediate values to 32-bit"""

    def extend(immediate):

        sign_bit = immediate[0]
        return sign_bit * (32 - len(immediate)) + immediate


class LeftShiftByTwo:
    """Class for left shifting a binary string by two positions"""

    def shift(binary_string):

        return binary_string + "00"
