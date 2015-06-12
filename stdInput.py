#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module for char input reading'''
import sys, tty, termios

class stdInput:
	'''a class to make an object to manage stdin method'''
	
	def __init__(self):
		'''init stdInput object'''
		self.stdinFileDescriptor = sys.stdin.fileno()
		self.stdinOriginalSet = termios.tcgetattr(self.stdinFileDescriptor)
		self.lineReading = True
		self.charReading = False
	
	
	def switch(self):
		'''switch between 2 input method : line by line or char by char'''
		if self.lineReading:
			self.setCharReading()
		else:
			self.setLineReading()
	
	
	def setLineReading(self):
		'''switch to line by line input mode'''
		termios.tcsetattr(self.stdinFileDescriptor, termios.TCSANOW , self.stdinOriginalSet)
		self.lineReading = True
		self.charReading = False
	
	
	def setCharReading(self):
		'''switch to char by char input mode'''
		tty.setraw(self.stdinFileDescriptor)
		self.lineReading = False
		self.charReading = True
	
	def readChar(self):
		''' read one char in standard input stream'''
		if self.charReading:
			return sys.stdin.read(1)
		else:
			self.switch()
			ch = sys.stdin.read(1)
			self.switch()
			return ch
	
	def readMultiChar(self, nb = 1):
		''' read multiple char in standard input stream whithout waiting for a line break'''
		if nb <= 1:
			return self.readChar()
		
		switch = not(self.charReading)
		if switch:
			self.switch()
		
		ch=''
		# get and write the input char, one by one
		while nb > 0:
			ch += sys.stdin.read(1)
			print(ch[len(ch)-1], end = '',flush=True)
			nb -= 1
		
		if switch:
			self.switch()
		
		return ch
		

