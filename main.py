from MIPS_processor import Processor


def main():
    processor = Processor()

    # processor.store_instructions("search.txt")
    # processor.store_instructions("factorial.txt")
    processor.store_instructions("insertion_sort.txt")

    processor.execute_instruction()

    processor.print_state()


main()

# for search value stored in t2
