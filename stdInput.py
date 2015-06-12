#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module for char input reading'''
import sys, tty, termios

class stdInput:
	def __init__(self):
		self.stdinFileDescriptor = sys.stdin.fileno()
		self.stdinOriginalSet = termios.tcgetattr(self.stdinFileDescriptor)
		self.lineReading = True
		self.charReading = False
	
	
	def switch(self):
		if self.lineReading:
			self.setCharReading()
		else:
			self.setLineReading()
	
	
	def setLineReading(self):
		termios.tcsetattr(self.stdinFileDescriptor, termios.TCSANOW , self.stdinOriginalSet)
		self.lineReading = True
		self.charReading = False
	
	
	def setCharReading(self):
		tty.setraw(self.stdinFileDescriptor)
		self.lineReading = False
		self.charReading = True
	
	def readChar(self):
		if self.charReading:
			return sys.stdin.read(1)
		else:
			self.switch()
			ch = sys.stdin.read(1)
			self.switch()
			return ch
	
	def readMultiChar(self, nb = 1):
		if nb == 1:
			return self.readChar()
		
		if nb < 1:
			return ''
		
		switch = not(self.charReading)
		
		if switch:
			self.switch()
		
		ch=''
		while nb > 0:
			ch += sys.stdin.read(1)
			print(ch[len(ch)-1], end = '',flush=True)
			nb -= 1
		
		if switch:
			self.switch()
		
		return ch
		

