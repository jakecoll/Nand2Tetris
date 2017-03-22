// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
// pythonic pseudo code:
// i=R0
// j=R1
// R2=0
// while(i>0):
// 		R2 += j
//		i--

//initialize product with 0

@0
D=M
@i
M=D		// i = R0

@1
D=M
@j
M=D		// j = R1

@2
M=0 	// R2 = 0

(WHILE)
	// loop parameter
	@i
	D=M
	@END
	D;JLE

	// loop
	@j
	D=M  	// D=j
	@2
	M=D+M  	//R2=R2+j
	@1
	D=1		//D=1
	@i
	M=M-D	// j--

	@WHILE
	0;JMP  	// iterate over loop again

(END)

	@END
	0;JMP 	//infinite loop
