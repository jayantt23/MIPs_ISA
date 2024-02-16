.data
array:      .word   1, 4, 3, 2, 7, 6         # Initial array
search_value: .word -5                     # Value to search for

array_size: .word 6                           # Size of the array

.text
.globl main

main:
    la $t0, array                     # Load address of the array
    lw $t1, search_value              # Load the value to search for
    lw $t5, array_size                # Load the size of the array
    li $t2, -1                        # Initialize index result to -1
    li $t3, 0                         # Initialize i = 0

search_loop:
    bge $t3, $t5, exit      # Exit loop if end of array is reached

    lw $t4, 0($t0)                   # Load element from array
    beq $t4, $t1, element_found      # Branch if element is found

    addi $t0, $t0, 4                 # Move to next element in array
    addi $t3, $t3, 1                 # i++
    j search_loop

element_found:
    move $t2, $t3                    # Store index of found element
    j exit

exit:
li $v0, 10
syscall

  
