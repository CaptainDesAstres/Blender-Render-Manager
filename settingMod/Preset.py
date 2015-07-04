#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage preset'''
import xml.etree.ElementTree as xmlMod
from settingMod.Resolution import *
import os

class Preset:
	'''class to manage preset'''
	
	
	def __init__(self, xml= None):
		'''initialize preset with default value or values extracted from an xml object'''
		if xml is None:
			self.defaultInit()
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self):
		'''initialize preset with default value'''
		self.resolution = Resolution()
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize preset with values extracted from an xml object'''
		self.resolution = Resolution(xml.find('resolution'))
	
	
	
	
	
	def toXml(self):
		'''export preset into xml syntaxed string'''
		txt = '<preset>\n'
		txt += self.resolution.toXml()
		txt += '</preset>\n'
		return txt
	
	
	
	
	
	def see(self, log):
		'''menu to explore and edit preset settings'''
		change = False
		log.menuIn('Preset')
		
		while True:
			os.system('clear')
			log.print()
			
			self.print()
			
			print('''\n\n        Menu :
1- Edit Resolution
0- Save and quit

''')
			
			choice = input('Action?').strip().lower()
			
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()
				return change
			elif choice == '1':
				change = (self.resolution.see(log) or change)
			else:
				log.error('Unvalid menu choice', False)
		
	
	
	
	
	
	def print(self):
		'''a method to print preset'''
		self.resolution.print()
	
	
	
	
	
	
	
	
	
	
