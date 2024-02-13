from MIPS_components import *


class Processor:
    def __init__(self):
        self.inst_mem = Instruction_memory()
        self.reg_file = Register_file()
        self.alu = ALU()
        self.data_memory = Data_Memory()
        self.sign_extender = Sign_extend()
        self.Left_shifter = Left_shifter()
        # self.pc = 0x00400000
        # self.pc = 0x00000000
        self.pc = 0

    def print_instruction_memory(self):
        print("--------Ins Mem-----------------------------------")
        print("Printing instruction memory........")
        for address, ins in self.inst_mem.memory.items():
            print(f"{address} : {ins}")
        print("--------------------------------------------------")

    def print_state(self):
        print("Processor State:")
        print("Program Counter (PC):", hex(self.pc))
        print("Register File:")
        for reg_num, reg_val in self.reg_file.registers.items():
            print(
                f"Register ${int(reg_num):02d}({self.reg_file.get_register_name(reg_num)}): {hex(reg_val)}"
            )

    def fetch(self):

        instruction = ""
        for _ in range(4):
            instruction += format(self.inst_mem.memory[self.pc], "08b")
            self.pc += 1
            print(
                f"currently doing fetch instruction is {instruction}  and pc is {self.pc}\n"
            )
        return instruction

    def decode(self, instruction):
        parsed_instruction = self.parse_instruction(instruction)
        return parsed_instruction

    def execute_mem_wb_r_type(self, parsed_instruction):
        funct = parsed_instruction["funct"]
        print(f"funct is {funct}\n")
        if funct == "100000":  # add operation
            rs = self.reg_file.read_register(parsed_instruction["rs"])
            rt = self.reg_file.read_register(parsed_instruction["rt"])
            self.alu.srcA = rs
            self.alu.srcB = rt
            self.alu.execute_operation("100000")  # add operation
            self.reg_file.write_register(parsed_instruction["rd"], self.alu.ALU_result)
        elif funct == "100010":  # sub operation
            rs = self.reg_file.read_register(parsed_instruction["rs"])
            rt = self.reg_file.read_register(parsed_instruction["rt"])
            self.alu.srcA = rs
            self.alu.srcB = rt
            self.alu.execute_operation("100010")  # sub operation
            self.reg_file.write_register(parsed_instruction["rd"], self.alu.ALU_result)

    def execute_mem_wb_i_type(self, parsed_instruction):
        opcode = parsed_instruction["opcode"]
        immediate_bin = parsed_instruction["immediate"]
        immediate = int(parsed_instruction["immediate"], 2)  # convert it to an integer
        immediate = self.sign_extender.extend(immediate)

        # take care of negative values of immediate
        if immediate_bin[0] == "1":
            immediate = -(2 ** len(immediate_bin) - immediate)

        rs = self.reg_file.read_register(parsed_instruction["rs"])
        rt = self.reg_file.read_register(parsed_instruction["rt"])

        if opcode == "100011":  # lw operation
            address = rs + immediate
            data = self.data_memory.read(address)
            self.reg_file.write_register(parsed_instruction["rt"], data)
        elif opcode == "101011":  # sw operation
            address = rs + immediate
            data = rt
            self.data_memory.write(address, data)
        elif opcode == "001000":  # addi operation
            print(f"rs value is {rs}")
            print(f"immediate value is {immediate}")
            result = rs + immediate
            self.reg_file.write_register(parsed_instruction["rt"], result)
        elif opcode == "000100":  # beq operation
            if rs == rt:
                offset = immediate
                self.pc += offset * 4  # need to check if +4 is to be added
        elif opcode == "000101":  # bne operation
            if rs != rt:
                offset = immediate
                self.pc += offset * 4

    def execute_mem_wb_j_type(self, parsed_instruction):
        opcode = parsed_instruction["opcode"]
        if opcode == "000010":
            address = int(parsed_instruction["address"], 2)
            address = parsed_instruction["address"]
            updated_pc = self.Left_shifter.shift(int(address, 2))
            updated_pc = (
                updated_pc >> 4
            )  # this is technically done by taking 4 zero lines from the bus with pc + 4
            self.pc = updated_pc

    def parse_instruction(self, instruction):
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

    def store_instructions(self, file_name):
        with open(file_name, "r") as file:
            machine_code = file.readlines()

        address = 0

        # fill the instruction memory, this is for simulation purposes only

        for instruction in machine_code:
            # split the 32 bit instruction into 4 locations
            for i in range(4):
                # self.inst_mem.write(address, int(instruction[i * 8 : (i + 1) * 8], 2))
                self.inst_mem.memory[address] = int(
                    instruction[i * 8 : (i + 1) * 8], 2
                )  # store an integer value in each address, this can later be converted to 8 bit binary
                # working correctly
                print(
                    f"Wrote into instruction memory, {address} : {int(instruction[i*8 : (i+1)*8], 2)}\n"
                )

                address += 1

    def execute_instruction(self):

        # self.pc = 0x00000000
        self.pc = 0

        while True:

            instruction = self.fetch()
            print(f"Instruction returned from fetch cycle is {instruction}\n")
            if instruction == "halt":  # look up what shoud go here
                break

            if not instruction:
                break

            parsed_instruction = self.decode(instruction)
            opcode = parsed_instruction["opcode"]

            if opcode == "000000":  # R-type
                print(f"R type instruction \n")
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
            ]:
                print("I type instruction \n")
                self.execute_mem_wb_i_type(parsed_instruction)
            elif opcode in ["000010"]:
                print("J type instruction \n")
                self.execute_mem_wb_j_type(parsed_instruction)

            if self.pc == len(self.inst_mem.memory):
                break


if __name__ == "__main__":

    processor = Processor()

    processor.store_instructions("./testing.txt")
    processor.print_instruction_memory()
    processor.execute_instruction()

    processor.print_state()
