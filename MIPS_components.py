class Memory:
    def __init__(self):
        self.memory = {}


class Instruction_memory(Memory):
    def __init__(self):
        super().__init__()
        # self.A = 0x00000000
        # self.RD = 0x00000000

    # def RD(self, A):
    #     self.A = A
    #     self.RD = Memory.memory[A]
    #     return self.RD

    # for simulation purposed not in the control of hte user in actual mips
    # def write(self, address, data):
    #     self.memory[address] = data

    def read(self, address):
        if address in self.memory:
            return self.memory[address]
        else:
            return None


class Register_file:
    def __init__(self):
        # error: 0x used instead of 0b!
        # self.registers = {
        #     0x00000: 0x00000000,  # $0
        #     0x00001: 0x00000000,  # $at
        #     0x00010: 0x00000000,  # $v0
        #     0x00011: 0x00000000,  # $v1
        #     0x00100: 0x00000000,  # $a0
        #     0x00101: 0x00000000,  # $a1
        #     0x00110: 0x00000000,  # $a2
        #     0x00111: 0x00000000,  # $a3
        #     0x01000: 0x00000000,  # $t0
        #     0x01001: 0x00000000,  # $t1
        #     0x01010: 0x00000000,  # $t2
        #     0x01011: 0x00000000,  # $t3
        #     0x01100: 0x00000000,  # $t4
        #     0x01101: 0x00000000,  # $t5
        #     0x01110: 0x00000000,  # $t6
        #     0x01111: 0x00000000,  # $t7
        #     0x10000: 0x00000000,  # $s0
        #     0x10001: 0x00000000,  # $s1
        #     0x10010: 0x00000000,  # $s2
        #     0x10011: 0x00000000,  # $s3
        #     0x10100: 0x00000000,  # $s4
        #     0x10101: 0x00000000,  # $s5
        #     0x10110: 0x00000000,  # $s6
        #     0x10111: 0x00000000,  # $s7
        #     0x11000: 0x00000000,  # $t8
        #     0x11001: 0x00000000,  # $t9
        #     0x11010: 0x00000000,  # $k0
        #     0x11011: 0x00000000,  # $k1
        #     0x11100: 0x00000000,  # $gp
        #     0x11101: 0x7FFFEFFC,  # $sp
        #     0x11110: 0x00000000,  # $fp
        #     0x11111: 0x00000000,  # $ra
        # }

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

        self.A1 = 0b00000
        self.A2 = 0b00000
        self.A3 = 0b00000
        self.RD1 = 0x00000000
        self.RD2 = 0x00000000
        self.WD3 = 0x00000000

    def RD1(self, A1):
        self.A1 = A1
        self.RD1 = self.registers[self.A1]
        return self.RD1

    def RD2(self, A2):
        self.A2 = A2
        self.RD2 = self.registers[self.A2]
        return self.RD2

    def WB(self, A3, WD3):
        self.A3 = A3
        self.WD3 = WD3
        self.registers[self.A3] = self.WD3
        return

    def read_register(self, register):
        if register in self.registers:
            return self.registers[register]
        else:
            return None

    def write_register(self, register, value):
        print(
            f"Writing to register {register} ({self.get_register_name(register)}): {value}\n"
        )
        self.registers[register] = value
        print(f"Changed made {register} : {self.registers[register]}")

    def get_register_name(self, register):
        if register in self.register_names:
            return self.register_names[register]
        else:
            return None


class ALU:
    def __init__(self):
        self.srcA = 0x00000000
        self.srcB = 0x00000000
        self.Zero = 0b0
        self.ALU_result = 0x00000000

    def execute_operation(self, opcode):
        if opcode == "100000":  # add operation
            self.execute_add()
        elif opcode == "100010":  # sub operation
            self.execute_sub()

    def execute_add(self):
        self.ALU_result = self.srcA + self.srcB

    def execute_sub(self):
        self.ALU_result = self.srcA - self.srcB


class Data_Memory(Memory):
    def __init__(self):
        super().__init__()
        self.A = 0x00000000
        self.WD = 0x00000000
        self.RD = 0x00000000

    def RD(self, A):
        self.A = A
        self.RD = Memory.memory[self.A]
        return self.RD

    def WB(self, A, WD):
        self.A = A
        self.WD = WD
        Memory.memory[self.A] = self.WD
        return

    def read(self, address):
        return self.memory.get(address, 0x00000000)  # ret 0 if add not found


class Adder:
    def __init__(self):
        pass

    def add(self, A, B):
        return A + B


class Sign_extend:
    def __init__(self):
        self.imm = 0x0000
        self.sign_imm = 0x00000000

    def extend(self, imm):
        self.imm = imm
        self.sign_imm = 0x00000000 | self.imm
        return self.sign_imm


class Left_shifter:
    def __init__(self):
        pass

    def shift(self, A):
        return A << 2
