.data
n: 5
ans:

.text
.globl main
main:
	lw $s0, n
	addi $s0, $s0, 1
	addi $t0, $0, 1
	addi $t1, $0, 2
	j factorial

	
factorial :
	add $t2, $0, $t1
	add $t3, $0, $0
	j multiply

fac :
	add $t0, $0, $t3
	addi $t1, $t1, 1
	bne $t1, $s0, factorial
	j result

multiply :
	add $t3, $t3, $t0
	addi $t2, $t2, -1
	bne $t2, $0, multiply
	j fac

result :
	add $s1, $0, $t0
	sw $s1 ans
