class Instruction_memory:
    def __init__(self):
        self.memory = {}
        self.A = 0x00000000
        self.RD = 0x00000000
    def RD(self, A):
        self.A = A
        self.RD = self.memory[A]
        return self.RD

class Register_file:
    def __init__(self):
        self.registers = {
            0x00000 : 0,
            0x00001 : 0,
            0x00010 : 0,
            0x00011 : 0,
            0x00100 : 0,
            0x00101 : 0,
            0x00110 : 0,
            0x00111 : 0,
            0x01000 : 0,
            0x01001 : 0,
            0x01010 : 0,
            0x01011 : 0,
            0x01100 : 0,
            0x01101 : 0,
            0x01110 : 0,
            0x01111 : 0,
            0x10000 : 0,
            0x10001 : 0,
            0x10010 : 0,
            0x10011 : 0,
            0x10100 : 0,
            0x10101 : 0,
            0x10110 : 0,
            0x10111 : 0,
            0x11000 : 0,
            0x11001 : 0,
            0x11010 : 0,
            0x11011 : 0,
            0x11100 : 0,
            0x11101 : 0,
            0x11110 : 0x7fffeffc,
            0x11111 : 0,
            0x11111 : 0,
        }
        self.A1 = 0b00000
        self.A2 = 0b00000
        self.A3 = 0b00000
        self.RD1 = 0x00000000
        self.RD2 = 0x00000000
        self.WE3 = 0b0
        self.WD3 = 0x00000000