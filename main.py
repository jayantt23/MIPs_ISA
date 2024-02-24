from MIPS_processor import Processor


def main():
    processor = Processor()

    # processor.store_instructions("search.txt")
    # processor.store_instructions("factorial.txt")
    processor.store_instructions("insertion_sort.txt")

    processor.control_unit()

    processor.print_state()
    processor.print_instruction_memory()


main()

# for search value stored in t2
