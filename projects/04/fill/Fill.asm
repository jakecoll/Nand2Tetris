// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(INIT)
	@8192 	//32 x 256 number of 16 bit pixels
	D=A
	@i
	M=D  	// index var at 8192


(LOOP) //go through index backwards

	@i
	M=M-1
	D=M
	@INIT 	//if index complete re-initialize
	D;JLT
	@KBD 	//keyboard address load
	D=M  	// d equals value
	@CLEAR  
	D;JEQ   //if no value jump to clear
	@FILL   // o/w jump to fill
	0;JMP

	

	//fill screen
	(FILL)
		@SCREEN  //load screen value
		D=A
		@i
		A=D+M  
		M=-1
		@LOOP
		0;JMP

	//clear screen
	(CLEAR)

		@SCREEN
		D=A
		@i
		A=D+M
		M=0
		@LOOP
		0;JMP





