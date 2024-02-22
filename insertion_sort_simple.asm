.data
array:      .word   -2, 1, 0, 3, 2, -8, 6, 10, 9     # Initial array to be sorted
size:       .word 9 # 9 elements in the array


	.text # start of the code
	.globl	main # variables to be accessed inside main too
main: # start of the main function
			
initialize:
	la	$t0, array		# array location, la doesn't give value stored in array but where array is
	lw	$t1, size		# size of array
	li	$t2, 0			# start from 0, kind of like i = 0

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
exit:
	li	$v0, 10			# exit
	syscall				
