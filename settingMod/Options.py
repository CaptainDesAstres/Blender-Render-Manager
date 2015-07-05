#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage Rendering Options'''
import xml.etree.ElementTree as xmlMod
import os

class Options:
	'''class to manage Rendering Options'''
	
	
	def __init__(self, xml= None):
		'''initialize Rendering Options with default value or values extracted from an xml object'''
		if xml is None:
			self.defaultInit()
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self):
		'''initialize Rendering Options with default value'''
		
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize Rendering Options with values extracted from an xml object'''
		
	
	
	
	
	
	def toXml(self):
		'''export Rendering Options into xml syntaxed string'''
		txt = '<options>\n'
		
		txt += '</options>\n'
		return txt
	
	
	
	
	
	def see(self, log, versions):
		'''menu to explore and edit Rendering Options settings'''
		change = False
		log.menuIn('Rendering Options')
		
		while True:
			os.system('clear')
			log.print()
			
			self.print()
			
			print('''\n\n        Menu :
0- Save and quit

''')
			
			choice = input('Action?').strip().lower()
			
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()
				return change
			else:
				log.error('Unvalid menu choice', False)
		
	
	
	
	
	
	def print(self):
		'''a method to print Rendering Options'''
		
	
	
	
	
	
	
	
	
	
	
