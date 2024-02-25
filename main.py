from MIPS_processor import Processor


def main():
    processor = Processor()

    print("Program 1: Linear Search of given input in array [1, 4, 3, 2, 7, 6]")
    print("Program 2: Factorial of given input")
    print("Program 3: Sorting array [-2, 1, 0, 3, 2, -8, 6, 10, 9] using Insertion Sort")
    n = int(input("Which program do you want to run: "))
    
    if(n==1):
        processor.store_instructions("search.txt")
        k = int(input("Search Value: "))
        processor.mem.write(0x10010000 + 0x18, k)
    elif(n==2):
        processor.store_instructions("factorial.txt")
        k = int(input("n: "))
        processor.mem.write(0x10010000, k)
    elif(n==3):
        processor.store_instructions("insertion_sort.txt")

    processor.control_unit()

    processor.print_state()
    processor.print_instruction_memory()
    
    if(n==1):
        print("Output of Search ($t2):", processor.mem.read(0x10010020))
    elif(n==2):
        print("Output of factorial ($s1):", processor.mem.read(0x10010000 + 0x4))
    elif(n==3):
        print("Output array:", processor.mem.read(0x10010000), processor.mem.read(0x10010000 + 0x4), processor.mem.read(0x10010000 + 0x8),
               processor.mem.read(0x10010000 + 0xc), processor.mem.read(0x10010000 + 0x10), processor.mem.read(0x10010000 + 0x14), 
               processor.mem.read(0x10010000 + 0x18), processor.mem.read(0x10010000 + 0x1c), processor.mem.read(0x10010000 + 0x20))


main()

# for search value stored in t2
