
	.data
comma: .asciiz ","
open: .asciiz "["
close: .asciiz " ]"
space:	.asciiz " "		# a space string.
line:	.asciiz	"\n"		# a newline string.
colon:	.asciiz ": "	# a colon string with space.
array:	.word	0 : 5000	# an array of word, for storing values.
size:	.word			# will get overwritten once the user enters something else

input_array_size:	.asciiz	"Input array size ([0,5000]): "
input_each_value:	.asciiz	"Input value "
after_sorting:	.asciiz "Sorted array:\n"
unsorted_array: .asciiz "Unsorted array given as input:\n"

	.text # start of the code
	.globl	main # variables to be accessed inside main too
main: # start of the main function
promt_user:
# a0 to a3 are argument registers used to pass arguments to # function or sys call
# v0 and v1 value registers, used to hold returnva lues from function or system calls
# a0 used for passing data to system calls that required input arguments

	li	$v0, 4			# 4 -> print string system call
	la	$a0, input_array_size	# address of string to a0
	syscall				
read_size:
	li	$v0, 5			# 5 -> read integer system call from user input,  then stores the integer in v0
	syscall				
	la	$t0, size		# t0 (temp reg) now holds address of size
	sw	$v0, 0($t0)		# stores value of integer read (ie size) into memory location which initially had size
				
initialize:
	la	$t0, array		# array location, la doesn't give value stored in array but where array is
	lw	$t1, size		# size of array
	li	$t2, 0			# start from 0, kind of like i = 0
read_values_loop:
	bge	$t2, $t1, populating_array_finish	# while i < arr.size() t2 < t1 do the stuff under, else branch, if i>= arr.size() end
	li	$v0, 4			
	la	$a0, input_each_value 
	syscall				# print "Input value "
	li	$v0, 1			# 1 ->print integer - iteration count
	addi	$a0, $t2, 1		# i+1 into a0
	syscall				# issue a system call.
	li	$v0, 4			
	la	$a0, colon		# put a : into a0
	syscall				# print it

	li	$v0, 5			# sys call to read an integer from user and store it in v0
	syscall				
	sw	$v0, 0($t0)		# t0 contains addres of array, store into the array value which was jsut read

	addi	$t0, $t0, 4		# now t0 containes array + 4 so array[1]
	addi	$t2, $t2, 1		# i++
	j	read_values_loop	# jump back to the beginning of the loop.
populating_array_finish:
	li $v0, 4
	la $a0, unsorted_array
	syscall
	jal	print			# print teh array ( jal - jump and link)
initialize_before_sorting:
	la	$t0, array		# pointer ot beginning of array
	lw	$t1, size		# array size stored in t1
	li	$t2, 1			# int i = 1
outer_loop:
	la	$t0, array		# pointer to begining of array
	bge	$t2, $t1, outer_done	# branch if i >= arr.size()
	move	$t3, $t2		# j = i because we sort till i
inner_loop:
	la	$t0, array		
	mul	$t5, $t3, 4		# j*4 so index for jth element
	add	$t0, $t0, $t5		#  base element + 4*j -> arr[j] address
	ble	$t3, $zero, inner_loop_end	# while j > 0 do stuff under, may happen that element to be inserted in index 0 in that case j-1 segmentation fault
	lw	$t7, 0($t0)		# t7 <- contents of a[j]
	lw	$t6, -4($t0)		# t6 <- contents of a[j-1]
	bge	$t7, $t6, inner_loop_end	# while a[j] < a[j-1] we have to do swaps
	# we are inserting elements into already sorted array so we just swap back till a[j-1] > a[j]
	lw	$t4, 0($t0) # t4 <- a[j] so this is like temp = a[j]
	sw	$t6, 0($t0) # a[j] = a[j-1]
	sw	$t4, -4($t0) # a[j-1] = temp
	subi	$t3, $t3, 1 # j--
	j	inner_loop		
inner_loop_end:
	addi	$t2, $t2, 1		# i++
	j	outer_loop		
outer_done:
	li	$v0, 4			# print string
	la	$a0, after_sorting
	syscall						
	jal	print		
exit:
	li	$v0, 10			# exit
	syscall				

print:
initialize_variables:
	la	$t0, array # pointer to array in t0, base address 
	lw	$t1, size # array size in t1
	li	$t2, 0 # i = 0
	li $v0, 4
	la $a0, open
	syscall
loop_print:
	bge	$t2, $t1, print_done # as long as i < arr.size() do stuff under
	beq $t2, $0, print_element # so that comme not printing before first element
	li $v0, 4
	la $a0, comma
	syscall
print_element:
	li	$v0, 4 # print a string ie empty space
	la	$a0, space
	syscall
	li	$v0, 1 # sys call for printing an integer
	lw	$a0, 0($t0) # store el pointed to by t0 into a0
	syscall # print stuff(integer) stored in a0
	addi	$t0, $t0, 4 # basically move array pointer by one element
	addi	$t2, $t2, 1 # i++
	j loop_print

print_done:
	li $v0, 4
	la $a0, close
	syscall
	li	$v0, 4
	la	$a0, line # print an empty line after
	syscall
	jr	$ra # jump back to the address stored in ra, basically where jumping occured for this printing