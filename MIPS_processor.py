import MIPS_components as comp

class Processor:
    def __init__(self):
        self.inst_mem = comp.Instruction_memory()
        self.reg_file = comp.Register_file()
        self.alu = comp.ALU()
        self.data_mem = comp.Data_Memory()