#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module for char input reading'''
import sys, tty, termios

class stdInput:
	def __init__(self):
		self.fd = sys.stdin.fileno()
		self.originalSet = termios.tcgetattr(self.fd)
		self.lineReading = True
		self.charReading = False
	
	
	def switch(self):
		if self.lineReading:
			self.setCharReading()
		else:
			self.setLineReading()
	
	
	def setLineReading(self):
		termios.tcsetattr(self.fd, termios.TCSANOW , self.originalSet)
		self.lineReading = True
		self.charReading = False
	
	
	def setCharReading(self):
		tty.setraw(self.fd)
		self.lineReading = False
		self.charReading = True
	
	def readChar(self):
		return sys.stdin.read(1)

