#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage list of all know version of Blender in the system'''
import xml.etree.ElementTree as xmlMod
import os

class VersionList:
	'''class dedicated to Blender version managing'''
	
	
	def __init__(self, xml= None):
		'''initialize Blender version list with default value or values extracted from an xml object'''
		if xml is None:
			self.defaultInit()
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self):
		'''initialize Blender version list with default value'''
		
		self.list = {'Standard Blender':'blender'}
		
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize Blender version list with values extracted from an xml object'''
		self.list = {}
		for version in xml.findall('version'):
			self.list[version.get('alias')] = version.get('path')
	
	
	
	
	
	def toXml(self):
		'''export Blender version list into xml syntaxed string'''
		
		xml = '  <versionsList>\n'
		for k, v in self.list.items():
			xml += '    <version alias="'+k+'" path="'+v+'" />'
		xml = '  </versionsList>\n'
		
		return xml
	
	
	
	
	
	def see(self, log):
		'''method to see Blender version list and access edition menu'''
		change = False
		log.menuIn('Blender Version List')
		
		while True:
			# print log and Blender versions list
			os.system('clear')
			log.print()
			
			self.print()
			
			print('''\n    \033[4mMenu :\033[0m
1- Add version
0- Quit

''')
			
			
		
			#treat available actions
			choice= input('menu?').strip().lower()
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()# quit preferences menu
				return change
			elif choice == '1':
				change = (self.add(log) or change)
			else:
				log.write('\033[31munknow request\033[0m\n')
	
	
	
	
	
	def print(self, index = False, std = True):
		'''a method to display the Blender version list'''
		print('\n            \033[4mBlender Version List :\033[0m\n')
		
		keys = list(self.list.keys())
		keys.sort()
		
		if not std:
			# don't display Standard Blender version if std is False
			keys.remove('Standard Blender')
		
		if index:
			for i, k in enumerate(keys):
				print(str(i)+'- '+k+' :\n    '+self.list[k]+'\n')
		else:
			for k in keys:
				print(k+' :\n    '+self.list[k]+'\n')
	
	
	
	
	
	def add(self, log):
		'''a method to add a Blender version to the list'''
		confirm = False
		log.menuIn('Add A Version')
		
		while True:
			# print log 
			os.system('clear')
			log.print()
			
			# get new version path
			choice= input('path of the version?').strip().lower()
			
			if choice == '':
				log.menuOut()# quit preferences menu
				return confirm
			
			# check version path
			# get blender version from blender path
			# get user alias confirmation
			# add version
			
			log.write('\033[31mnot yet implemented\033[0m\n')
	
	
	
	
	
