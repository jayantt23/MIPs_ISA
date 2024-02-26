.data
n: 5
ans:

.text
.globl main
main:
	lw $s0, n		# Load n from memory
	addi $s0, $s0, 1	# increment n by 1
	addi $t0, $0, 1		# Initialize result to 1
	addi $t1, $0, 2		# Initialize counter to 1
factorial1 :
	add $t2, $0, $t1	
	add $t3, $0, $0
multiply :			# multiply result by counter
	add $t3, $t3, $t0
	addi $t2, $t2, -1
	bne $t2, $0, multiply	# if n != 0, repeat
factorial2 :
	add $t0, $0, $t3
	addi $t1, $t1, 1
	bne $t1, $s0, factorial1
done :
	add $s1, $0, $t0	# Storing the result in s1
	sw $s1 ans 		# Storing the result from s1 reg to memory
