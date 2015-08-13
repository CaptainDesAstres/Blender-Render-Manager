#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module who manage the log of the script'''
import os

class Log:
	'''class who manage the log of the script
there is to log: 
	the file where is save the log at each new line,
	the string who is print eache time that the standart output is erase'''
	
	def __init__(self, start, init):
		'''initialize the log object and open the log file'''
		self.log = init
		if not os.path.exists(os.getcwd()+'/log/session '+start+'.log'):
			self.logFile = open(os.getcwd()+'/log/session '+start+'.log','w')
		else:
			self.logFile = open(os.getcwd()+'/log/session '+start+'.log','a')
		
		self.logFile.write(self.log)
		self.write('création du log\n')
		
		self.menu = []
		
		self.runMenu = None
	
	
	
	
	def __del__(self):
		'''close the log file when the object is deleted'''
		self.logFile.close()
		del(self.log)
		del(self.logFile)
	
	
	
	
	def __str__(self):
		'''return string log'''
		return self.log
	
	
	
	
	def print(self, menu = True):
		'''print the log'''
		os.system('clear')
		print(self.log)
		if menu :
			self.printMenu()
	
	
	
	
	def write(self, txt, sep = '\n'):
		'''add lines to the log'''
		self.logFile.write(txt+sep)
		self.log += txt+sep
	
	
	
	
	def error(self, err, log = True):
		'''Display a error message and add it to the log'''
		err = '\033[31mError : '+err+'\033[0m\n'
		
		self.menuIn('Error Message')
		self.print()
		print('\n\n'+err+'Press enter to continue')
		input()
		self.menuOut()
		if log:
			self.write(err, '')
	
	
	
	
	def iadd(self,txt):
		'''redirect '+=' operator to the write()method'''
		self.write(txt);
	
	
	
	
	def menuIn(self, menu):
		'''add a menu'''
		self.menu.append(menu)
	
	
	
	
	def menuOut(self):
		'''quit a menu'''
		return self.menu.pop()
	
	
	
	
	def printMenu(self):
		'''print three structure to current menu position'''
		bar = '=========================='
		print(bar)
		if len(self.menu) == 0 :
			print('⁻⁼=####MENU ERROR####=⁼⁻\n'+bar)
		else:
			for i,m in enumerate(self.menu):
				if i == 0:
					prefix = ''
				else:
					i -= 1
					prefix = '╚═ '
				print(('  '*i)+prefix+m+' :')
			print(bar)
	
	
	
	
	
	def runPrint(self):
		'''print th running menu'''
		if self.runMenu is not None:
			print(self.runMenu)



