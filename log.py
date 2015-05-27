#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
import os

class Log:
	def __init__(self, start, init):
		self.log = init
		if not os.path.exists(os.getcwd()+'/log/session '+start+'.log'):
			self.logFile = open(os.getcwd()+'/log/session '+start+'.log','w')
		else:
			self.logFile = open(os.getcwd()+'/log/session '+start+'.log','a')

		self.logFile.write(self.log)
		self.write('création du log\n')	
	
	def __del__(self):
		self.logFile.close()
		del(self.log)
		del(self.logFile)
	
	def __str__(self):
		return self.log
	
	def print(self):
		return print(self.log)
	
	def write(self, txt):
		self.logFile.write(txt)
		self.log += txt
	
	def iadd(self,txt):
		# l'opérateur += redirige vers Log.write()
		self.write(self,txt);



