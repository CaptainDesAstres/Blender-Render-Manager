#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage Animation settings'''
import xml.etree.ElementTree as xmlMod
import os

class Animation:
	'''class to manage Animation settings'''
	
	
	def __init__(self, xml= None):
		'''initialize Animation settings with default value or values extracted from an xml object'''
		if xml is None:
			self.defaultInit()
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self):
		'''initialize Animation settings with default value'''
		
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize Animation settings with values extracted from an xml object'''
		
	
	
	
	
	
	def toXml(self):
		'''export Animation settings into xml syntaxed string'''
		return '<animation />\n'
		
	
	
	
	
	
	def see(self, log):
		'''menu to explore and edit Animation settings settings'''
		change = False
		log.menuIn('Animation settings')
		
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
		'''a method to print Animation settings'''
		
	
	
	
	
	
	
	
	
	
	
	
