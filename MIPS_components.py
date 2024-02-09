class Memory:
    def __init__(self):
        self.memory = {}

class Instruction_memory(Memory):
    def __init__(self):
        self.A = 0x00000000
        self.RD = 0x00000000
    def RD(self, A):
        self.A = A
        self.RD = Memory.memory[A]
        return self.RD

class Register_file:
    def __init__(self):
        self.registers = {
            0x00000 : 0x00000000, # $0
            0x00001 : 0x00000000, # $at
            0x00010 : 0x00000000, # $v0
            0x00011 : 0x00000000, # $v1
            0x00100 : 0x00000000, # $a0
            0x00101 : 0x00000000, # $a1
            0x00110 : 0x00000000, # $a2
            0x00111 : 0x00000000, # $a3
            0x01000 : 0x00000000, # $t0
            0x01001 : 0x00000000, # $t1
            0x01010 : 0x00000000, # $t2
            0x01011 : 0x00000000, # $t3
            0x01100 : 0x00000000, # $t4
            0x01101 : 0x00000000, # $t5
            0x01110 : 0x00000000, # $t6
            0x01111 : 0x00000000, # $t7
            0x10000 : 0x00000000, # $s0
            0x10001 : 0x00000000, # $s1
            0x10010 : 0x00000000, # $s2
            0x10011 : 0x00000000, # $s3
            0x10100 : 0x00000000, # $s4
            0x10101 : 0x00000000, # $s5
            0x10110 : 0x00000000, # $s6
            0x10111 : 0x00000000, # $s7
            0x11000 : 0x00000000, # $t8
            0x11001 : 0x00000000, # $t9
            0x11010 : 0x00000000, # $k0
            0x11011 : 0x00000000, # $k1
            0x11100 : 0x00000000, # $gp
            0x11101 : 0x7fffeffc, # $sp
            0x11110 : 0x00000000, # $fp
            0x11111 : 0x00000000, # $ra
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

class ALU:
    def __init__(self):
        self.srcA = 0x00000000
        self.srcB = 0x00000000
        self.Zero = 0b0
        self.ALU_result = 0x00000000

class Data_Memory(Memory):
    def __init__(self):
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

class Adder:
    def __init__(self):
        pass
    
    def add(self, A, B):
        return A+B
    
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
        return A<<2