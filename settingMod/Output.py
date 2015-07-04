#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage rendering output path'''
import xml.etree.ElementTree as xmlMod
import os
from usefullFunctions import indexPrintList

class Output:
	'''class to manage rendering output path'''
	
	
	def __init__(self, xml= None):
		'''initialize output path with default value or values extracted from an xml object'''
		if xml is None:
			self.defaultInit()
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self):
		'''initialize output path with default value'''
		
		if not os.path.exists('/home/'+os.getlogin()+'/.BlenderRenderManager/render'):
			os.mkdir('/home/'+os.getlogin()+'/.BlenderRenderManager/render')
		self.path = '/home/'+os.getlogin()+'/.BlenderRenderManager/render/'
		self.pattern = '%N - %S/%L - %F'
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize output path with values extracted from an xml object'''
		self.path = xml.get('path')
		self.pattern = xml.get('pattern')
	
	
	
	
	
	def toXml(self):
		'''export output path into xml syntaxed string'''
		return '<output path="'+self.path+'" pattern="'+self.pattern+'" />\n'
	
	
	
	
	
	def see(self, log):
		'''method to see output path and access edition menu'''
		change = False
		log.menuIn('Output')
		
		while True:
			os.system('clear')
			log.print()
			
			print('\n')
			self.print()
			
			print('''\n\n        \033[4mMenu :\033[0m
1- Edit path
2- Edit patterns
0- Quit

''')
			choice = input().strip().lower()
			
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()
				return change
			elif choice == '1':
				# edit output path
				change = (self.editPath(log) or change)
			elif choice == '2':
				# edit output pattern
				change = (self.editPattern(log) or change)
			else:
				log.write('\033[31mError : unvalid menu index!\033[0m\n')
	
	
	
	
	
	def print(self, index = False, std = True):
		'''a method to display the output path settings'''
		
		print('\033[4mOutput path :\033[0m')
		print('      '+self.path)
		print('\n\033[4mOutput pattern :\033[0m')
		print('      '+self.pattern)
	
	
	
	
	
	def editPath(self, log):
		'''method to manually edit output path'''
		log.menuIn('Edit Path')
		
		while True:
			os.system('clear')
			log.print()
			
			#print current path and ask the new one
			print('\nCurrent output path : '+self.path)
			choice = input('\n\nwhat\'s the path to use ?(absolute path required, surround path by \' or " if it contains space)').strip()
			if choice == '':
				log.menuOut()
				return False
			
			
			# remove ' and/or "
			if choice[0] in ['\'', '"'] and choice[-1] == choice[0]:
				choice  = choice[1:len(choice)-1]
			
			# check it's absolute path
			if choice[0] != '/':
				log.write('\033[31mError : the path must be absolute (begin by «/»)!\033[0m\n')
				continue
			
			# check path exist 
			if not os.path.exists(choice):
				log.write('\033[31mError : this path correspond to nothing!\033[0m\n')
				continue
			
			# check path is a directory
			if not os.path.isdir(choice):
				log.write('\033[31mError : this path don\'t correspond to a directory!\033[0m\n')
				continue
			
			# check path is writable
			if not os.access(choice, os.W_OK):
				log.write('\033[31mError : you don\'t have the permission to write in this directory!\033[0m\n')
				continue
			
			# apply path settings and confirm
	
	
	
	
	
	def editPattern(self, log):
		'''method to manually edit output pattern'''
		log.menuIn('Edit Pattern')
		# list available pattern
		patterns = [
					'%N/%S/%L/%F',
					'%N/%S/%L - %F',
					'%N - %S/%L/%F',
					'%N - %S/%L - %F',
					'%N - %S - %L/%F',
					
					'%N/%S/%F/%L',
					'%N/%S/%F - %L',
					'%N - %S/%F/%L',
					'%N - %S/%F - %L',
					'%N - %S - %F/%L',
					
					'%S/%N/%L/%F',
					'%S/%N/%L - %F',
					'%S - %N/%L/%F',
					'%S - %N/%L - %F',
					'%S - %N - %L/%F'
					]
		
		
		while True:
			os.system('clear')
			log.print()
			print('\n\n')
			
			# print available pattern and current one and ask the new one
			indexPrintList(patterns)
			print('\nCurrent pattern : '+self.pattern)
			choice = input('\n\nwhat\'s the pattern to use?(h for help)').strip().lower()
			
			# quit menu
			if choice in ['', 'q', 'quit', 'cancel']:
				log.menuOut()
				return False
			
			#display help
			if choice == 'h':
				os.system('clear')
				log.menuIn('Help')
				log.print()
				print('''\n        \033[4mPattern Help\033[0m

Choose a pattern for output file naming and directory tree. part separate by '/' will be directory and final part will be the output file name. part separate by '-' will be in the same directory/file name.

%N will be replace by the file name
%S will be replace by the scene name
%L will be replace by the renderlayer group alias
%F will be replace by the number of the frame

Press enter to continue''')
				input()
				log.menuOut()
				continue
			
			# convert choice in int
			try:
				choice = int(choice)
			except ValueError:
				log.write('\033[31mError : unvalid pattern choice\033[0m\n')
				continue
			
			# check choice is valid
			if choice < 0 or choice >= len(patterns):
				log.write('\033[31mError : out of range pattern choice\033[0m\n')
				continue
			
			# apply new settings and quit
			self.pattern = patterns[choice]
			log.write('pattern set to : '+patterns[choice]+'\n')
			log.menuOut()
			return True
	
	
	
	
	
	
	
	
