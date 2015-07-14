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
		self.overwrite = False
		self.backup = 5
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize output path with values extracted from an xml object'''
		self.path = xml.get('path')
		self.pattern = xml.get('pattern')
		self.overwrite = {'True':True, 'False':False}[xml.get('overwrite')]
		self.backup = int(xml.get('backup'))
	
	
	
	
	
	def toXml(self):
		'''export output path into xml syntaxed string'''
		return '<output path="'+self.path+'" pattern="'+self.pattern\
			+'" overwrite="'+str(self.overwrite)+'" backup="'+str(self.backup)+'" />\n'
	
	
	
	
	
	def menu(self, log):
		'''method to see output path and access edition menu'''
		change = False
		log.menuIn('Output')
		
		while True:
			
			log.print()
			
			print('\n')
			self.print()
			
			print('''\n\n        \033[4mMenu :\033[0m
1- Edit path
2- Edit patterns
3- Switch overwrite mode
4- Change backup limit (only in «backup» overwriting mode)
0- Save And Quit

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
			elif choice == '3':
				# switch overwriting mode
				change = (self.switchOverwrite(log) or change)
			elif choice == '4':
				# edit backup limit
				change = (self.editBackupLimit(log) or change)
			else:
				log.error('Unvalid menu index!', False)
	
	
	
	
	
	def print(self):
		'''a method to display the output path settings'''
		
		print('\033[4mOutput path :\033[0m')
		print('      '+self.path)
		print('\n\033[4mOutput pattern :\033[0m')
		print('      '+self.pattern)
		print('\n\033[4mOverwriting :\033[0m')
		print('      '+{True:'enabled', False:'backup'}[self.overwrite])
		if not self.overwrite:
			print('\n\033[4mBackup limit :\033[0m')
			if self.backup == 0:
				print('      No limit')
			else:
				print('      '+str(self.backup))
	
	
	
	
	
	def editPath(self, log):
		'''method to manually edit output path'''
		log.menuIn('Edit Path')
		
		while True:
			
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
				log.error('The path must be absolute (begin by «/»)!')
				continue
			
			# check path exist 
			if not os.path.exists(choice):
				log.error('This path correspond to nothing!')
				continue
			
			# check path is a directory
			if not os.path.isdir(choice):
				log.error('This path don\'t correspond to a directory!')
				continue
			
			# check path is writable
			if not os.access(choice, os.W_OK):
				log.error('You don\'t have the permission to write in this directory!')
				continue
			
			# apply path settings and confirm
			self.path = choice
			log.write('Output path set to : '+self.path)
			log.menuOut()
			return True
	
	
	
	
	
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
				log.error('Unvalid pattern choice')
				continue
			
			# check choice is valid
			if choice < 0 or choice >= len(patterns):
				log.error('Out of range pattern choice.')
				continue
			
			# apply new settings and quit
			self.pattern = patterns[choice]
			log.write('Pattern set to : '+patterns[choice])
			log.menuOut()
			return True
	
	
	
	
	
	def switchOverwrite(self, log):
		'''A method to switch Overwrite settings'''
		self.overwrite = not self.overwrite
		log.write('Overwrite mode set to '+{True:'enabled', False:'backup'}[self.overwrite])
		return True
	
	
	
	
	
	def editBackupLimit(self, log):
		'''A method to edit Backup limit'''
		return False
	
	
	
	
	
	
	
	
	
