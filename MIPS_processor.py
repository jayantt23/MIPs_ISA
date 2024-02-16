from MIPS_components import *


class Processor:
    def __init__(self):
        """
        Constructor for initializing memory, register file, ALU, left shifter, and program counter.
        """
        self.mem = Memory()
        self.reg_file = Register_file()
        self.alu = ALU()
        self.Left_shifter = Left_shifter()
        self.pc = 0x00400000

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

    def fetch(self):
        """
        Fetches the next instruction from memory, increments the program counter, and returns the fetched instruction as a 32-bit binary string.
        """
        if self.pc not in self.mem.memory:
            print("\nFinished\n")
            return
        instruction = format(self.mem.memory[self.pc], "032b")
        self.pc += 4
        return instruction

    def decode(self, instruction):
        """
        Decode the given instruction and return a dictionary with the parsed components.
        """
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

    def execute_mem_wb_r_type(self, parsed_instruction):
        """
        Execute the execute, memory, and write back  stage of the R-type instruction.
        Parses the instruction to determine the operation to be executed.
        Updates the ALU source registers and executes the corresponding operation.
        Writes the result back to the destination register.
        """
        funct = parsed_instruction["funct"]
        print(f"funct is {funct}\n")
        if funct == "100000":  # add operation
            print("Executing add operation")
            rs = self.reg_file.read_register(parsed_instruction["rs"])
            rt = self.reg_file.read_register(parsed_instruction["rt"])
            self.alu.srcA = rs
            self.alu.srcB = rt
            self.alu.execute_operation("100000")  # add operation
            self.reg_file.write_register(parsed_instruction["rd"], self.alu.ALU_result)

        elif funct == "100010":  # sub operation
            print("Executing sub operation")
            rs = self.reg_file.read_register(parsed_instruction["rs"])
            rt = self.reg_file.read_register(parsed_instruction["rt"])
            self.alu.srcA = rs
            self.alu.srcB = rt
            self.alu.execute_operation("100010")  # sub operation
            self.reg_file.write_register(parsed_instruction["rd"], self.alu.ALU_result)

        elif funct == "001000":  # jr operation
            print("Executing jr operation")
            rs = parsed_instruction["rs"]
            target_address = self.reg_file.read_register(rs)
            self.pc = target_address

    def execute_mem_wb_i_type(self, parsed_instruction):
        """
        Execute the execute, memory, and memory-write back stage for the I-type instruction.
        This function takes the parsed instruction as input and performs the required operation based on the opcode.
        It updates the registers and memory as per the operation specified in the instruction.
        """
        opcode = parsed_instruction["opcode"]
        immediate_bin = parsed_instruction["immediate"]
        immediate = int(parsed_instruction["immediate"], 2)  # convert it to an integer

        # take care of negative values of immediate
        if immediate_bin[0] == "1":
            immediate = -(2 ** len(immediate_bin) - immediate)

        rs = self.reg_file.read_register(parsed_instruction["rs"])
        rt = self.reg_file.read_register(parsed_instruction["rt"])

        if opcode == "100011":  # lw operation
            print("Executing lw operation")
            address = rs + immediate
            print("address:", address)
            data = self.mem.read(address)
            self.reg_file.write_register(parsed_instruction["rt"], data)
        elif opcode == "101011":  # sw operation
            print("Executing sw operation")
            address = rs + immediate
            data = rt
            self.mem.write(address, data)
        elif opcode == "001000":  # addi operation
            print("Executing addi operation")
            print(f"rs value is {rs}")
            print(f"immediate value is {immediate}")
            result = rs + immediate
            self.reg_file.write_register(parsed_instruction["rt"], result)
        elif opcode == "000100":  # beq operation
            print("Executing beq operation")
            if rs == rt:
                offset = immediate
                self.pc += offset * 4  # need to check if +4 is to be added
        elif opcode == "000101":  # bne operation
            print("Executing bne operation")
            if rs != rt:
                offset = immediate
                self.pc += offset * 4
        elif opcode == "001111":  # lui operation
            print("Executing lui operation")
            immediate = immediate << 16
            value = rt | immediate
            self.reg_file.write_register(parsed_instruction["rt"], value)

        elif opcode == "000111":  # ble operation
            print("Executing ble operation")
            if rs <= rt:
                offset = immediate
                self.pc += offset * 4

        elif opcode == "000011":  # li operation
            print("Executing li operation")
            self.reg_file.write_register(parsed_instruction["rt"], immediate)
        elif opcode == "000010":  # la operation
            print("Executing la operation")
            address = rs + immediate
            data = self.mem.read(address)
            self.reg_file.write_register(parsed_instruction["rt"], data)

        elif opcode == "000100":  # subi operation
            print("Executing subi operation")
            result = rs - immediate
            self.reg_file.write_register(parsed_instruction["rt"], result)

    def execute_mem_wb_j_type(self, parsed_instruction):
        opcode = parsed_instruction["opcode"]
        if opcode == "000010":  # j ( jump)
            print("Executing jmp operation")
            address = int(parsed_instruction["address"], 2)
            updated_pc = self.Left_shifter.shift(address)
            self.pc = updated_pc

        elif opcode == "000011":  # jal (jump and link)
            print("Executing jal operation")
            address = int(parsed_instruction["address"], 2)
            updated_pc = self.Left_shifter.shift(address)
            self.reg_file.write_register("$ra", self.pc + 4)
            self.pc = updated_pc

    def store_instructions(self, file_name):
        with open(file_name, "r") as file:
            machine_code = file.readlines()

        # address = 0

        # fill the instruction memory, this is for simulation purposes only

        for instruction in machine_code:
            if instruction.strip():
                x = instruction.split()
                address = int(x[0], 16)
                instruction = x[1]

                self.mem.memory[address] = int(instruction, 2)

    def execute_instruction(self):

        # self.pc = 0x00000000

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
                "001111",
            ]:
                print("I type instruction \n")
                self.execute_mem_wb_i_type(parsed_instruction)
            elif opcode in ["000010"]:
                print("J type instruction \n")
                self.execute_mem_wb_j_type(parsed_instruction)

            if self.pc == len(self.mem.memory):
                break


if __name__ == "__main__":

    processor = Processor()

    processor.store_instructions("./factorial.txt")
    processor.print_instruction_memory()
    processor.execute_instruction()

    processor.print_state()
