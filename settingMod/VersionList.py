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
			#print log and preferences
			os.system('clear')
			log.print()
			
			self.print()
			
			print('''\n    \033[4mMenu :\033[0m
0- Quit

''')
			
			
		
			#treat available actions
			choice= input('menu?').strip().lower()
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()# quit preferences menu
				return change
			else:
				log.write('\033[31munknow request\033[0m\n')
	
	
	
	
	
	def print(self):
		'''a method to display the Blender version list'''
		print('\n            \033[4mBlender Version List :\033[0m\n')
		for k, v in self.list.items():
			print(k+' :\n    '+v+'\n')
	
	
	
	
	
	
	
	
	
	
