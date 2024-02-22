from MIPS_components import *


def prPurple(skk):
    print("\033[95m {}\033[00m".format(skk))


def prCyan(skk):
    print("\033[96m {}\033[00m".format(skk))


class Processor:
    """Processor Class representing a MIPS processor"""

    def __init__(self):
        self.mem = Memory()
        self.reg_file = Register_file()
        self.alu = ALU()
        self.pc = 0x00400000

    def fetch(self):
        """Fetch the next instruction from memory."""
        if self.pc not in self.mem.memory:
            print("\nFinished\n")
            return
        print("\nPC:", self.pc)
        instruction = format(self.mem.memory[self.pc], "032b")
        self.pc += 4
        return instruction

    def decode(self, instruction):
        """Decode the instruction and extract its fields."""
        # here indexing is left to right
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

    def execute_instruction(self):

        while True:

            instruction = self.fetch()
            print(f"Instruction returned from fetch cycle is {instruction}")
            # if instruction == "halt":  # look up what shoud go here
            #     break

            if not instruction:
                break

            parsed_instruction = self.decode(instruction)
            opcode = parsed_instruction["opcode"]

            if opcode == "000000":  # R-type
                prCyan(f"R type instruction")
                self.execute_mem_wb_r_type(parsed_instruction)
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
                prCyan("I type instruction")
                self.execute_mem_wb_i_type(parsed_instruction)
            elif opcode in ["000010"]:
                prCyan("J type instruction")
                self.execute_mem_wb_j_type(parsed_instruction)

    def execute_mem_wb_r_type(self, parsed_instruction):
        """For execute mem wb of r type instructions"""
        funct = parsed_instruction["funct"]
        rs = self.reg_file.read_register(parsed_instruction["rs"])
        rt = self.reg_file.read_register(parsed_instruction["rt"])
        self.alu.srcA = rs
        self.alu.srcB = rt
        if funct == "100000":  # add operation
            prPurple("Executing add operation")
            self.alu.execute_operation("100000")  # add operation
            self.reg_file.write_register(parsed_instruction["rd"], self.alu.ALU_result)
        elif funct == "100010":  # sub operation
            prPurple("Executing sub operation")
            self.alu.execute_operation("100010")  # sub operation
            self.reg_file.write_register(parsed_instruction["rd"], self.alu.ALU_result)
        elif funct == "101010":  # slt operation
            prPurple("Executing slt operation")
            self.alu.execute_operation("101010")  # slt operation
            self.reg_file.write_register(parsed_instruction["rd"], self.alu.ALU_result)
        elif funct == "100001":  # addu operation
            prPurple("Executing addu operation")
            if self.alu.srcA < 0:
                self.alu.srcA = -self.alu.srcA
            if self.alu.srcB < 0:
                self.alu.srcB = -self.alu.srcB
            self.alu.execute_operation("100000")  # add operation
            self.reg_file.write_register(parsed_instruction["rd"], self.alu.ALU_result)

    def execute_mem_wb_i_type(self, parsed_instruction):
        """For execute mem wb of i type instructions"""

        opcode = parsed_instruction["opcode"]
        immediate_bin = parsed_instruction["immediate"]
        immediate = int(parsed_instruction["immediate"], 2)  # convert it to an integer

        # take care of negative values of immediate
        if immediate_bin[0] == "1":
            immediate = -(2 ** len(immediate_bin) - immediate)

        rs = self.reg_file.read_register(parsed_instruction["rs"])
        rt = self.reg_file.read_register(parsed_instruction["rt"])

        if opcode == "100011":  # lw operation
            prPurple("Executing lw operation")
            address = rs + immediate
            data = self.mem.read(address)
            self.reg_file.write_register(parsed_instruction["rt"], data)
        elif opcode == "101011":  # sw operation
            prPurple("Executing sw operation")
            address = rs + immediate
            data = rt
            self.mem.write(address, data)
        elif opcode == "001000":  # addi operation
            prPurple("Executing addi operation")
            result = rs + immediate
            self.reg_file.write_register(parsed_instruction["rt"], result)
        elif opcode == "001001":  # addiu operation
            prPurple("Executing addiu operation")
            if rs < 0:
                rs = -rs
            result = rs + immediate
            self.reg_file.write_register(parsed_instruction["rt"], result)
        elif opcode == "001101":  # ori operation
            prPurple("Executing ori operation")
            result = rs | immediate
            self.reg_file.write_register(parsed_instruction["rt"], result)
        elif opcode == "000100":  # beq operation
            prPurple("Executing beq operation")
            if rs == rt:
                offset = immediate
                self.pc += offset * 4  # need to check if +4 is to be added
        elif opcode == "000101":  # bne operation
            prPurple("Executing bne operation")
            if rs != rt:
                offset = immediate
                self.pc += offset * 4
        elif opcode == "001111":  # lui operation
            prPurple("Executing lui operation")
            value = 0x10010000
            self.reg_file.write_register(parsed_instruction["rt"], value)

    def execute_mem_wb_j_type(self, parsed_instruction):
        """For execute mem wb of j type instructions"""

        opcode = parsed_instruction["opcode"]
        if opcode == "000010":
            prPurple("Executing jmp operation")
            address = int(parsed_instruction["address"], 2)
            self.pc = address << 2

    def store_instructions(self, file_name):
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

    def print_state(self):
        print("Processor State:")
        print("Program Counter (PC):", hex(self.pc))
        print("Register File:")
        for reg_num, reg_val in self.reg_file.registers.items():
            print(
                f"Register ${int(reg_num):02d}({self.reg_file.get_register_name(reg_num)}): {hex(reg_val)}"
            )


if __name__ == "__main__":

    processor = Processor()

    processor.store_instructions("./insertion_sort.txt")
    processor.print_instruction_memory()
    processor.execute_instruction()

    processor.print_state()
    processor.print_instruction_memory()
