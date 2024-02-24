from MIPS_components import *


# functions for formatting output shown in CLI
def prPurple(skk):
    print("\033[95m {}\033[00m".format(skk))


def prCyan(skk):
    print("\033[96m {}\033[00m".format(skk))

class Processor:
    """Class for representing a MIPS processor, initialized with its components, and methods for different stages of the 5 stage cycle and for printing the state"""

    def __init__(self):
        self.mem = Memory()
        self.reg_file = Register_file()
        self.alu = ALU()
        self.pc = 0x00400000
        self.clk = 0

        # Control Signals
        self.regDst = 0
        self.branch = 0
        self.memRead = 0
        self.memToReg = 0
        self.aluOp = 00
        self.memWrite = 0
        self.aluSrc = 0
        self.regWrite = 0
        self.jump = 0
    
    def fetch(self):
        """Fetch the next instruction from memory.
        It takes no parameters
        Returns:
        - str: 32 bit Binary representation of the fetched instruction.
        """
        if self.pc not in self.mem.memory:
            print("\nFinished\n")
            return
        print("\nPC:", self.pc)
        instruction = format(self.mem.memory[self.pc], "032b")
        self.pc += 4
        return instruction
    
    def decode(self, instruction):
        """Decode the instruction and extract its fields.
        Parameters:
        - instruction (str): Binary representation of the instruction to be decoded.

        Returns:
        - dict: Dictionary containing the parsed fields of the instruction."""
        # here indexing is left to right as instruction is python string
        opcode = instruction[0:6]
        rs = instruction[6:11]
        rt = instruction[11:16]
        rd = instruction[16:21]
        shamt = instruction[21:26]
        funct = instruction[26:32]
        address = instruction[6:32]
        immediate = instruction[16:32]
        
        parsed_instruction = {
            "opcode": opcode,
            "rs": rs,
            "rt": rt,
            "rd": rd,
            "shamt": shamt,
            "funct": funct,
            "address": address,
            "immediate": immediate,
        }
        
        print(f"parsed instruction is {parsed_instruction}")
        
        return parsed_instruction
    
    def control_unit(self):
        """method to call fetch, decode, and then call the respective functions for the rest 
        of the stages based on opcode - no parameters"""

        while True:

            instruction = self.fetch()
            print(f"Instruction returned from fetch cycle is {instruction}")

            if not instruction:
                break
            
            parsed_instruction = self.decode(instruction)
            opcode = parsed_instruction["opcode"]

            if opcode == "000000":  # R-type
                self.regDst = 1
                self.branch = 0
                self.memRead = 0
                self.memToReg = 0
                self.memWrite = 0
                self.aluSrc = 0
                self.regWrite = 1
                self.jump = 0
                
                if parsed_instruction["funct"] == "100000":
                    self.aluOp = 0b00
                elif parsed_instruction["funct"] == "100010":
                    self.aluOp = 0b01
                elif parsed_instruction["funct"] == "101010":
                    self.aluOp = 0b10
                
                self.print_control_signals()
                prCyan(f"R type instruction")
                self.execute_r_type(parsed_instruction)
                
            elif opcode in [
                "001000",
                "001001",
                "101011",
                "100011",
                "000100",
                "000101",
                "001100",
                "001101",
                "001010",
                "001111",
                "001101",
            ]:  
                self.regDst = 0
                self.branch = 1 if opcode in ["000100", "000101"] else 0
                self.memRead = 1 if opcode == "100011" else 0
                self.memToReg = 1 if opcode in ["001000", "001001"] else 0
                self.aluOp = (
                0b00 if opcode in [
                    "001000",
                    "001001",
                    "101011",
                    "001100",
                    "001101",
                    "001010",
                    "001111",
                    "001101",
                ]
                else 0b01  # for branch
            )
                self.memWrite = 1 if opcode == "101011" else 0
                self.aluSrc = 1
                self.regWrite = 1
                self.jump = 0

                self.print_control_signals()
                prCyan("I type instruction")
                self.execute_i_type(parsed_instruction)
                
            elif opcode in ["000010"]:
                self.regDst = 0
                self.branch = 0
                self.memRead = 0
                self.memToReg = 0
                self.aluOp = 0b00
                self.memWrite = 0
                self.aluSrc = 0
                self.regWrite = 0
                self.jump = 1
                
                self.print_control_signals()
                prCyan("J type instruction")
                self.execute_mem_wb_j_type(parsed_instruction)

    def execute_r_type(self, parsed_instruction):
        """For execute mem wb of r type instructions
        Params:
        - parsed_instruction(dict): Parsed Fields of instruction"""

        funct = parsed_instruction["funct"]
        rs = self.reg_file.read_register(parsed_instruction["rs"])
        rt = self.reg_file.read_register(parsed_instruction["rt"])
        self.alu.srcA = rs
        self.alu.srcB = rt
        if funct == "100000":  # add operation
            prPurple("Executing add operation")
            self.alu.execute_operation("100000")  # add operation
        elif funct == "100010":  # sub operation
            prPurple("Executing sub operation")
            self.alu.execute_operation("100010")  # sub operation
        elif funct == "101010":  # slt operation
            prPurple("Executing slt operation")
            self.alu.execute_operation("101010")  # slt operation
        elif funct == "100001":  # addu operation
            prPurple("Executing addu operation")
            if self.alu.srcA < 0:
                self.alu.srcA = -self.alu.srcA
            if self.alu.srcB < 0:
                self.alu.srcB = -self.alu.srcB
            self.alu.execute_operation("100000")  # add operation
        
        self.mem_read()
        self.write_back(parsed_instruction)

    def execute_i_type(self, parsed_instruction):
        """For execute mem wb of i type instructions
        parameters:
        - parsed instruction ( dict): Parsed fields of the instruction"""

        opcode = parsed_instruction["opcode"]
        immediate_bin = parsed_instruction["immediate"]
        immediate = int(parsed_instruction["immediate"], 2)  # convert it to an integer

        # take care of negative values of immediate
        if immediate_bin[0] == "1":
            immediate = -(2 ** len(immediate_bin) - immediate)

        rs = self.reg_file.read_register(parsed_instruction["rs"])
        rt = self.reg_file.read_register(parsed_instruction["rt"])
        self.alu.srcA = rs
        self.alu.srcB = immediate
        if opcode == "100011":  # lw operation
            prPurple("Executing lw operation")
            self.alu.execute_operation("100000")
            data = self.mem_read()
            self.reg_file.write_register(parsed_instruction["rt"], data)
            return
        elif opcode == "101011":  # sw operation
            prPurple("Executing sw operation")
            self.alu.execute_operation("100000")
            data = rt
            self.mem_read()
            self.mem.write(self.alu.ALU_result, data)
            return
        elif opcode == "001000":  # addi operation
            prPurple("Executing addi operation")
            self.alu.execute_operation("100000")
        elif opcode == "001001":  # addiu operation
            prPurple("Executing addiu operation")
            if rs < 0:
                rs = -rs
            self.alu.execute_operation("100000")
        elif opcode == "001101":  # ori operation
            prPurple("Executing ori operation")
            self.alu.execute_operation("100000")
        elif opcode == "000100":  # beq operation
            prPurple("Executing beq operation")
            if rs == rt:
                offset = immediate
                self.pc += offset * 4  # need to check if +4 is to be added
            return
        elif opcode == "000101":  # bne operation
            prPurple("Executing bne operation")
            if rs != rt:
                offset = immediate
                self.pc += offset * 4
            return
        elif opcode == "001111":  # lui operation
            prPurple("Executing lui operation")
            self.alu.ALU_result = immediate << 16
        
        self.mem_read()
        self.write_back(parsed_instruction)

    def execute_mem_wb_j_type(self, parsed_instruction):
        """For execute mem wb of j type instructions
        parameters:
        - parsed instruction ( dict): Parsed fields of the"""

        opcode = parsed_instruction["opcode"]
        if opcode == "000010":
            prPurple("Executing jmp operation")
            address = int(parsed_instruction["address"], 2)
            self.pc = address << 2
        
        self.mem_read()
        self.write_back(parsed_instruction)
    
    def mem_read(self):
        if(self.memRead):
            data = self.mem.read(self.alu.ALU_result)
            return data
    
    def write_back(self, parsed_instruction):
        if(self.regWrite):
            if(self.regDst):
                self.reg_file.write_register(parsed_instruction["rd"], self.alu.ALU_result)
            else:
                self.reg_file.write_register(parsed_instruction["rt"], self.alu.ALU_result)

    def store_instructions(self, file_name):
        """
        Store instructions from source txt file into memory.

        Parameters:
        - file_name (.txt): Name of the file containing instructions.
        """
        with open(file_name, "r") as file:
            machine_code = file.readlines()

        for instruction in machine_code:
            if instruction.strip():
                x = instruction.split()
                address = int(x[0], 16)
                if address < 0x10010000:
                    instruction = int(x[1], 2)
                else:
                    # handle negative numberss
                    if x[1][0] == "1":
                        instruction = -(2**32 - int(x[1], 2))
                    else:
                        instruction = int(x[1], 2)

                self.mem.memory[address] = instruction

    def print_instruction_memory(self):
        print(
            "-----------------------------------Ins Mem-----------------------------------"
        )
        print("Printing instruction memory........")
        for address, ins in self.mem.memory.items():
            print(f"{address} : {ins}")
        print(
            "-----------------------------------------------------------------------------"
        )

    def print_control_signals(self):
        print(f"Control Signals: regDst = {self.regDst}, branch = {self.branch}, memRead = {self.memRead}, memToReg = {self.memToReg}, aluOp = {self.aluOp}, memWrite = {self.memWrite}, aluSrc = {self.aluSrc}, regWrite = {self.regWrite} and jump = {self.jump}")
    
    def print_state(self):
        print("Processor State:")
        print("Program Counter (PC):", hex(self.pc))
        print("Register File:")
        for reg_num, reg_val in self.reg_file.registers.items():
            print(
                f"Register ${int(reg_num):02d}({self.reg_file.get_register_name(reg_num)}): {hex(reg_val)}"
            )